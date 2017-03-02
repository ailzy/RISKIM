
import pickle
from util import Logger
from datagate import DataGate
from datahandler import DataHandler

class TripleGate:
    def __init__(self,
                 fund_datagate=None,
                 index_datagate=None,
                 macro_datagate=None,
                 dumpped_file=None):
        self._fund_datagate = fund_datagate
        self._index_datagate = index_datagate
        self._macro_datagate = macro_datagate
        self._dumpped_file = dumpped_file
        self._logger = Logger()
        assert (self._fund_datagate or dumpped_file)
        self._callback_data_list = pickle.load(open(dumpped_file, 'rb')) \
            if dumpped_file else []

    def _fund_datagate_generator(self):
        for date, value_list in self._fund_datagate:
            yield date, value_list

    def _index_datagate_generator(self):
        for date, value_list in self._index_datagate:
            yield date, value_list

    def _macro_datagate_generator(self):
        for date, value_list in self._macro_datagate:
            yield date, value_list

    def _combinatiional_generator(self):
        last_index_date, last_index_value_list, \
        index_date, index_value_list, \
        last_macro_date, last_macro_value_list, \
        macro_date, macro_value_list = [None] * 8
        fund_generator = self._fund_datagate_generator()
        index_generator = self._index_datagate_generator()
        macro_generator = self._macro_datagate_generator()
        try:
            for date, fund_value_list in fund_generator:
                while not index_date or index_date <= date:
                    last_index_date, last_index_value_list = index_date, index_value_list
                    index_date, index_value_list = next(index_generator)
                while not macro_date or macro_date <= date:
                    last_macro_date, last_macro_value_list = macro_date, macro_value_list
                    macro_date, macro_value_list = next(macro_generator)
                if date and last_index_date and last_macro_date:
                    yield {'fund': {'date': date, 'value_list': fund_value_list}, \
                           'index': {'date': last_index_date, 'value_list': last_index_value_list}, \
                           'macro': {'date': last_macro_date, 'value_list': last_macro_value_list}}
        except StopIteration:
            self._logger.warning(module='datagate',
                              file='triplegate.py',
                              content="data iteration stopped.")

    def _build(self):
        if not self._callback_data_list:
            for data_dict in self._combinatiional_generator():
                self._callback_data_list.append([data_dict['fund']['date'],
                                           data_dict['fund']['value_list'],
                                           data_dict['index']['date'],
                                           data_dict['index']['value_list'],
                                           data_dict['macro']['date'],
                                           data_dict['macro']['value_list']])

    def dump_to_file(self, file_path):
        self._build()
        with open(file_path, 'wb') as f:
            pickle.dump(self._callback_data_list, f)

    def __iter__(self):
        self._build()
        for data_list in self._callback_data_list:
            yield data_list
