
import numpy as np
from util import Logger
from lasso import LarsRegression
from correlateanalysis import Covariance, PrincipalAnalysis, SparseInv
from sklearn.linear_model import MultiTaskLassoCV

class MultTask:
    def __init__(self, value_matrix, target_matrix, mode='msl'):
        """
        :param value_matrix: N lists with each D dim features
        :param target_matrix: N lists with each M dim targets
        :param mode: msl or mtl
        msl: multi-single-lasso
        mtl: multi-task-lasso
        """
        self._logger = Logger()
        self._logger.info(module='factormodel',
                          file='multtask.py',
                          content="Building mult-tasks fitting.")
        assert (len(value_matrix) == len(target_matrix))
        self._A = value_matrix
        self._B = target_matrix
        self._lars_regressor_list = []

        # construct lars regression model list
        assert (len(self._A) == len(self._B))

        self._A_cov = Covariance(self._A)
        self._B_cov = Covariance(self._B)

        self._A_mean = self._A_cov.mean_matrix
        self._A_norm = self._A_cov.norm_matrix
        self._A_std = self._A_cov.std_matrix
        self._A_normalized = self._A_cov.normalized_matrix
        self._A_instance_list = self._A_normalized.T.tolist()

        self._B_mean = self._B_cov.mean_matrix
        self._B_norm = self._B_cov.norm_matrix
        self._B_std = self._B_cov.std_matrix
        self._B_normalized = self._B_cov.normalized_matrix

        self._beta_matrix_decay = None

        self._logger.info(module='factormodel',
                          file='multtask.py',
                          content="Gram construction complete, now doing model fitting.")
        if mode == 'msl':
            self._Beta_msl = []
            for i, target_vec in enumerate(self._B_normalized.tolist()):
                lars_regressor = LarsRegression([2, 3], 10, 5)
                lars_regressor.filling(self._A_instance_list, target_vec)
                lars_regressor.fitting_with_cross_validation()
                self._Beta_msl.append(lars_regressor.predict_coef)
                # print "    the task %s is complete." % str(i)
            self._beta_matrix_decay = np.array(self._Beta_msl).T
        elif mode == 'mtl':
            """ (1 / (2 * n_samples)) * ||Y - XW||^Fro_2 + alpha * ||W||_21
                ||W||_21 = \sum_i \sqrt{\sum_j w_{ij}^2}
            """
            self._beta_matrix_decay = MultiTaskLassoCV(cv=2).fit(self._A_normalized.T,
                                                     self._B_normalized.T).coef_
            self._beta_matrix_decay = np.array(self._beta_matrix_decay).T

        self._logger.info(module='factormodel',
                          file='multtask.py',
                          content="The multi-tasks fitting complete.")
        self._beta_matrix = np.multiply(self._beta_matrix_decay,
                                        (1 / self._A_norm).dot(self._B_norm.T))
        self._delta_matrix = - self._A_mean.T.dot(self._beta_matrix) + self._B_mean.T
        self._cov_matrix = self._beta_matrix.T.dot(
            self._A_cov.empirical_covariance).dot(self._beta_matrix)
        self._cov_matrix_lowrank = None

    @property
    def beta_matrix(self):
        return self._beta_matrix

    def predict_on_train(self):
        return np.multiply(self._A_normalized.T.dot(
            self._beta_matrix_decay), self._B_norm.T) + self._B_mean.T

    def predict(self, instance_list):
        return np.array(instance_list).dot(self._beta_matrix) \
               + self._delta_matrix

    @property
    def riskcov_matrix_empirical(self):
        return self._cov_matrix

    def _riskcov_sparseinverse_estimation(self):
        nonzero_dim_list = []
        selected_beta_list = []
        for i, beta_row in enumerate(self._beta_matrix.tolist()):
            if sum(beta_row) != 0:
                nonzero_dim_list.append(i)
                selected_beta_list.append(beta_row)

        dims_list = list(zip(*self._A))
        selected_dims_list = []
        for i in nonzero_dim_list:
            selected_dims_list.append(dims_list[i])

        beta_matrix = np.array(selected_beta_list)
        inst_matrix = np.array(selected_dims_list).T

        self._logger.info(module='factormodel',
                          file='multtask.py',
                          content="Doing sparse inverse estimation of gram matrix.")
        self._cov_matrix_lowrank = beta_matrix.T.dot(
            SparseInv(inst_matrix).predict_covariance).dot(beta_matrix)

    def _riskcov_pca_estimation(self):
        self._cov_matrix_lowrank = self._beta_matrix.T.dot(
            PrincipalAnalysis(self._A).predict_covariance).dot(self._beta_matrix)

    def get_riskcov_matrix_lowrank(self, mode='pca'):
        if mode=='pca':
            self._riskcov_pca_estimation()
        elif mode == 'spinv':
            self._riskcov_sparseinverse_estimation()
        return self._cov_matrix_lowrank

    @property
    def matrix_A_stand(self):
        return self._A_norm

    @property
    def matrix_A_mean(self):
        return self._A_mean

    @property
    def matrix_A_std(self):
        return self._A_std

    @property
    def matrix_B_stand(self):
        return self._B_norm

    @property
    def matrix_B_mean(self):
        return self._B_mean

    @property
    def matrix_B_std(self):
        return self._B_std




