import traceback

import numpy as np
from util import Logger
from sklearn import linear_model
from basicscaling import zeromean_y, shuffle, \
    scale_train_x, scale_test_x

class LarsRegression:
    def __init__(self, cv_num_vec, repeat_num, coef_precision):
        """
        :param cv_num_vec:
        :param repeat_num:
        """
        self._cv_num_vec = cv_num_vec
        self._repeat_num = repeat_num

        self._x_train_matrix = None
        self._x_train_matrix_scaled = None
        self._x_train_norm_vec = None
        self._x_train_mean_vec = None

        self._y_train_vec = None
        self._y_train_vec_scaled = None
        self._y_train_mean = None
        self._y_train_std = None

        self._x_train_remained_instance = None
        self._y_train_remained_instance = None

        self._predict_coef = None

        self._model_vec = []

        self._coef_precision = coef_precision

        self._logger = Logger()

    @property
    def predict_coef(self):
        return self._predict_coef

    @property
    def predict_coef_nonzero_idx(self):
        nonzero_list = np.nonzero(self._predict_coef)[0].tolist()
        return nonzero_list

    @property
    def predict_triparams_list(self):
        return list(zip(self._predict_coef,
                        self._x_train_mean_vec,
                        self._x_train_norm_vec))

    @property
    def pred_train_mean(self):
        return self._y_train_mean

    @property
    def pred_train_std(self):
        return self._y_train_std

    def filling(self, x_train, y_train):
        assert (len(x_train) == len(y_train) and
                len(x_train) > 1)

        # remain the last instance left as a valid instance,
        # so as to avoid extremely situation in model fitting.
        self._x_train_remained_instance = x_train[-1]
        self._y_train_remained_instance = y_train[-1]
        try:
            self._x_train_matrix = np.array(x_train[0:-1])
            self._x_train_matrix_scaled, self._x_train_norm_vec, \
            self._x_train_mean_vec = scale_train_x(self._x_train_matrix)

            self._y_train_vec = np.array(y_train[0:-1])
            self._y_train_vec_scaled, self._y_train_mean = zeromean_y(self._y_train_vec)
            self._y_train_std = np.std(self._y_train_vec)
        except:
            self._x_train_matrix = None
            self._y_train_vec = None
            self._logger.error(module='factormodel',
                               file='lasso.py',
                               content=traceback.format_exc())

    def fitting_with_cross_validation(self):
        # init predict coefficients to be zero vector
        self._predict_coef = np.array([0.0] * len(self._x_train_mean_vec))

        if len(self._x_train_matrix) < 10:
            self._logger.warning(module='factormodel',
                                 file='lasso.py',
                                 content="the num of training instances is less than 10. fitting exit.")
            return

        x_valid_instance_matrix = \
            scale_test_x(np.array([self._x_train_remained_instance]),
                         self._x_train_norm_vec,
                         self._x_train_mean_vec)

        y_valid_instance_value = self._y_train_remained_instance
        x_train_matrix_shuffled = self._x_train_matrix_scaled
        y_train_vec_shuffled = self._y_train_vec_scaled

        model_num = 0
        repeat_num = self._repeat_num

        for cv_num in self._cv_num_vec:
            while True:
                if repeat_num == 0 or model_num > 0:
                    break
                repeat_num -= 1
                x_train_matrix_shuffled, y_train_vec_shuffled = \
                    shuffle(x_train_matrix_shuffled, y_train_vec_shuffled)
                try:
                    model = LarsRegression._model_fitting_cv(x_train_matrix_shuffled,
                                                             y_train_vec_shuffled,
                                                             cv_num)
                    pred = model.predict(x_valid_instance_matrix)[0]
                    dist_d = abs((pred + self._y_train_mean - y_valid_instance_value) /
                                 self._y_train_std)
                    if dist_d > 5:
                        self._logger.warning(module='factormodel',
                                             file='lasso.py',
                                             content="fitting restart.")
                        continue
                    for i, v in enumerate(model.coef_):
                        self._predict_coef[i] += v
                    model_num += 1
                except:
                    self._logger.error(module='factormodel',
                                       file='lasso.py',
                                       content=traceback.format_exc())
                    continue
        if model_num == 0:
            self._logger.warning(module='factormodel',
                                 file='lasso.py',
                                 content="fitting with cross validation failed. model num is zero.")

        precision_base = float(np.power(10, self._coef_precision))
        # let coef vec keep 2 decimal precision
        self._predict_coef = [int(v * precision_base ) / precision_base
                              for v in self._predict_coef]

    def fitting_without_cross_validation(self):
        self._predict_coef = np.array([0.0] * len(self._x_train_mean_vec))

        if len(self._x_train_matrix) < 10:
            self._logger.warning(module='factormodel',
                                 file='lasso.py',
                                 content="the num of training instances is less than 10. fitting exit.")
            return
        try:
            model = LarsRegression._model_fitting(
                self._x_train_matrix_scaled + [self._x_train_remained_instance],
                self._y_train_vec_scaled + [self._y_train_remained_instance])
            for i, v in enumerate(model.coef_):
                self._predict_coef[i] += v
        except:
            # traceback.print_exc()
            self._logger.error(module='factormodel',
                               file='lasso.py',
                               content="fitting without cross validation failed.")

    def predict(self, x_test_array):
        x_test_matrix = scale_test_x(np.array([x_test_array]),
                                     self._x_train_norm_vec,
                                     self._x_train_mean_vec)
        pred = 0
        for v, p in list(zip(x_test_matrix[0], self._predict_coef)):
            pred += v * p
        pred += self._y_train_mean
        return pred

    def nonzero_list(self):
        # nonzero_idx_arr = sorted(np.nonzero(coef)[0].tolist(),
        #    cmp=lambda x1, x2: 1 if abs(coef[x1]) < abs(coef[x2]) else -1)
        return sorted(self.predict_coef_nonzero_idx)

    # LassoLarsCV: least angle regression
    @classmethod
    def _model_fitting_cv(cls, x, y, num_cv, plotting=False):
        # Compute paths
        # print("Computing regularization path using the Lars lasso...")
        model = linear_model.LassoLarsCV(cv=num_cv).fit(x, y)
        # Display results
        if plotting:
            import matplotlib.pyplot as plt
            m_log_alphas = -np.log10(model.cv_alphas_)
            plt.figure(figsize=(20, 10))
            plt.plot(m_log_alphas, model.cv_mse_path_, ':')
            plt.plot(m_log_alphas, model.cv_mse_path_.mean(axis=-1), 'k',
                     label='Average across the folds', linewidth=2)
            plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
                        label='alpha CV')
            plt.legend()
            plt.xlabel('-log(alpha)')
            plt.ylabel('Mean square error')
            plt.axis('tight')
            plt.savefig('cross_validation', dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None)
            plt.plot()
        return model

    @classmethod
    def _model_fitting(cls, x, y, alpha=0, max_iter=500):
        model = linear_model.LassoLars(alpha=alpha, max_iter=max_iter).fit(x, y)
        return model
