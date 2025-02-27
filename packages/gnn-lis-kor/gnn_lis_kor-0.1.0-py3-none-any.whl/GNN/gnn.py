import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.nn import Linear
from torch_geometric.datasets import MovieLens
from torch_geometric.nn import SAGEConv, to_hetero
import torch_geometric.transforms as T
import optuna
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import logging
optuna.logging.set_verbosity(optuna.logging.WARNING)

# Загрузка данных
dataset_path = '/tmp/'
dataset = MovieLens(root=dataset_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = dataset[0].to(device)

# Подготовка данных
data['user'].x = torch.eye(data['user'].num_nodes, device=device)
del data['user'].num_nodes
data = T.ToUndirected()(data)
del data['movie', 'rev_rates', 'user'].edge_label

train_data, val_data, test_data = T.RandomLinkSplit(
    num_val=0.1,
    num_test=0.1,
    neg_sampling_ratio=0.0,
    edge_types=[('user', 'rates', 'movie')],
    rev_edge_types=[('movie', 'rev_rates', 'user')],
)(data)

weight = torch.bincount(train_data['user', 'movie'].edge_label)
weight = weight.max() / weight


# Функция ошибки
def weighted_mse_loss(pred, target, weight=None):
    weight = 1. if weight is None else weight[target].to(pred.dtype)
    return (weight * (pred - target.to(pred.dtype)).pow(2)).mean()


# Модель
class GNNEncoder(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels, dropout=0.5):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.dropout = torch.nn.Dropout(p=dropout)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x


class EdgeDecoder(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.lin1 = Linear(2 * hidden_channels, hidden_channels)
        self.lin2 = Linear(hidden_channels, 1)

    def forward(self, z_dict, edge_label_index):
        row, col = edge_label_index
        z = torch.cat([z_dict['user'][row], z_dict['movie'][col]], dim=-1)
        z = self.lin1(z).relu()
        z = self.lin2(z)
        return z.view(-1)


class GNNModel(torch.nn.Module):
    def __init__(self, hidden_channels, dropout=0.5):
        super().__init__()
        self.encoder = GNNEncoder(hidden_channels, hidden_channels, dropout=dropout)
        self.encoder = to_hetero(self.encoder, data.metadata(), aggr='sum')
        self.decoder = EdgeDecoder(hidden_channels)

    def forward(self, x_dict, edge_index_dict, edge_label_index):
        z_dict = self.encoder(x_dict, edge_index_dict)
        return self.decoder(z_dict, edge_label_index)


def train():
    model.train()
    optimizer.zero_grad()
    pred = model(train_data.x_dict, train_data.edge_index_dict,
                 train_data['user', 'movie'].edge_label_index)
    target = train_data['user', 'movie'].edge_label
    loss = weighted_mse_loss(pred, target, weight)
    loss.backward()
    optimizer.step()
    return float(loss)


@torch.no_grad()
def test(data):
    model.eval()
    pred = model(data.x_dict, data.edge_index_dict,
                 data['user', 'movie'].edge_label_index)
    pred = pred.clamp(min=0, max=5)
    target = data['user', 'movie'].edge_label.float()
    rmse = F.mse_loss(pred, target).sqrt()
    return float(rmse)

# Оптимизация с Optuna
def objective(trial):
    hidden_channels = trial.suggest_int('hidden_channels', 16, 128, step=16)
    lr = trial.suggest_float('lr', 1e-5, 1e-2, log=True)
    epochs = trial.suggest_int('epochs', 100, 500, step=10)
    weight_decay = trial.suggest_float('weight_decay', 1e-6, 1e-2, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.7)
    
    model = GNNModel(hidden_channels=hidden_channels, dropout=0.5).to(device)
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)

    def train():
        model.train()
        optimizer.zero_grad()
        pred = model(train_data.x_dict, train_data.edge_index_dict,
                     train_data['user', 'movie'].edge_label_index)
        target = train_data['user', 'movie'].edge_label
        loss = weighted_mse_loss(pred, target, weight)
        loss.backward()
        optimizer.step()
        return float(loss)
    
    @torch.no_grad()
    def test(data):
        model.eval()
        pred = model(data.x_dict, data.edge_index_dict,
                     data['user', 'movie'].edge_label_index)
        pred = pred.clamp(min=0, max=5)
        target = data['user', 'movie'].edge_label.float()
        rmse = F.mse_loss(pred, target).sqrt()
        return float(rmse)
    
    for epoch in range(epochs):
        train()
    
    val_rmse = test(val_data)
    return val_rmse


# Оптимизация гиперпараметров
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=30)
print("Best hyperparameters:", study.best_params)

# Обучение с лучшими гиперпараметрами
best_params = study.best_params
model = GNNModel(best_params['hidden_channels'], dropout=0.5).to(device)
optimizer = AdamW(model.parameters(), lr=best_params['lr'], weight_decay=best_params['weight_decay'])

epoch_list, loss_list, train_rmse_list, val_rmse_list, test_rmse_list = [], [], [], [], []

for epoch in tqdm(range(1, best_params['epochs'] + 1), desc="Training Progress", unit="epoch"):
    loss = train()
    train_rmse = test(train_data)
    val_rmse = test(val_data)
    test_rmse = test(test_data)
    epoch_list.append(epoch)
    train_rmse_list.append(train_rmse)
    val_rmse_list.append(val_rmse)
    test_rmse_list.append(test_rmse)

