"""
Factorseries
"""
import math
import numpy as np
from datagate import Baseseries
from calendar import monthrange
from util import Logger
from datetime import timedelta, datetime
from techanalysis import TechnicalFactors

class Factorseries:
    def __init__(self, date_list, series_list, mode, calendar='month',
                 period_list=[10]):
        """
        transform time series into target series
        :param date_list: datetime
        :param nav_list: nav value for each day
        :param mode:
        :param calendar: 'month' or 'week' or 'season'
        """
        self._date_list = date_list
        self._series_list = series_list
        self._mode = mode
        self._calendar = calendar
        self._logger = Logger()

        if len(self._series_list) < 30:
            self._logger.warning(module='modeldata',
                                 file='factorutil.py',
                                 content="the num of value list in factorseries is less than 30, build series failed")
            return
        
        if self._mode == 'original':
            pass
        else:
            self._date2navidx = dict()
            for i, date in enumerate(date_list):
                self._date2navidx[date] = i
            self._target_list = []

            self._basic_value_ratio_list = []
            for idx in range(len(self._series_list) - 1):
                self._basic_value_ratio_list.append(self._series_list[idx + 1] /
                                        self._series_list[idx])

        if self._mode == 'backward_ratio':
            self._backward_ratio_list = self._basic_value_ratio_list
            # adjust date list, remove the heading day, thus
            # we obtain looking backward nav list
            self._series_list = self._series_list[1:]
            self._date_list = self._date_list[1:]

        elif self._mode == 'forward_ratio':
            self._forward_ratio_list = self._basic_value_ratio_list
            self._series_list = self._series_list[:-1]
            self._date_list = self._date_list[:-1]

        elif 'forward_ret' in self._mode:
            self._series_list = self._series_list[:-1]
            self._date_list = self._date_list[:-1]

            # this maps each date to its ending date.
            self._date_later_map = dict()

            start_date, end_date = self._date_list[0], \
                                   self._date_list[-1]

            for idx in range(len(self._date_list)):
                date_now = self._date_list[idx]
                date_target = None
                if self._calendar == 'week':
                    date_target = date_now + timedelta(days=7)
                elif self._calendar == 'month':
                    y, m, d = date_now.year, \
                              date_now.month, \
                              date_now.day
                    start_year = y
                    start_month = m + 1
                    if m + 1 == 13:
                        start_year += 1
                        start_month = 1
                    date_target = date_now + timedelta(days=monthrange(
                        start_year, start_month)[1])
                elif self._calendar == 'quarter':
                    y, m, d = date_now.year, \
                              date_now.month, \
                              date_now.day
                    start_year = y
                    start_month = m + 1
                    date_target = date_now
                    for i in range(3):
                        if start_month == 13:
                            start_year += 1
                            start_month = 1
                        date_target = date_target + timedelta(days=monthrange(
                            start_year, start_month)[1])
                        start_month += 1
                if date_target > end_date:
                    continue

                self._date_later_map[date_now] = date_target

            # forward
            self._ret_mean_list = []
            self._ret_sum_list = []
            self._ret_std_list = []
            self._ret_sharpe_list = []

            self._logret_mean_list = []
            self._logret_std_list = []
            self._logret_sharpe_list = []

            # building a sharpe ratio predicting list
            date_lookingend_list = []

            lnn = 0

            for i in range(len(self._date_list)):
                date = self._date_list[i]
                if date not in self._date_later_map:
                    break
                date_ending = self._date_later_map[date]
                while True:
                    if date_ending in self._date2navidx:
                        break
                    else:
                        date_ending = date_ending - timedelta(days=1)
                idx_end = self._date2navidx[date_ending]

                if idx_end >= len(self._date_list):
                    break

                lnn += 1

                # storing the begining date and the ending date
                date_lookingend_list.append(date_ending)

                self._ret_mean_list.append(
                    np.mean(self._basic_value_ratio_list[i: idx_end + 1]) - 1
                )

                self._ret_sum_list.append(
                     self._series_list[idx_end] /
                     self._series_list[i] - 1
                )

                self._ret_std_list.append(
                    np.std(self._basic_value_ratio_list[i: idx_end + 1])
                )
                self._logret_mean_list.append(
                    np.mean([math.log10(x) for x in
                             self._basic_value_ratio_list[i: idx_end + 1]])
                )
                self._logret_std_list.append(
                    np.std([math.log10(x) for x in
                            self._basic_value_ratio_list[i: idx_end + 1]])
                )
                self._ret_sharpe_list.append(
                    self._ret_mean_list[-1] / (self._ret_std_list[-1] + 1e-10)
                )
                self._logret_sharpe_list.append(
                    self._logret_mean_list[-1] / (self._logret_std_list[-1] + 1e-10)
                )

            self._series_list = self._series_list[:lnn]
            self._date_list = self._date_list[:lnn]
            self._date_target_list = date_lookingend_list

        elif self._mode == 'backward_talib':
            self._talib_factors_list = TechnicalFactors(period_list)\
                .generate_factors_on_period_list(self._series_list)

            # dropping out heading invalid days in technical factors
            # generated by TA-Lib
            # filter out invalid numeric values
            valid_date_list = []
            valid_series_list = []
            valid_factors_list = []
            for i, talib_factors in enumerate(self._talib_factors_list):
                valid_flag = True
                for j, v in enumerate(talib_factors):
                    if math.isnan(v):
                        valid_flag = False
                        break
                if valid_flag:
                    valid_date_list.append(self._date_list[i])
                    valid_series_list.append(self._series_list[i])
                    valid_factors_list.append(talib_factors)

            self._org_date_list = self._date_list
            self._org_series_list = self._series_list
            self._date_list = valid_date_list
            self._series_list = valid_series_list
            self._talib_factors_list = valid_factors_list

        if self._mode == 'original':
            self._target_list = [[v] for v in self._series_list]
        elif self._mode == 'backward_ratio':
            # backward ratio list is the target list
            self._target_list = [[v] for v in self._backward_ratio_list]
        elif self._mode == 'forward_ratio':
            self._target_list = [[v] for v in self._forward_ratio_list]
        elif self._mode == 'forward_ret_mean':
            self._target_list = [[v] for v in self._ret_mean_list]
        elif self._mode == 'forward_ret_sum':
            self._target_list = [[v] for v in self._ret_sum_list]
        elif self._mode == 'forward_ret_sharpe':
            self._target_list = [[v] for v in self._logret_sharpe_list]
        elif self._mode == 'backward_talib':
            self._target_list = self._talib_factors_list

    @property
    def factors_list(self):
        return self._target_list

    @property
    def date_list(self):
        return self._date_list

    @property
    def series_list(self):
        return self._series_list
