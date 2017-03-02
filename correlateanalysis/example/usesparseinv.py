
import matplotlib.pyplot as plt
import numpy as np

def plotting_covariances(emp_cov, est_cov, model=None):
    plt.figure(figsize=(20, 12))
    plt.subplots_adjust(left=0.02, right=0.98)
    covs = [('Empirical', emp_cov), ('Estimated', est_cov)]
    vmax = est_cov.max()
    for i, (name, this_cov) in enumerate(covs):
        plt.subplot(1, 2, i + 1)
        plt.imshow(this_cov, interpolation='nearest', vmin=-vmax, vmax=vmax,
                   cmap=plt.cm.RdBu_r)
        plt.xticks(())
        plt.yticks(())
        plt.title('%s covariance' % name)

    if  model:
        # plot the model selection metric
        plt.figure(figsize=(4, 3))
        plt.axes([.2, .15, .75, .7])
        plt.plot(model.cv_alphas_, np.mean(model.grid_scores, axis=1), 'o-')
        plt.axvline(model.alpha_, color='.5')
        plt.title('Model selection')
        plt.ylabel('Cross-validation score')
        plt.xlabel('alpha')

    plt.show()

if __name__ == '__main__':
    from scipy import linalg
    from sklearn.datasets import make_sparse_spd_matrix

    n_samples, n_features = 1000, 100

    prng = np.random.RandomState(1)
    prec = make_sparse_spd_matrix(n_features, alpha=.98,
                                  smallest_coef=.4,
                                  largest_coef=.7,
                                  random_state=prng)
    cov = linalg.inv(prec)
    d = np.sqrt(np.diag(cov))
    cov /= d
    cov /= d[:, np.newaxis]
    prec *= d
    prec *= d[:, np.newaxis]
    X = prng.multivariate_normal(np.zeros(n_features), cov, size=n_samples)

    # X is a matrix with shape (n_samples, n_features)
    from correlateanalysis.covariance import Covariance
    from correlateanalysis.sparseinv import SparseInv
    plotting_covariances(Covariance(X).empirical_covariance,
                         SparseInv(X).predict_covariance)