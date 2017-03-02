
import numpy as np
from sklearn.covariance import GraphLassoCV

class SparseInv:
    def __init__(self, original_matrix):
        '''
        :param dmatrix: X is an instances list(matrix)
        '''
        # X = [x(1), x(2), ..., x(len)], with dim number of features
        self._X = np.matrix(original_matrix)
        self._len, self._dim =  self._X.shape
        glasso_model = GraphLassoCV()
        glasso_model.fit(self._X)
        self._glasso_covariance = glasso_model.covariance_
        self._glasso_precision = glasso_model.precision_

    @property
    def predict_covariance(self):
        return self._glasso_covariance

    @property
    def predict_precision(self):
        return self._glasso_precision