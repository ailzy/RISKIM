import numpy as np
import math

class Covariance:
    def __init__(self, original_matrix):
        '''
        :param dmatrix: X is an instances list(matrix)
        '''
        # X = [x(1), x(2), ..., x(len)], with dim number of features
        self._X_org_matrix = np.matrix(original_matrix).T
        self._dim, self._len =  self._X_org_matrix.shape

        self._X_matrix_mean = self._X_org_matrix.mean(axis=1)
        self._X_matrix_std = self._X_org_matrix.std(axis=1)
        self._X_matrix_morm = self._X_matrix_std * math.sqrt(self._len)

        self._X_matrix_meanzero = self._X_org_matrix - self._X_matrix_mean
        self._X_matrix_standardized = self._X_matrix_meanzero / self._X_matrix_std
        self._X_matrix_normalized = self._X_matrix_meanzero / self._X_matrix_morm

        self._empirical_gram = np.dot(self._X_matrix_normalized,
                                      self._X_matrix_normalized.T)
        self._empirical_covariance = np.dot(self._X_matrix_meanzero,
                                            self._X_matrix_meanzero.T) / self._len
        self._empirical_correlation = np.dot(self._X_matrix_standardized,
                                            self._X_matrix_standardized.T)

    @property
    def shape(self):
        return self._dim, self._len

    @property
    def instances_len(self):
        return self._len

    @property
    def dimension_num(self):
        return self._dim

    @property
    def org_matrix(self):
        return self._X_org_matrix

    @property
    def standardized_matrix(self):
        return self._X_matrix_standardized

    @property
    def normalized_matrix(self):
        return self._X_matrix_normalized

    @property
    def mean_matrix(self):
        return self._X_matrix_mean

    @property
    def std_matrix(self):
        return self._X_matrix_std

    @property
    def norm_matrix(self):
        return self._X_matrix_morm

    @property
    def empirical_gram(self):
        return self._empirical_gram

    @property
    def empirical_covariance(self):
        return self._empirical_covariance

    @property
    def empirical_correlation(self):
        return self._empirical_correlation

if __name__ == '__main__':
    datamatrix = Covariance([[2, 3, 4, 5],
                             [12, 13, 14, 15],
                             [22, 23, 24, 25]])
    print datamatrix.mean_matrix
    print datamatrix.std_matrix
    print datamatrix.norm_matrix
    print datamatrix.standardized_matrix
    print datamatrix.empirical_covariance
    print datamatrix.empirical_correlation

