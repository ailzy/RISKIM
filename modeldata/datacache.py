
"""
DataCache
====================================
A cache for collecting callback data
"""

class DataCache:
    def __init__(self):
        self._mode = None
        self._date_list = []
        self._fund_value_list_list = []
        self._index_value_list_list = []
        self._macro_value_list_list = []

    def update_data(self, date, fund_value_list,
                    index_value_list, macro_value_list):
        self._date_list += [date]
        self._fund_value_list_list += [fund_value_list]
        self._index_value_list_list += [index_value_list]
        self._macro_value_list_list += [macro_value_list]

    @property
    def date_list(self):
        return self._date_list

    def __len__(self):
        return len(self._date_list)

    @property
    def fund_matrix(self):
        ''' daily for each column
        :return:
        '''
        return self._fund_value_list_list

    @property
    def fund_matrix_transpose(self):
        ''' symbol for each column
        :return:
        '''
        return list(zip(*self._fund_value_list_list))

    @property
    def index_matrix(self):
        ''' daily for each column
        :return:
        '''
        return self._index_value_list_list

    @property
    def index_matrix_transpose(self):
        ''' symbol for each column
        :return:
        '''
        return list(zip(*self._index_value_list_list))

    @property
    def macro_matrix(self):
        ''' daily for each column
        :return:
        '''
        return self._macro_value_list_list

    @property
    def macro_matrix_transpose(self):
        ''' symbol for each column
        :return:
        '''
        return list(zip(*self._macro_value_list_list))

