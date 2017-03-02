
"""
Demo to test Multi-Task-Lasso and Multi-Single-Lasso
"""
import numpy as np
import matplotlib.pyplot as plt
from factormodel import MultTask
rng = np.random.RandomState(42)

# Generate some 2D coefficients with sine waves
# with random frequency and phase
n_samples, n_features, n_tasks = 200, 80, 3
n_relevant_features = 10
coef = np.zeros((n_tasks, n_features))
times = np.linspace(0, 1 * np.pi, n_tasks)
for k in range(n_relevant_features):
    coef[:, k] = np.sin((1. + rng.randn(1)) * times + 1 * rng.randn(1))

X_train = rng.randn(n_samples, n_features)
X_test = rng.randn(1, n_features)
Y = np.dot(X_train, coef.T) + rng.randn(n_samples, n_tasks)

print "The shape of X_train is %s" % str(X_train.shape)
print "The shape of Y is %s" % str(Y.shape)

multTask_msl = MultTask(X_train, Y, 'msl')
multTask_mtl = MultTask(X_train, Y, 'mtl')

print multTask_mtl.predict(X_train) - multTask_mtl.predict_on_train()
# print multTask_mtl.predict(X) - Y

beta_msl = multTask_msl.beta_matrix
beta_mtl = multTask_mtl.beta_matrix

print multTask_msl.riskcov_matrix_empirical
print multTask_mtl.riskcov_matrix_empirical

print multTask_msl.get_riskcov_matrix_lowrank()
print multTask_mtl.get_riskcov_matrix_lowrank()

print multTask_msl.get_riskcov_matrix_lowrank('sinv')
print multTask_mtl.get_riskcov_matrix_lowrank('sinv')

print multTask_msl.predict(X_test)
print multTask_mtl.predict(X_test)

fig = plt.figure(figsize=(5, 10))
plt.subplot(1, 2, 1)
plt.spy(beta_msl)
plt.xlabel('Feature')
plt.ylabel('Time (or Task)')
plt.text(10, 5, 'Lasso')
plt.subplot(1, 2, 2)
plt.spy(beta_mtl)
plt.xlabel('Feature')
plt.ylabel('Time (or Task)')
plt.text(10, 5, 'MultiTaskLasso')
fig.suptitle('Coefficient non-zero location')

feature_to_plot = 0
plt.figure()
lw = 2
plt.plot(coef[:, feature_to_plot], color='seagreen', linewidth=lw,
         label='Ground truth')
plt.plot(beta_msl.T[:, feature_to_plot], color='cornflowerblue', linewidth=lw,
         label='Lasso')
plt.plot(beta_mtl.T[:, feature_to_plot], color='gold', linewidth=lw,
         label='MultiTaskLasso')
plt.legend(loc='upper center')
plt.axis('tight')
plt.ylim([-1.1, 1.1])
plt.show()

