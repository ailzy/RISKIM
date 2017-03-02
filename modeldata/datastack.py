
"""
Model
===============================================

"""
import numpy as np
from copy import deepcopy
from datetime import timedelta
import traceback
from util import Logger
from datacache import DataCache
from factorutil import Factorseries

class DataStack:
    def __init__(self, datacache, taskname,
                 params_dict={'calendar': 'month', 'period_list': [10]}):
        """
        :param mode: mode
            'netvalue_perdiction' or 'sharperatio_prediction'
        :param params:
            the type and value of params according to the mode.
        """
        self._taskname = taskname
        assert (isinstance(datacache, DataCache))
        self._datacache = datacache
        self._params_dict = params_dict

        self._talib_indicator_date_list = None
        self._talib_indicator_value_matrix = None

        self._macro_indicator_date_list = None
        self._macro_indicator_value_matrix = None

        self._target_date_list = None
        self._target_value_matrix = None

        self._logging = lambda content: Logger().info(module='model', file='datastack.py',
                                                      content=content)
        self._build()

    def _build(self):
        if len(self._datacache) == 0:
            self._logging("Datacache contains 0 objectives, build DataStack stop.")
            return

        date_list = self._datacache.date_list
        fund_matrix_transpose = self._datacache.fund_matrix_transpose
        index_matrix_transpose = self._datacache.index_matrix_transpose
        macro_matrix_transpose = self._datacache.macro_matrix_transpose

        targetseries_list, talib_indicatorseries_list = None, None

        try:
            self._logging("Building Factorseries...")
            if self._taskname == 'netvalue_prediction':
                targetseries_list = [Factorseries(date_list, value_list, 'backward_ratio')
                                     for value_list in fund_matrix_transpose]
                talib_indicatorseries_list, = [Factorseries(date_list, value_list, 'backward_ratio')
                                    for value_list in index_matrix_transpose]
            else:
                factorseries_mode = None
                if self._taskname == 'sharperatio_prediction':
                    factorseries_mode = 'forward_ret_sharpe'
                elif self._taskname == 'retmean_prediction':
                    factorseries_mode = 'forward_ret_mean'
                elif self._taskname == 'retsum_prediction':
                    factorseries_mode = 'forward_ret_sum'
                targetseries_list = [Factorseries(date_list, value_list, factorseries_mode,
                                                  calendar=self._params_dict['calendar'])
                                     for value_list in fund_matrix_transpose]
                talib_indicatorseries_list = [Factorseries(date_list, value_list, 'backward_talib',
                                                     period_list=self._params_dict['period_list'])
                                              for value_list in index_matrix_transpose]
            macro_indicatorseries_list = [Factorseries(date_list, value_list, 'original')
                                          for value_list in macro_matrix_transpose]
            self._logging("Building Factorseries complete.")
        except:
            Logger().error(module='model', file='datastack.py', content=traceback.format_exc())

        def stacking_up(factorseries_list):
            factors_date_set = None
            for factorseries in factorseries_list:
                if factors_date_set is None:
                    factors_date_set = set(factorseries.date_list)
                else:
                    factors_date_set &= set(factorseries.date_list)

            factors_date_list = sorted(factors_date_set)
            factors_value_list = [[] for i in range(len(factors_date_set))]

            for factorseries in factorseries_list:
                idx = 0
                for i, date_factors in enumerate(list(zip(factorseries.date_list,
                                                          factorseries.factors_list))):
                    date, factors = date_factors
                    # piling up all factors into one vector for each day
                    if date in factors_date_set:
                        factors_value_list[idx] += factors
                        idx += 1
            return factors_date_list, factors_value_list

        self._logging("Doing stacking(piling up) factorseries.")
        self._target_date_list, \
        self._target_value_matrix = stacking_up(targetseries_list)
        self._talib_indicator_date_list, \
        self._talib_indicator_value_matrix = stacking_up(talib_indicatorseries_list)
        self._macro_indicator_date_list, \
        self._macro_indicator_value_matrix = stacking_up(macro_indicatorseries_list)
        self._logging("Stacking(piling up) factorseries complete.")

    @property
    def target_date_list(self):
        return self._target_date_list

    @property
    def target_value_matrix(self):
        return self._target_value_matrix

    @property
    def talib_indicator_date_list(self):
        return self._talib_indicator_date_list

    @property
    def talib_indicator_value_matrix(self):
        return self._talib_indicator_value_matrix

    @property
    def macro_indicator_date_list(self):
        return self._macro_indicator_date_list

    @property
    def macro_indicator_value_matrix(self):
        return self._macro_indicator_value_matrix







