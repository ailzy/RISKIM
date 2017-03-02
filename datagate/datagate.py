
from datahandler import DataHandler
from util import Logger

class DataGate:
    def __init__(self, datahandler, symbol_list=None):
        self._datahandler = datahandler
        self._selected_symbol_list = symbol_list
        self._symbol_list = []
        self._baseseries_list = datahandler.baseseries_list
        self._date_list = datahandler.date_list
        self._logger = Logger()

    def iterator(self):
        symbol_set = set(self._selected_symbol_list) \
            if self._selected_symbol_list else None
        baseseries_obj_list = []
        for baseseries_obj in self._baseseries_list:
            if not symbol_set or baseseries_obj.symbol in symbol_set:
                baseseries_obj_list.append(baseseries_obj)
                self._symbol_list.append(baseseries_obj.symbol)

        selected_generator_list = [baseseries_obj.generator()
                                   for baseseries_obj in baseseries_obj_list]

        for idx in range(len(self._date_list)):
            try:
                date, value_list = self._date_list[idx], []
                for symbol, series_generator in list(zip(self._selected_symbol_list,
                                                         selected_generator_list)):
                    this_date, value = next(series_generator)
                    assert (date == this_date)
                    value_list.append(value)
                yield [date, value_list]
            except StopIteration:
                self._logger.warning(module='datagate',
                                     file='datagate.py',
                                     content="daily values generation stopped.")
                break

    def __iter__(self):
        return self.iterator()

    @property
    def symbol_list(self):
        return self._symbol_list

