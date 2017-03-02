
"""
testdatagate
"""

import numpy as np
from datetime import datetime
from datagate import (DataHandler,
                      CSVLoader,
                      DataGate)

input_file = '../../expdata/index.csv'
print "now we test extracting indexes from file: %s." % input_file

csvloader = CSVLoader(input_file)
datahandler = DataHandler(csvloader,
                          datetime(2013, 1, 1),
                          datetime(2013, 12, 31))

symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)

print "show the first 10 days of the first 1 symbols below: %s." % str(symbol_list[0:2])
datagenerator = DataGate(datahandler, symbol_list[0:10])

num = 0
for date, value_list in datagenerator:
    print date, value_list
    num += 1
    if num == 10:
        break

input_file = '../../expdata/macro.csv'
print "now we test extracting macrodata from file: %s." % input_file

csvloader = CSVLoader(input_file)
datahandler = DataHandler(csvloader,
                          datetime(2013, 1, 1),
                          datetime(2013, 12, 31))

symbol_list = datahandler.symbol_list
print "the num of valid symbols in the date range is %d." % len(symbol_list)

print "show the first 10 days of the first 1 symbols below: %s." % str(symbol_list[0:2])
datagenerator = DataGate(datahandler, symbol_list[0:10])

num = 0
for date, value_list in datagenerator:
    print date, value_list
    num += 1
    if num == 10:
        break
