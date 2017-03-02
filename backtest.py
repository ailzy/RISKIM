"""
Back Testing Simulation
=================================================
This script loads config and backtest strategy on
an input nav fund stream.
"""
import warnings, sys
import numpy as np
from modeldata import *
from util import Logger
from datetime import datetime
from portfolio import Portfolio
from util import ConfigLoader, init_dir
from account import MultAccount, Account
from transaction import ModelMgr, CalendarMgr
from datagate import CSVLoader, DataHandler, \
    DataGate, TripleGate

warnings.filterwarnings("ignore")

# Preparation
config_loader = ConfigLoader('backtest.ini')
# Init log system
logger_handler = Logger('./bk.log', config_loader.system.log_level)
logging = lambda content: logger_handler.info(
    module='backtest', file='backtest.py', content=content)
# File paths
fund_file_path = config_loader.system.fund_path
index_file_path = config_loader.system.index_path
macro_file_path = config_loader.system.macro_path
output_dir_path = config_loader.system.output_path
invest_cycle = config_loader.experiment.invest_cycle
# Model params
g_start, g_end = config_loader.experiment.general_start_end
b_start, b_end = config_loader.experiment.backtest_start_end
talib_period = config_loader.model.talib_period
lookback_window_list = config_loader.gridsearch.lookback_window_list
risk_thres_list = config_loader.gridsearch.risk_thres_list
adjust_thres_list = config_loader.gridsearch.adjust_thres_list
# Grid params list
grid_params_list = [(lw, risk_thres, ad_thres)
                    for lw in lookback_window_list
                    for risk_thres in risk_thres_list
                    for ad_thres in adjust_thres_list]

# First step: construct DataAlign object
datahandler = DataHandler(CSVLoader(fund_file_path), g_start, g_end)
fund_symbol_list = datahandler.symbol_list[0:5]
logging("the num of valid symbols in the date range is %d." % len(fund_symbol_list))
fund_dg = DataGate(datahandler, fund_symbol_list)
fund_num = len(fund_symbol_list)

datahandler = DataHandler(CSVLoader(index_file_path), g_start, g_end)
index_symbol_list = datahandler.symbol_list
logging("the num of valid symbols in the date range is %d." % len(index_symbol_list))
index_dg = DataGate(datahandler, index_symbol_list)

datahandler = DataHandler(CSVLoader(macro_file_path), g_start, g_end)
macro_symbol_list = datahandler.symbol_list
logging("the num of valid symobls in the date range is %d." % len(macro_symbol_list))
macro_dg = DataGate(datahandler, macro_symbol_list)

# Second step: construct TripleGate object
# Macro data are replaced by fund
triple_dg = TripleGate(fund_dg, index_dg, fund_dg)
datacache = DataCache()
calendarmgr = CalendarMgr(b_start, b_end, invest_cycle)
fund_date = None
trading_start = False
oneshot_once_start = True

def portfolio_selection(last_weight_list,
                        fund_num,
                        return_ret,
                        riskcov_lr,
                        adjust_thres,
                        risk_thres):
    try:
        new_weight_list = Portfolio(last_weight_list,
                                    fund_num,
                                    return_ret,
                                    riskcov_lr,
                                    adjust_thres,
                                    risk_thres).asset_weight
    except:
        logger_handler.warning(module='backtest',
                               file='backtest.py',
                               content="Portfolio optimization for params %s failed, allocation not changed.")
        new_weight_list = last_weight_list
    return new_weight_list

last_date = None
asset_weight_equal = [1.0 / fund_num] * fund_num

logging_local = lambda content, notation: \
    logging({'backtest_time': str(fund_date),
             'notation': notation, 'content': content})

logging_local("Backtest begins, init all accounts.", "trace")
macct_dynamic_list = [MultAccount('dynamic %s' % str(params), fund_symbol_list)
                      for params in grid_params_list]
macct_dyaction = MultAccount('dyaction', fund_symbol_list)
macct_constant = MultAccount('constant', fund_symbol_list)
macct_oneshot = MultAccount('oneshot', fund_symbol_list)

for fund_date, fund_value_list, _, \
    index_value_list, _, macro_value_list in triple_dg:
    datacache.update_data(fund_date,
                          fund_value_list,
                          index_value_list,
                          macro_value_list)

    logging_local("Backtesting date is %s." % str(fund_date), "trace")

    transaction_flag = False
    if calendarmgr.trading_or_not(fund_date):
        logging_local("The date is a trading day.", "trace")
        transaction_flag = True
        trading_start = True

    if trading_start:
        logging_local("Update net values for each account.", "trace")
        for account in macct_dynamic_list:
            account.update_datenav(fund_date, fund_value_list)
        macct_dyaction.update_datenav(fund_date, fund_value_list)
        macct_oneshot.update_datenav(fund_date, fund_value_list)
        macct_constant.update_datenav(fund_date, fund_value_list)

    if transaction_flag:
        lw2model = dict()
        logging_local("Models fitting begin.", "trace")
        for lw in lookback_window_list:
            logging_local("Doing model fitting for look back window %s." % lw, "trace")
            modelmgr = ModelMgr(fund_date, datacache,
                                lookback_window=lw,
                                talib_period=talib_period)
            modelmgr.build()
            lw2model[lw] = modelmgr
        logging_local("Models fitting complete.", "trace")

        logging_local("Updating assets allocation in multiple accounts begin.", "trace")
        # Sort the return rate and obtain the optimal
        optimal_param = sorted(list(zip(grid_params_list,
                                        macct_dynamic_list)),
                               cmp=lambda x, y: cmp(x[1].cum_ret, y[1].cum_ret))[-1][0]

        for params, macct in list(zip(grid_params_list + [optimal_param],
                                      macct_dynamic_list + [macct_dyaction])):
            macct.logging()
            lookback_window, risk_thres, adjust_thres = params
            modelmgr = lw2model[lookback_window]
            return_ret = modelmgr.ret
            riskcov_lr = modelmgr.riskcov_lr
            last_weight_list = macct.mult_account_weight_list
            new_weight_list = portfolio_selection(last_weight_list,
                                                  fund_num,
                                                  return_ret,
                                                  riskcov_lr,
                                                  adjust_thres,
                                                  risk_thres)
            macct.update_allocation(new_weight_list)

        macct_constant.logging()
        macct_constant.update_allocation(asset_weight_equal)
        macct_oneshot.logging()
        if oneshot_once_start:
            macct_oneshot.update_allocation(asset_weight_equal)
            oneshot_once_start = False
        logging_local("Updating assets allocation in multiple accounts complete.", "trace")

logging_local("Backtest end. Now withdraw all accounts.", "trace")
for account in macct_dynamic_list + [macct_dyaction,
                                     macct_constant,
                                     macct_oneshot]:
    account.stop()
    account.logging()
logging_local("All accounts stopped.", "trace")

