
from account import Account
from datetime import timedelta, datetime

acct = Account('test')

thisdate = datetime.today()
def get_next_date():
    global thisdate
    thisdate += timedelta(days=1)
    return thisdate

acct.update_nav(1)
acct.buy(5)
acct.buy(2)
print acct.market_value
print acct.surplus_value
print ""
acct.update_nav(1.2)
print acct.market_value
print acct.surplus_value
print ""
acct.sell(5)
print acct.market_value
print acct.surplus_value
print ""
acct.extract_surplus()
print acct.market_value
print acct.surplus_value
print ""
acct.update_nav(1.5)
print acct.market_value
print acct.surplus_value
print ""
acct.update_nav(1.7)
print acct.market_value
print acct.surplus_value
print ""






