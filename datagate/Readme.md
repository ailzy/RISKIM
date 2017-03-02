## datagate
    In backtesting, this module plays a role as a simulator for data streaming input.
    Both single time series and multiple time series supported.

## example
    test/testdatagate.py

## usage
    (1) Init A CSVLoader Object
        input_file = '../data/test/index/stage6/common_index.csv'
        csvloader = CSVLoader(input_file)

        This class will build an object storing each symbol's data into a baseseries object.

    (2) Construct A DataHandler Object
        datahandler = DataHandler(csvloader,
                                  datetime(2013, 1, 1),
                                  datetime(2013, 12, 31))

        DataHandler provides a method for pipelining csvloader's series into an array of generators.

    (3) Construct DataGate Object
        datagenerator = DataGate(datahandler, symbol_list[0:10])

        Temporarily, DataGate serves only as a wrapper for getting a sub-collection generators from datahandler.

## scalability

## some warnings
    Be aware of that, we use 0 value representing the series has not started yet. So, we dont
    allow 0 value appearing in the middle of a series.
