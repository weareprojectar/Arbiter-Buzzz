import os
import datetime
import numpy as np
import pandas as pd

DATA_PATH = '../data/tmp'

os.chdir(DATA_PATH)
files = os.listdir()

net_data = {}
# calculating net buysell
for filename in files:
    df = pd.read_csv(filename)
    codename = str(list(set(df['code']))[0]).zfill(6)
    df.drop(['Unnamed: 0', 'code', 'name', 'close_price'], axis=1, inplace=True)
    buy_df = df[df['buysell'] == 'buy']
    sell_df = df[df['buysell'] == 'sell']
    for tmp_df in [buy_df, sell_df]:
        tmp_df.drop('buysell', axis=1, inplace=True)
        date_list = list(tmp_df['date'])
        tmp_df['date'] = list(map(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'), date_list))
        tmp_df.set_index('date', inplace=True)
        tmp_df.index = pd.to_datetime(tmp_df.index)
        tmp_df.sort_index(inplace=True)
    net_df = buy_df + sell_df
    net_data[codename] = net_df

print(net_data)
