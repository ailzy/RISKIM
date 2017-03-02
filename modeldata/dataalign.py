
from datastack import DataStack

class DataAlign:
    def __init__(self, datastack, window=120):
        assert (isinstance(datastack, DataStack))
        self._datastack = datastack
        self._date_list = []
        self._Y_matrix = []
        self._X_matrix = []
        self._X_matrix_remain = []
        self._date_list_remain = []
        self._lookback_window = window
        self._build()

    def _build(self):
        target_date_list = self._datastack.target_date_list
        target_value_matrix = self._datastack.target_value_matrix
        talib_indicator_date_list = self._datastack.talib_indicator_date_list
        talib_indicator_value_matrix = self._datastack.talib_indicator_value_matrix
        macro_indicator_date_list = self._datastack.macro_indicator_date_list
        macro_indicator_value_matrix = self._datastack.macro_indicator_value_matrix

        tm_common_date_set = set(talib_indicator_date_list) & \
                             set(macro_indicator_date_list)

        ttm_common_date_set = set(target_date_list) & \
                              set(tm_common_date_set)

        date_list_xall = sorted(list(tm_common_date_set))
        self._date_list = sorted(list(ttm_common_date_set))

        X_matrix_all = []
        for date, value_vector in list(zip(talib_indicator_date_list,
                                           talib_indicator_value_matrix)):
            if date in tm_common_date_set:
                X_matrix_all.append(list(value_vector))

            if date in ttm_common_date_set:
                self._X_matrix.append(list(value_vector))

        idx1, idx2, cutoff_idx = 0, 0, None
        for date, value_vector in list(zip(macro_indicator_date_list,
                                           macro_indicator_value_matrix)):
            if date in tm_common_date_set:
                X_matrix_all[idx1] += value_vector
                idx1 += 1
                if date == self._date_list[-1]:
                    cutoff_idx = idx1

            if date in ttm_common_date_set:
                self._X_matrix[idx2] += value_vector
                idx2 += 1

        self._X_matrix_remain = X_matrix_all[cutoff_idx:]
        self._date_list_remain = date_list_xall[cutoff_idx:]

        for date, value_vector in list(zip(target_date_list,
                                           target_value_matrix)):
            if date in ttm_common_date_set:
                self._Y_matrix.append(value_vector)

        self._date_list = self._date_list[-self._lookback_window:]
        self._X_matrix = self._X_matrix[-self._lookback_window:]
        self._Y_matrix = self._Y_matrix[-self._lookback_window:]

    @property
    def len(self):
        return len(self._date_list)

    @property
    def date_list(self):
        return self._date_list
    @property
    def X_matrix_remain(self):
        return self._X_matrix_remain

    @property
    def date_list_remain(self):
        return self._date_list_remain

    @property
    def Y_matrix(self):
        return self._Y_matrix

    @property
    def X_matrix(self):
        return self._X_matrix