# Визуализация
plt.plot(epoch_list, train_rmse_list, label='Train RMSE')
plt.plot(epoch_list, val_rmse_list, label='Validation RMSE')
plt.plot(epoch_list, test_rmse_list, label='Test RMSE')
plt.legend()
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.title('Training and Validation Metrics')
plt.grid(True)
plt.show()

from torch_geometric.nn import GATConv

# Модель с GATConv
class GNNEncoder(torch.nn.Module):
    def __init__(self, hidden_channels, out_channels, heads=1, dropout=0.5):
        super().__init__()
        self.conv1 = GATConv(
            (-1, -1), 
            hidden_channels, 
            heads=heads, 
            dropout=dropout, 
            add_self_loops=False  # Отключаем self-loops
        )
        self.dropout = torch.nn.Dropout(p=dropout)
        self.conv2 = GATConv(
            (-1, -1), 
            out_channels, 
            heads=1, 
            concat=False, 
            dropout=dropout, 
            add_self_loops=False  # Отключаем self-loops
        )

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x


class GNNModel(torch.nn.Module):
    def __init__(self, hidden_channels, dropout=0.5, heads=1):
        super().__init__()
        self.encoder = GNNEncoder(hidden_channels, hidden_channels, heads=heads, dropout=dropout)
        self.encoder = to_hetero(self.encoder, data.metadata(), aggr='sum')
        self.decoder = EdgeDecoder(hidden_channels)
    
    def forward(self, x_dict, edge_index_dict, edge_label_index):
        # Кодирование графа
        z_dict = self.encoder(x_dict, edge_index_dict)
        # Декодирование рёбер
        return self.decoder(z_dict, edge_label_index)


def train():
    model.train()
    optimizer.zero_grad()
    pred = model(train_data.x_dict, train_data.edge_index_dict,
                 train_data['user', 'movie'].edge_label_index)
    target = train_data['user', 'movie'].edge_label
    loss = weighted_mse_loss(pred, target, weight)
    loss.backward()
    optimizer.step()
    return float(loss)


@torch.no_grad()
def test(data):
    model.eval()
    pred = model(data.x_dict, data.edge_index_dict,
                 data['user', 'movie'].edge_label_index)
    pred = pred.clamp(min=0, max=5)
    target = data['user', 'movie'].edge_label.float()
    rmse = F.mse_loss(pred, target).sqrt()
    return float(rmse)


# Функция для Optuna
def objective(trial):
    hidden_channels = trial.suggest_int('hidden_channels', 16, 128, step=16)
    heads = trial.suggest_int('heads', 1, 8)
    lr = trial.suggest_float('lr', 1e-5, 1e-2, log=True)
    epochs = trial.suggest_int('epochs', 100, 1000, step=10)
    weight_decay = trial.suggest_float('weight_decay', 1e-6, 1e-2, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.7)

    model = GNNModel(hidden_channels=hidden_channels, heads=heads, dropout=dropout).to(device)
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)

    def train():
        model.train()
        optimizer.zero_grad()
        pred = model(train_data.x_dict, train_data.edge_index_dict,
                     train_data['user', 'movie'].edge_label_index)
        target = train_data['user', 'movie'].edge_label
        loss = weighted_mse_loss(pred, target, weight)
        loss.backward()
        optimizer.step()
        return float(loss)
    
    @torch.no_grad()
    def test(data):
        model.eval()
        pred = model(data.x_dict, data.edge_index_dict,
                     data['user', 'movie'].edge_label_index)
        pred = pred.clamp(min=0, max=5)
        target = data['user', 'movie'].edge_label.float()
        rmse = F.mse_loss(pred, target).sqrt()
        return float(rmse)
    
    for epoch in range(epochs):
        train()
    
    val_rmse = test(val_data)
    return val_rmse


# Запуск оптимизации
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=30)
print("Best hyperparameters:", study.best_params)

# Обучение с лучшими гиперпараметрами
best_params = study.best_params
model = GNNModel(
    hidden_channels=best_params['hidden_channels'],
    heads=best_params['heads'],
    dropout=best_params['dropout']
).to(device)
optimizer = AdamW(model.parameters(), lr=best_params['lr'], weight_decay=best_params['weight_decay'])

epoch_list, train_rmse_list, val_rmse_list, test_rmse_list = [], [], [], []

for epoch in tqdm(range(1, best_params['epochs'] + 1), desc="Training Progress", unit="epoch"):
    loss = train()
    train_rmse = test(train_data)
    val_rmse = test(val_data)
    test_rmse = test(test_data)
    epoch_list.append(epoch)
    train_rmse_list.append(train_rmse)
    val_rmse_list.append(val_rmse)
    test_rmse_list.append(test_rmse)

# Визуализация результатов
plt.plot(epoch_list, train_rmse_list, label='Train RMSE')
plt.plot(epoch_list, val_rmse_list, label='Validation RMSE')
plt.plot(epoch_list, test_rmse_list, label='Test RMSE')
plt.legend()
plt.xlabel('Epoch')
plt.ylabel('Value')
plt.title('Training and Validation Metrics (GATConv)')
plt.grid(True)
plt.show()