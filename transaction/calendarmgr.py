
"""
CalendarMgr
==============================
Trading and Fitting management.
"""
from calendar import monthrange
from datetime import datetime, timedelta

class CalendarMgr:
    def __init__(self, start_date, end_date, invest_mode):
        """
        :param start_date: the start date
        :param end_date: the end date
        :param invest_mode: 'month', 'week', 'year'
        """
        self._start_date = start_date
        self._end_date = end_date

        # the investing day
        self._invest_mode = invest_mode
        self._trading_date_list = []
        self._trading_date_set = None
        self._init_trading_date()
        self._trading_idx = 0
        self._mving_idx = 0

    def _init_trading_date(self):
        now, end = self._start_date, self._end_date
        while now < end:
            self._trading_date_list.append(now)
            y, m, d = now.year, now.month, now.day

            if self._invest_mode == 'month':
                yn, mn, dn = y, m + 1, self._start_date.day
                if mn == 13:
                    mn = 1
                    yn += 1
                monthdays = monthrange(yn, mn)[1]
                if monthdays < dn:
                    dn = monthdays
                date_next = datetime(yn, mn, dn)

            elif self._invest_mode == 'week':
                yn, mn, dn = y, m, d + 7
                monthdays = monthrange(yn, mn)[1]
                if monthdays < dn:
                    mn += 1
                    dn -= monthdays
                    if mn == 13:
                        mn = 1
                        yn += 1
                date_next = datetime(yn, mn, dn)

            elif self._invest_mode == 'year':
                yn, mn, dn = y + 1, m, d
                date_next = datetime(yn, mn, dn)

            while True:
                if date_next.weekday() < 5:
                    break
                else:
                    if date_next.day < 5:
                        if (date_next + timedelta(days=1)).weekday() < 5:
                            date_next += timedelta(days=1)
                        elif (date_next + timedelta(days=2)).weekday() < 5:
                            date_next += timedelta(days=2)
                    else:
                        if (date_next - timedelta(days=1)).weekday() < 5:
                            date_next -= timedelta(days=1)
                        elif (date_next - timedelta(days=2)).weekday() < 5:
                            date_next -= timedelta(days=2)
            now = date_next
        self._trading_date_set = set(self._trading_date_list)

    def trading_or_not(self, date):
        if self._start_date <= date <= self._end_date and \
            self._trading_idx < len(self._trading_date_list) and \
                date >= self._trading_date_list[self._trading_idx]:
            self._trading_idx += 1
            return True
        return False

    @property
    def trading_date_list(self):
        return self._trading_date_list

    @property
    def trading_date_list_len(self):
        return len(self._trading_date_list)

if __name__ == '__main__':
    start = datetime(2013, 1, 4)
    end = datetime(2014, 12, 31)
    calender_mgr = CalendarMgr(start, end, 'year')
    for i in range(500):
        this_date = start + timedelta(days=i)
        print this_date, calender_mgr.trading_or_not(this_date)
