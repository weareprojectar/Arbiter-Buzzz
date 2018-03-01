# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 03:23:52 2018
@author: lmhoo
"""
import os
import pandas as pd
import numpy as np
import time

print(os.getcwd())

def calc_relative_score():
    # for market_type in ['kospi', 'kosdaq']:
    market_type = 'kospi'
    start = time.time()
    market_total_ohlcv = pd.read_csv('../../data/{}_ohlcv.csv'.format(market_type), sep=',', encoding='CP949', low_memory=False)
    market_total_buy = pd.read_csv('../../data/{}_buy.csv'.format(market_type), sep=',', low_memory=False)
    market_total_ab_score = pd.read_csv('../../data/{}_absolute_score.csv'.format(market_type), sep=',', encoding='CP949', low_memory=False)
    market_total_ohlcv= market_total_ohlcv[(market_total_ohlcv['date'] > 20060101) & (market_total_ohlcv['date'] < 20180215)]
    cols = ['date','code','name','close_price', 'volume']
    cols2 =['date', 'code', 'individual', 'foreign_retail', 'institution', 'etc_corporate']
    cols3 = ['date','code', 'absolute_score']
    market_total_ohlcv = market_total_ohlcv[cols]
    market_total_buy = market_total_buy[cols2]
    market_total_ab_score = market_total_ab_score[cols3]
    end = time.time()
    print('time: {}'.format(end - start))

    start = time.time()
    market_total_ohlcv['date'] = pd.to_datetime(market_total_ohlcv['date'], format='%Y%m%d')
    market_total_ohlcv = market_total_ohlcv.sort_values(['code','date'], ascending=[True, True], axis=0)
    market_total_ohlcv = market_total_ohlcv.set_index(['date','code'])
    market_total_buy['date'] = pd.to_datetime(market_total_buy['date'], format='%Y%m%d')
    market_total_buy = market_total_buy.sort_values(['code','date'], ascending=[True, True], axis=0)
    market_total_buy = market_total_buy.set_index(['date','code'])
    market_total_ab_score = market_total_ab_score.reset_index()
    market_total_ab_score['date'] = pd.to_datetime(market_total_ab_score['date'], format='%Y-%m-%d')
    market_total_ab_score['date'] = pd.to_datetime(market_total_ab_score['date'], format='%Y%m%d')
    market_total_ab_score = market_total_ab_score.set_index(['date','code'])

    total_df = pd.concat([market_total_ohlcv, market_total_buy, market_total_ab_score], axis=1, join='inner')
    total_df = total_df.reset_index('code')
    total_df.drop('index', axis=1, inplace=True)
    df_date_list = sorted(list(set(total_df.index.strftime("%Y-%m-%d"))))
    end = time.time()
    print('time: {}'.format(end - start))

    print(total_df.isnull().sum())

    start = time.time()
    i = 0
    total_df['cl*vol_relative'] = total_df['volume']*total_df['close_price']
    tmp_df = total_df.groupby(total_df.index)['cl*vol_relative'].sum()

    #close * volume
    for day in df_date_list:
        i = i + 1
        start_loop = time.time()
        total_df.loc[day, 'cl*vol_relative'] = total_df.loc[day, 'cl*vol_relative']/tmp_df[day]
        total_df.loc[day, 'close_price_relative_rank'] = total_df.loc[day, 'cl*vol_relative'].rank(method='min', ascending=False)
        bins = np.linspace(total_df.loc[day, 'close_price_relative_rank'].min(), total_df.loc[day, 'close_price_relative_rank'].max(), 24)
        total_df.loc[day, 'close_price_relative_rank_section'] = np.digitize(total_df.loc[day, 'close_price_relative_rank'], bins)
        total_df.loc[day, 'close_price_relative_rank_section'] = 25 - total_df.loc[day, 'close_price_relative_rank_section']
        end_loop = time.time()
        print('time: {}'.format(end_loop - start_loop))
    end = time.time()
    print('time: {}'.format(end - start))

    start = time.time()
    # Net buy * close_price
    for column in ['individual','foreign_retail','institution','etc_corporate']:
        total_df[column + '*cl_relative'] = total_df[column]*total_df['close_price']
        tmp_df2 = total_df.groupby(total_df.index)[column+'*cl_relative'].sum()
        i = 0
        for day in df_date_list:
            i = i + 1
            start1 = time.time()
            total_df.loc[day,  column + '*cl_relative'] = total_df.loc[day, column + '*cl_relative']/tmp_df2[day]
            total_df.loc[day,  column + '_relative_rank'] = total_df.loc[day,  column + '*cl_relative'].rank(method='min', ascending=False)
            bins = np.linspace(total_df.loc[day,column + '_relative_rank'].min(), total_df.loc[day, column + '_relative_rank'].max(), 12)
            total_df.loc[day,  column + '_relative_rank_section'] = np.digitize(total_df.loc[day, column + '_relative_rank'], bins)
            total_df.loc[day,  column + '_relative_rank_section'] = 13 - total_df.loc[day,  column + '_relative_rank_section']
            end1 = time.time()
            print(i,'/',len(df_date_list), end1-start1)
    end = time.time()
    print('time: {}'.format(end - start))

    start = time.time()
    total_df['relative_score'] = total_df['close_price_relative_rank_section'] + (total_df['individual_relative_rank_section']/3) + ((2*total_df['foreign_retail_relative_rank_section'])/3) + ((2*total_df['institution_relative_rank_section'])/3) + (total_df['etc_corporate_relative_rank_section']/3)
    total_df['total_score'] = total_df['relative_score'] + total_df['absolute_score']
    total_df['total_score'] = round(total_df['total_score']*round(100/69, 2))
    end = time.time()
    print(end - start)

    drop_list = ['close_price','volume', 'individual', 'foreign_retail', 'institution', 'etc_corporate']
    total_df.drop(drop_list, axis=1, inplace=True)
    total_df.to_csv('../../data/processed/{}_sd_score.csv'.format(market_type), sep=',', encoding='utf-8')

calc_relative_score()
