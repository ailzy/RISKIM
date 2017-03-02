
from account import MultAccount
from datetime import datetime, timedelta

thisdate = datetime.today()
def get_next_date():
    global thisdate
    thisdate += timedelta(days=1)
    return thisdate

multacct = MultAccount(['A', 'B', 'C', 'D', 'E'])

multacct.update_datenav(get_next_date(), [1, 1, 1, 1, 1])
multacct.update_allocation([0.5, 0.5, 0, 0, 0])
print ""

multacct.update_datenav(get_next_date(), [1.3, 0.8, 0.9, 1.2, 1.1])
multacct.update_allocation([0, 0, 0.3, 0.6, 0.1])
print ""

multacct.update_datenav(get_next_date(), [1.5, 0.6, 0.7, 0.9, 1.2])
multacct.update_allocation([0, 0, 0.3, 0.6, 0.1])
print ""

multacct.update_datenav(get_next_date(), [1.9, 0.8, 0.6, 0.97, 1.1])
multacct.update_allocation([0.5, 0.5, 0, 0, 0])
print ""

multacct.update_datenav(get_next_date(), [2.4, 1.2, 1.3, 1.8, 1.9])
multacct.update_allocation([0, 0, 0.3, 0.6, 0.1])
print ""

multacct.update_datenav(get_next_date(), [2.5, 1,2, 1.4, 1.9, 2.0])

print "STOP MULT-ACCOUNT, SELL ALL FUNDS."
multacct.stop()
print "FINAL CUMULATIVE RETURN RATE IS %.5f" % \
      multacct.final_cumret