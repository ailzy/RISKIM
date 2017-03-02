
import numpy as np
from modeldata import *
from datetime import datetime
from datagate import CSVLoader, DataHandler, DataGate, TripleGate

# First Step: Construct DataAlign Object
datahandler = DataHandler(CSVLoader('../../expdata/test/nav/wande/index_fund.csv'),
                          datetime(2008, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)
fund_dg = DataGate(datahandler, symbol_list)

datahandler = DataHandler(CSVLoader('../../expdata/test/index/stage6/common_index.csv'),
                          datetime(2008, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)
index_dg = DataGate(datahandler, symbol_list)

datahandler = DataHandler(CSVLoader('../../expdata/choicedata/macrodata.csv'),
                          datetime(2008, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
print "the num of valid symobls in the date range is %d." % len(symbol_list)
macro_dg = DataGate(datahandler, symbol_list)

triple_dg = TripleGate(fund_dg, index_dg, macro_dg)

datacache = DataCache()

for fund_date, fund_value_list, _, \
    index_value_list, _, macro_value_list in triple_dg:
    datacache.update_data(fund_date,
                          fund_value_list,
                          index_value_list,
                          macro_value_list)

# datastack = DataStack(datacache, 'sharperatio_prediction')
datastack = DataStack(datacache, 'retmean_prediction')

print "date range of sharperatio prediction"
print "target value start at %s, end at %s." % \
      (datastack.target_date_list[0], datastack.target_date_list[-1])
print "talib indicator value start at %s, end at %s." % \
      (datastack.talib_indicator_date_list[0], datastack.talib_indicator_date_list[-1])
print "macro indicator value start at %s, end at %s." % \
      (datastack.macro_indicator_date_list[0], datastack.macro_indicator_date_list[-1])

dataalign = DataAlign(datastack)
print "alignment of the target and indicator values in sharperatio prediction."
print "target value start at %s, end at %s." % \
      (dataalign.date_list[0], dataalign.date_list[-1])

print "shape of Y matrix is %s" % str(np.array(dataalign.Y_matrix).shape)
print "shape of X matrix is %s" % str(np.array(dataalign.X_matrix).shape)

print "the remaining instances data, start at %s, end at %s." % \
      (dataalign.date_list_remain[0], dataalign.date_list_remain[-1])

print "the len of remaining instances is %s." % \
      str(len(dataalign.date_list_remain))
print "the len of remaining date list is %s." % \
      str(len(dataalign.X_matrix_remain))
