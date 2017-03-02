
"""
testmultdatagate
"""

from modeldata import *
import numpy as np
from util import Logger
from datetime import datetime
from datagate import (CSVLoader,
                      DataHandler,
                      DataGate,
                      TripleGate)
logger = Logger('./log', 'DEBUG')

datahandler = DataHandler(CSVLoader('../../expdata/fund.csv'),
                          datetime(2011, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
logger.info(module='datagate',
            file='usetriplegate.py',
            content="the num of valid symbols in the date range is %d." % len(symbol_list))
fund_dg = DataGate(datahandler, symbol_list[0:2])

datahandler = DataHandler(CSVLoader('../../expdata/index.csv'),
                          datetime(2011, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
logger.info(module='datagate',
            file='usetriplegate.py',
            content="the num of valid symbols in the date range is %d." % len(symbol_list))
index_dg = DataGate(datahandler, symbol_list[0:2])

datahandler = DataHandler(CSVLoader('../../expdata/macro.csv'),
                          datetime(2011, 1, 1),
                          datetime(2015, 12, 31))
symbol_list = datahandler.symbol_list
logger.info(module='datagate',
            file='usetriplegate.py',
            content="the num of valid symobls in the date range is %d." % len(symbol_list))
macro_dg = DataGate(datahandler, symbol_list[0:2])

triple_dg = TripleGate(fund_dg, index_dg, macro_dg)
triple_dg.dump_to_file('data.pickle')

num = 0
for v in triple_dg:
    # print v
    num += 1
    if num > 100:
        break

triple_dg_recover = TripleGate(None, None, None, 'data.pickle')

num = 0
for v in triple_dg_recover:
    print v
    num += 1
    if num > 100:
        break
