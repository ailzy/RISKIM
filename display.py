
"""
Backtest results display
"""

import sys, json, traceback
import pandas as pd
input_stream = sys.stdin

if __name__ == '__main__':
    ts2msgdic = dict()
    for line in input_stream:
        try:
            entry_dic = json.loads(line.rstrip('\n'))
            if entry_dic['level'] != 'INFO':
                continue
            content_dic = entry_dic['content']
            if content_dic['file'] != 'multacct.py':
                continue
            message_dic = content_dic['content']
            if type(message_dic) == dict:
                backtest_timestamp = message_dic['backtest_time']
                if backtest_timestamp in ts2msgdic:
                    ts2msgdic[backtest_timestamp].append(message_dic)
                else:
                    ts2msgdic[backtest_timestamp] = [message_dic]
        except:
            traceback.print_exc()

    ts2all = dict()
    for key in sorted(ts2msgdic.keys()):
        symbol2rate = dict()
        for entry in ts2msgdic[key]:
            return_rate = float(entry['content'].rstrip('.').split(' ')[-1])
            symbol = entry['account_name']
            symbol2rate[symbol] = return_rate
        ts2all[key] = symbol2rate

    pd.DataFrame(ts2all).T[['dyaction', 'oneshot', 'constant']].to_csv('bk_res.csv')
