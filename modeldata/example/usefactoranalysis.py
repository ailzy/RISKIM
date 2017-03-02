
import numpy as np
from datetime import datetime
from modeldata import Factorseries
from datagate import CSVLoader, DataHandler, DataGate

input_file = '../../expdata/test/nav/wande/nav1example.csv'
csvloader = CSVLoader(input_file)
datahandler = DataHandler(csvloader,
                          datetime(2013, 1, 1),
                          datetime(2013, 12, 31))

symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)

datagenerator = DataGate(datahandler, symbol_list[0:1])
date_list, series_list = [], []
num = 0
for date, value_list in datagenerator:
    date_list.append(date)
    series_list += value_list
    num += 1
    if num == 500:
        break

factorseries = Factorseries(date_list, series_list, 'backward_ratio')
assert (factorseries.factors_list[1] ==
        factorseries.series_list[1] / factorseries.series_list[0])
factorseries = Factorseries(date_list, series_list, 'forward_ratio')
assert (factorseries.factors_list[0] ==
        factorseries.series_list[1] / factorseries.series_list[0])
factorseries1 = Factorseries(date_list, series_list, 'forward_ret_mean')
factorseries2 = Factorseries(date_list, series_list, 'forward_ret_sharpe')
print factorseries1.factors_list
print factorseries2.factors_list
factorseries3 = Factorseries(date_list, series_list, 'backward_talib', period_list=[10, 20, 30])
print len(factorseries3.date_list)
print len(factorseries3.factors_list[0])
print np.array(factorseries3.factors_list).shape
