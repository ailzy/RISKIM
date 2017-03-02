
"""
Baseseries
====================================
A series manager class (baseseries).
"""

class Baseseries(object):
    def __init__(self, symbol, date_list, value_list,
                 valid=True):
        """
        Fund stores daily nav values for each fund.
        :param symbol:
        """
        assert (len(date_list) == len(value_list))
        self._symbol = symbol
        self._date_list = date_list
        self._value_list = value_list
        self._valid = valid

    @property
    def symbol(self):
        return self._symbol

    @property
    def start_date(self):
        return self._date_list[0] if self.valid else None

    @property
    def end_date(self):
        return self._date_list[-1] if self.valid else None

    @property
    def length(self):
        return len(self._date_list)

    @property
    def valid(self):
        return True if self.length > 0 and self._valid \
            else False

    @property
    def date_list(self):
        return self._date_list

    @property
    def value_list(self):
        return self._value_list

    def generator(self, filter_date_list=None):
        """
        generating date, value stream. when date_list
        is not None, outputting only existed days.
        :param date_list:
        :return:
        """
        idx = 0
        lnn = len(filter_date_list) if filter_date_list else 0
        for i in range(self.length):
            if lnn > 0 and idx >= lnn:
                break
            date = self.date_list[i]
            if lnn > 0 and idx < lnn and filter_date_list[idx] < date:
                for j in range(idx, lnn):
                    if filter_date_list[j] >= date:
                        idx = j
                        break
            if lnn == 0 or filter_date_list[idx] == date:
                yield date, self.value_list[i]
                idx += 1
