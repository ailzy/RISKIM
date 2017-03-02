"""
DataLoader
================
Loading CSV Data
"""
import pandas as pd
from util import Logger
from datetime import datetime
from calendar import monthrange
from baseseries import Baseseries

class CSVLoader:
    def __init__(self, file_path):
        """
        CSVLoader loads fund's nav or index's value from a csv file.
        :param file_path:
        """
        self._file_path = file_path
        self._symbol2data = dict()
        self._symbol2status = dict()
        self._logger = Logger()
        self._read()

    def _read(self):
        """
        read csv file.
        :return:
        """
        pd_frame = pd.read_csv(
            self._file_path, index_col=0, low_memory=False)
        column_name_list = list(pd_frame.columns)
        for symbol in column_name_list:
            date_list, value_list = [], []
            data_list = pd_frame[symbol]
            valid_flag = False
            for i, value in enumerate(data_list):
                if type(value) == type(''):
                    num = 0
                    for v in value.split(','):
                        num *= 1000
                        num += float(v)
                    value = num
                if value != 0:
                    valid_flag = True
                    date_list.append(
                        CSVLoader.trans2datetime(pd_frame.index[i]))
                    value_list.append(value)
                if valid_flag and value == 0:
                    self._logger.warning(module='datagate',
                                         file='csvloader.py',
                                         content="zero value appears in the middle of the series is not allowed.")
                    valid_flag = False
            self._symbol2data[symbol] = Baseseries(symbol, date_list, value_list, valid_flag)

    @classmethod
    def trans2datetime(cls, stramp):
        if type(stramp) != type(''):
            return stramp
        splitter = '-'
        if '/' in stramp:
            splitter = '/'
        ymd_list = stramp.split(splitter)
        dt = None
        if len(ymd_list) == 3:
            y, m, d = int(ymd_list[0]), int(ymd_list[1]), int(ymd_list[2])
            dt = datetime(y, m, d)
        elif len(ymd_list) == 2:
            y, m = int(ymd_list[0]), int(ymd_list[1])
            dt = datetime(y, m, monthrange(y, m)[1])
        return dt

    def get_baseseries_by_symbol(self, symbol):
        if symbol in self._symbol2data:
            return self._symbol2data[symbol]
        return None

    @property
    def symbol_list(self):
        return self._symbol2data.keys()

if __name__ == '__main__':
    data_loader = CSVLoader('../expdata/dynamic/fund.csv')
    baseseries = data_loader.get_baseseries_by_symbol('510070.SH')
    assert (isinstance(baseseries, Baseseries))
    for date, value in baseseries.generator():
        print date, value