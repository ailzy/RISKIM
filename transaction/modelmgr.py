
import numpy as np
from util import Logger
from copy import deepcopy
from calendarmgr import CalendarMgr
from factormodel import MultTask
from modeldata import DataCache, DataAlign, DataStack

class ModelMgr:
    def __init__(self,
                 this_date,
                 datacache,
                 lookback_window=120,
                 talib_period=[10, 20, 30, 40, 50, 60]):
        """
        :param this_date:
        :param datacache:
        :param lookback_window:
        """
        assert (isinstance(datacache, DataCache))
        self._this_date = this_date
        self._datacache = datacache
        self._multtask_model = None
        self._riskcov = None
        self._talib_period = talib_period
        self._lookback_window = lookback_window
        self._logger = Logger()

    def build(self):
        self._logger.info(module='transaction',
                          file='modelmgr.py',
                          content="The datetime now is %s. Building DataStack..." % self._this_date)
        datastack = DataStack(self._datacache, 'retsum_prediction',
                              params_dict={'calendar': 'month', 'period_list': self._talib_period})
        self._logger.info(module='transaction',
                          file='modelmgr.py',
                          content="Date range of returen mean prediction. " +
                                  "Target value start at %s, end at %s. " %
                                  (datastack.target_date_list[0], datastack.target_date_list[-1]) +
                                  "Talib indicator value start at %s, end at %s. " %
                                  (datastack.talib_indicator_date_list[0], datastack.talib_indicator_date_list[-1]) +
                                  "Macro indicator value start at %s, end at %s. " %
                                  (datastack.macro_indicator_date_list[0], datastack.macro_indicator_date_list[-1]))
        dataalign = DataAlign(datastack, self._lookback_window)
        self._logger.info(module='transaction',
                          file='modelmgr.py',
                          content="Alignment of the target and indicator values in sharperatio prediction. " +
                                  "Target value start at %s, end at %s. " %
                                  (dataalign.date_list[0], dataalign.date_list[-1]) +
                                  "DataStack and DataAlign complete.")

        X_train_matrix = np.array(dataalign.X_matrix)
        Y_train_matrix = np.array(dataalign.Y_matrix)
        X_pred_matrix = np.array(dataalign.X_matrix_remain)
        self._logger.info(module='transaction',
                          file='modelmgr.py',
                          content="Shape of X matrix is %s. " % str(X_train_matrix.shape) +
                                  "Shape of Y matrix is %s. " % str(Y_train_matrix.shape) +
                                  "Shape of X_pred_matrix is %s." % str(X_pred_matrix.shape))

        self._logger.info(module="transaction",
                          file="modelmgr.py",
                          content="Now doing multiple tasks fitting.")
        self._multtask_model = MultTask(X_train_matrix, Y_train_matrix, 'msl')
        self._riskcov_empirical = self._multtask_model.riskcov_matrix_empirical
        self._riskcov_lowrank = self._multtask_model.get_riskcov_matrix_lowrank()
        self._pred_ret = self._multtask_model.predict(X_pred_matrix).tolist()
        average_num = min(len(self._pred_ret), 10)

        self._ret = None
        # self._ret = np.array(self._pred_ret[-average_num:]).T.dot(
        #     np.ones((average_num, 1))) / float(average_num)

        for ret_vec in self._pred_ret[-average_num:]:
            if not self._ret:
                self._ret = deepcopy(ret_vec)
            else:
                for i, v in enumerate(ret_vec):
                    self._ret[i] += v
            for i in range(len(self._ret)):
                self._ret[i] /= float(average_num) + 1e-10

        self._logger.info(module="transaction",
                          file="modelmgr.py",
                          content="Multiple tasks fitting complete.")

    @property
    def riskcov_ep(self):
        return self._riskcov_empirical

    @property
    def riskcov_lr(self):
        return self._riskcov_lowrank

    @property
    def ret(self):
        return self._ret
