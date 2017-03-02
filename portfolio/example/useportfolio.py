
import numpy as np
from factormodel import MultTask
from portfolio import Portfolio, simplex_projection

# Example1:
rng = np.random.RandomState(42)
n_samples, n_features, n_tasks = 200, 65, 15
n_relevant_features = 5
coef = np.zeros((n_tasks, n_features))
times = np.linspace(0, 1 * np.pi, n_tasks)
for k in range(n_relevant_features):
    coef[:, k] = np.sin((1. + rng.randn(1)) * times + 10 * rng.randn(1))
X_train = rng.randn(n_samples, n_features)
X_test = rng.randn(1, n_features)
Y = np.dot(X_train, coef.T) + rng.randn(n_samples, n_tasks)

multTask_msl = MultTask(X_train, Y, 'msl')
riskcov_msl = multTask_msl.get_riskcov_matrix_lowrank()
predret_msl = multTask_msl.predict(X_test).tolist()[0]

print predret_msl, riskcov_msl
asset_weight = Portfolio([1.0 / 15] * 15,
                         n_tasks,
                         predret_msl,
                         riskcov_msl,
                         adjust_thres=0.3,
                         risk_thres=2).asset_weight
print asset_weight

# Example2:
predret = [0.035473298104288856, 0.016754470186157628,
           0.039721257216909396, 0.04829577572334836, 0.03724257748540197]
covmt = [[ 0.00614162,  0.00300124,  0.00422327,  0.00518325,  0.00796089],
         [ 0.00300124,  0.00204993,  0.00219752,  0.00294939,  0.00371477],
         [ 0.00422327,  0.00219752,  0.00306912,  0.0037098,   0.00549926],
         [ 0.00518325,  0.00294939,  0.0037098,  0.00486506,  0.00670856],
         [ 0.00796089,  0.00371477,  0.00549926,  0.00670856,  0.01062155]]

print Portfolio([1.0 / 5] * 5,
                5,
                predret,
                covmt,
                0.5,
                1).asset_weight