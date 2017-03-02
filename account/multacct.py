"""
MultAccount
"""
from singleacct import Account
from util import Logger

class MultAccount:
    def __init__(self, name, id_list):
        """
        :param id_list: string id list
        """
        self._name = name
        self._date_list = []
        self._account_list = []
        self._len = len(id_list)
        for id in id_list:
            self._account_list.append(Account(id))
        self._id_list = id_list

        self._nav_tail = -1
        self._pos_maxval = 0
        self._pos_dd = 0

        self._sum_investment = 0
        self._mult_account_weight_list = [1.0 / self._len] \
                                         * self._len
        self._market_value = 0
        self._pos_list = []
        self._cum_ret_list = []

        self._final_cum_ret = None

        self._invest_start = False
        self._logger = Logger()

    @property
    def name(self):
        return self._name

    @property
    def account_list(self):
        return self._account_list

    @property
    def account_num(self):
        return self._len

    def __iter__(self):
        for accout in self._account_list:
            yield  accout

    def find_maxdown(cls, pos_val, pos_maxval, mdd):
        down_val = pos_maxval - pos_val
        dd = down_val / (pos_maxval + 1e-10)
        if down_val < 0:
            pos_maxval = pos_val
        elif dd > mdd:
            mdd = dd
        return pos_maxval, mdd

    def update_datenav(self, date, nav_list):
        market_value_sum = 0
        # obtain all accounts' remaining weight
        market_value_list = []
        for account, nav in list(zip(self._account_list,
                                     nav_list)):
            account.update_nav(nav)
            market_value_sum += account.market_value
            market_value_list.append(account.market_value)

        if market_value_sum > 0:
            self._mult_account_weight_list = [v / market_value_sum
                                              for v in market_value_list]
        self._market_value = market_value_sum

        self._logger.debug(module='account',
                           file='multacct.py',
                           content=" " * 4 + "multi accounts, market value now is %.5f." % market_value_sum)

        self._date_list.append(date)
        self._pos_list.append(market_value_sum)

        self._pos_maxval, self._pos_dd = \
            self.find_maxdown(market_value_sum,
                              self._pos_maxval,
                              self._pos_dd)

        self._cum_ret_list.append(self.cum_ret)

        self._logger.debug(module='account',
                           file='multacct.py',
                           content=" " * 4 + "return rate %s." % str(self.cum_ret))

    def update_allocation(self, weight_list):
        if 0.995 < sum(weight_list) < 1.005:
            pass
        else:
            self._logger.debug(module='account',
                               file='multacct.py',
                               content="" * 4 + "weights sum not equal to 1 is not allowed.")
            return
        practical_invest = 0
        market_value_sum = 0
        if self._invest_start:
            pos_tail = self._pos_list[-1]
            for account, weight in list(zip(self._account_list,
                                            weight_list)):
                assert (isinstance(account, Account))
                single_invest = weight * (pos_tail if pos_tail > 0 else 1)
                adjust_invest  =  single_invest - account.market_value

                if abs(adjust_invest) / (account.market_value + 1e-10) > 0.01:
                    if adjust_invest > 0:
                        practical_invest += adjust_invest
                        account.buy(adjust_invest)
                    elif adjust_invest < 0:
                        account.sell(abs(adjust_invest))
                        practical_invest -= account.surplus_value
                        account.extract_surplus()
                market_value_sum += account.market_value
        else:
            for account, weight in list(zip(self._account_list,
                                            weight_list)):
                practical_invest += weight
                account.buy(weight)
                market_value_sum += account.market_value
            self._invest_start = True

        self._sum_investment += practical_invest
        self._market_value = market_value_sum

        self._logger.debug(module='account',
                           file='multacct.py',
                           content=" " * 4 + "this transaction cost extra invest %.5f." % practical_invest)
        self._logger.debug(module='account',
                           file='multacct.py',
                           content=" " * 4 + "cumulative investment is %.5f." % self._sum_investment)
        self._logger.debug(module='account',
                           file='multacct.py',
                           content=" " * 4 + "multi accounts, market value after transaction is %.5f." % market_value_sum)

    def stop(self):
        return_value_sum = 0
        for account in self._account_list:
            account.sell(account.market_value)
            return_value_sum += account.extract_surplus()
        self._final_cum_ret = (return_value_sum - self._sum_investment) / \
                              self._sum_investment

    def logging(self):
        self._logger.info(module='account', file='multacct.py',
                          content={'backtest_time': str(self._date_list[-1]),
                                   'account_name': self._name,
                                   'content': 'return rate is %.4f' % self.cum_ret})

    @property
    def cum_ret(self):
        if self._final_cum_ret:
            return self._final_cum_ret
        else:
            return (self._market_value - self._sum_investment) / \
                   (self._sum_investment + 1e-10)

    @property
    def cum_ret_avg(self):
        return sum(self._cum_ret_list) / len(self._cum_ret_list)

    @property
    def cum_ret_list(self):
        return self._cum_ret_list

    @property
    def pos_list(self):
        return self._pos_list

    @property
    def mult_account_weight_list(self):
        return self._mult_account_weight_list

    @property
    def investment_sum(self):
        return self._sum_investment

    @property
    def return_value(self):
        return  self.investment_sum * self.cum_ret

    @property
    def pos_dd(self):
        return self._pos_dd