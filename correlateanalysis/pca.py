import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

class PrincipalAnalysis:
    def __init__(self, original_matrix, shrinkage_ratio=0.5):
        self._X_org_matrix = np.matrix(original_matrix)
        self._len, self._dim =  self._X_org_matrix.shape
        n_components = int(max(min(self._dim, self._len) * shrinkage_ratio, 2))
        self._pca = PCA(n_components)
        self._pca.fit(self._X_org_matrix)
        self._components_num = self._pca.n_components_
        self._components_value_list = self._pca.components_
        self._singular_value_list_in = self._pca.explained_variance_
        self._singular_value_list_out = self._pca.noise_variance_
        minvar = min(self._pca.explained_variance_)
        sigma = - minvar if minvar < 0 else 0
        self._lowrank_cov = np.array(self._pca.components_).T.dot(
            np.diag(self._pca.explained_variance_ +
                    [sigma] * len(self._pca.explained_variance_)
                    )).dot(
            np.array(self._pca.components_))

    @property
    def predict_covariance(self):
        return self._lowrank_cov

