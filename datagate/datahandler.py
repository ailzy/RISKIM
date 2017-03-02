
from csvloader import CSVLoader
from baseseries import Baseseries

class DataHandler:
    def __init__(self, csvloader, start_date, end_date):
        self._csvloader = csvloader
        self._start_date = start_date
        self._end_date = end_date
        self._baseseries_list = []
        self._build()

    def _build(self):
        # construct baseseries object list in a temporary datastruct
        baseseries_list_temp = []
        for symbol in self._csvloader.symbol_list:
            baseseries = self._csvloader.get_baseseries_by_symbol(symbol)
            assert (isinstance(baseseries, Baseseries))
            if not baseseries.valid or baseseries.length == 0:
                continue
            if self._start_date >= baseseries.start_date and \
                self._end_date <= baseseries.end_date:
                baseseries_list_temp.append(baseseries)

        # if all of the series in csvloader are invalid, then return
        if not baseseries_list_temp:
            return

        # construct a new baseseries list with valid date list.
        self._common_date_list, self._symbol_list = [], []
        for baseseries in baseseries_list_temp:
            date_list = baseseries.date_list
            value_list = baseseries.value_list

            # line search for finding start and end date's indexing in the list
            start_idx, end_idx = 0, 0
            for idx, date in enumerate(date_list):
                if date >= self._start_date:
                    start_idx = idx
                    break

            for idx, date in enumerate(date_list[start_idx:]):
                if date <= self._end_date:
                    end_idx = idx + start_idx

            # store the valid date list to common_date_list
            if not self._common_date_list:
                self._common_date_list = date_list[start_idx:end_idx+1]

            self._baseseries_list.append(
                Baseseries(baseseries.symbol,
                           date_list[start_idx:end_idx+1],
                           value_list[start_idx:end_idx+1])
            )
            self._symbol_list.append(baseseries.symbol)

    @property
    def date_list(self):
        return self._common_date_list

    @property
    def symbol_list(self):
        return self._symbol_list

    @property
    def baseseries_list(self):
        return self._baseseries_list

