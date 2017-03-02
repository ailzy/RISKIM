
import os
import numpy as np
from modeldata import *
from datetime import datetime
from portfolio import Portfolio
from util import ConfigLoader
from transaction import ModelMgr, CalendarMgr
from datagate import CSVLoader, DataHandler, \
    DataGate, TripleGate

def abs_path(path):
    return os.path.join('../../', path)

config_loader = ConfigLoader(abs_path('backtest.ini'))
fund_file_path = abs_path(config_loader.system.fund_path)
index_file_path = abs_path(config_loader.system.index_path)
macro_file_path = abs_path(config_loader.system.macro_path)
invest_cycle = config_loader.experiment.invest_cycle
g_start, g_end = config_loader.experiment.general_start_end
b_start, b_end = config_loader.experiment.backtest_start_end

# First Step: Construct DataAlign Object
datahandler = DataHandler(CSVLoader(fund_file_path), g_start, g_end)
symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)
fund_dg = DataGate(datahandler, symbol_list[0:5])
fund_num = 5

datahandler = DataHandler(CSVLoader(index_file_path), g_start, g_end)
symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)
index_dg = DataGate(datahandler, symbol_list)

datahandler = DataHandler(CSVLoader(macro_file_path), g_start, g_end)
symbol_list = datahandler.symbol_list
print "the num of valid symobls in the date range is %d." % len(symbol_list)
macro_dg = DataGate(datahandler, symbol_list)

# Second Step: Construct TripleGate Object
triple_dg = TripleGate(fund_dg, index_dg, macro_dg)
datacache = DataCache()

fund_date = None
for fund_date, fund_value_list, _, \
    index_value_list, _, macro_value_list in triple_dg:
    datacache.update_data(fund_date,
                          fund_value_list,
                          index_value_list,
                          macro_value_list)

calendarmgr = CalendarMgr(b_start, b_end, invest_cycle)

modelmgr = ModelMgr(fund_date, datacache)
modelmgr.build()
print modelmgr.ret
print modelmgr.riskcov_ep
print modelmgr.riskcov_lr

asset_weight = Portfolio([1.0 / fund_num] * fund_num,
                         fund_num,
                         modelmgr.ret,
                         modelmgr.riskcov_lr,
                         adjust_thres=0.5,
                         risk_thres=1).asset_weight

print asset_weight
