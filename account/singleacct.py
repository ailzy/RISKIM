"""
Account
"""
from util import Logger

class BasicAccount:
    def __init__(self, id):
        """
        :param id:
        :param sub_discount:
        :param red_discount:
        """
        self._account_id = id
        self._volume = 0


class Account:
    def __init__(self, id,
                 sub_discount=0.0015,
                 red_discount=0.005):
        self._id = id
        self._nav = 1
        self._volume = 0
        self._market_value = 0
        self._surplus_value = 0
        self._sub_discount = sub_discount
        self._red_discount = red_discount
        self._logger = Logger()

    @property
    def volume(self):
        return self._volume

    @property
    def market_value(self):
        return self._market_value

    @property
    def surplus_value(self):
        return self._surplus_value

    def _update_market_value(self):
        self._market_value = self._volume * self._nav

    def update_nav(self, nav):
        self._logger.debug(module='account',
                           file='singleacct.py',
                           content="----" * 2 + "account %s, org market value is %.5f" % (self._id,
                                                                                          self._market_value))
        self._nav = nav
        self._update_market_value()
        self._logger.debug(module='account',
                           file='singleacct.py',
                           content="----" * 3 + "account %s, now market value is %.5f" % (self._id,
                                                                                          self._market_value))

    def buy(self, weight):
        self._logger.debug(module='account',
                           file='singleacct.py',
                           content="----" * 1 + "account %s, buy weight %.5f, cut off %.5f" %
                                                (self._id, weight, weight * self._sub_discount))
        weight *= 1 - self._sub_discount
        volume = weight / self._nav
        self._volume += volume
        self._update_market_value()

    def sell(self, weight):
        self._logger.debug(module='account',
                           file='singleacct.py',
                           content="----" * 1 + "account %s, sell weight %.5f, cut off %.5f" %
                                                (self._id, weight, weight * self._red_discount))
        volume = weight / self._nav
        self._volume -= volume
        self._update_market_value()
        self._surplus_value += \
            volume * self._nav * (1 - self._red_discount)

    def extract_surplus(self):
        surplus_value = self._surplus_value
        self._surplus_value = 0
        return surplus_value
