from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
import os, time
import pandas as pd
import numpy as np

from stockapi.models import (
    BM,
    Ticker,
    OHLCV,
    Specs,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinancial,
)
from marketsignal.models import Index, MarketScore, MSHome, RankData

DATA_PATH = os.getcwd() + '/tmp'
CLOSE_PATH = os.getcwd() + '/data/close'
VOLUME_PATH = os.getcwd() + '/data/volume'


class Indexer:
    def __init__(self):
        self.markets = ['KOSPI', 'KOSDAQ']
        self.recent_update_date = list(Ticker.objects.distinct('date').values_list('date'))[-1][0]

    ### STEP 2: finding size, style type for stocks ###
    def size_type_of_stock(self):
        for market in self.markets:
            inst_list = Info.objects.filter(date=self.recent_update_date).filter(market_type=market)
            cap_list = [int(inst.market_cap) for inst in inst_list]
            rank_list = pd.DataFrame(cap_list).rank(ascending=False)[0] # bigger value gets lower rank
            for i in range(len(inst_list)):
                rank = int(rank_list[i])
                inst_list[i].market_cap_rank = rank
                mid_rank = 300 if market == 'KOSPI' else 400
                if rank <= 100:
                    inst_list[i].size_type = 'L'
                elif rank > 100 and rank <= mid_rank:
                    inst_list[i].size_type = 'M'
                else:
                    inst_list[i].size_type = 'S'
                inst_list[i].save()
                print('Saved {} cap rank'.format(inst_list[i].code))

    def style_type_of_stock(self):
        inst_list = Info.objects.filter(date=self.recent_update_date)
        inst_list = list(filter(lambda x: x.per != 0, inst_list))
        type_dict = {
            'G': list(filter(lambda x: x.per >= 8.0, inst_list)),
            'V': list(filter(lambda x: x.per < 8.0, inst_list))
        }
        for key, val in type_dict.items():
            for inst in val:
                inst.style_type = key
                inst.save()
                print('Saved {} style type'.format(inst.code))

    def calc_size_index(self):
        size_types = ['L', 'M', 'S']
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
        for size in size_types:
            inst_list = Info.objects.filter(date=self.recent_update_date).filter(size_type=size)
            tickers = [inst.code for inst in inst_list]
            tickers = list(filter(lambda x: x in self.ohlcv_df.columns, tickers))
            df = self.ohlcv_df[tickers]
            ret = df.pct_change().fillna(0).replace(np.inf, 0).replace(-1.0, 0)
            data_list = []
            for i in range(len(ret)):
                row = ret.ix[i]
                div_by = len(list(filter(lambda x: x != 0, list(row))))
                div_by = 1 if div_by == 0 else div_by
                # date = row.name.strftime('%Y%m%d')
                index = row.sum()/div_by
                data_list.append(index)
            tmp = np.array(data_list)
            index_list = []
            for j in range(len(tmp)):
                if j == 0:
                    rt = (tmp[j] + 1)
                else:
                    rt = index_list[j-1]*(tmp[j] + 1)
                index_list.append(rt)
            index_list = list(map(lambda x: x*100, index_list))
            df['Index'] = index_list
            data_list = []
            for n in range(len(df)):
                date = df.ix[n].name.strftime('%Y%m%d')
                name = size
                index = df.ix[n]['Index']
                category = 'S'
                index_inst = Index(date=date,
                                   name=name,
                                   index=index,
                                   category=category)
                data_list.append(index_inst)
            Index.objects.bulk_create(data_list)
            print('Finished {} data'.format(size))

    def calc_style_index(self):
        style_types = ['G', 'V']
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
        for style in style_types:
            inst_list = Info.objects.filter(date=self.recent_update_date).filter(style_type=style)
            tickers = [inst.code for inst in inst_list]
            tickers = list(filter(lambda x: x in self.ohlcv_df.columns, tickers))
            df = self.ohlcv_df[tickers]
            ret = df.pct_change().fillna(0).replace(np.inf, 0).replace(-1.0, 0)
            data_list = []
            for i in range(len(ret)):
                row = ret.ix[i]
                div_by = len(list(filter(lambda x: x != 0, list(row))))
                div_by = 1 if div_by == 0 else div_by
                # date = row.name.strftime('%Y%m%d')
                index = row.sum()/div_by
                data_list.append(index)
            tmp = np.array(data_list)
            index_list = []
            for j in range(len(tmp)):
                if j == 0:
                    rt = (tmp[j] + 1)
                else:
                    rt = index_list[j-1]*(tmp[j] + 1)
                index_list.append(rt)
            index_list = list(map(lambda x: x*100, index_list))
            df['Index'] = index_list
            data_list = []
            for n in range(len(df)):
                date = df.ix[n].name.strftime('%Y%m%d')
                name = style
                index = df.ix[n]['Index']
                category = 'ST'
                index_inst = Index(date=date,
                                   name=name,
                                   index=index,
                                   category=category)
                data_list.append(index_inst)
            Index.objects.bulk_create(data_list)
            print('Finished {} data'.format(style))

    def calc_industry_index(self):
        ind_types = [data.industry for data in list(Info.objects.distinct('industry'))]
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
        for ind in ind_types:
            inst_list = Info.objects.filter(industry=ind)
            tickers = [inst.code for inst in inst_list]
            tickers = list(filter(lambda x: x in self.ohlcv_df.columns, tickers))
            df = self.ohlcv_df[tickers]
            ret = df.pct_change().fillna(0).replace(np.inf, 0).replace(-1.0, 0)
            data_list = []
            for i in range(len(ret)):
                row = ret.ix[i]
                div_by = len(list(filter(lambda x: x != 0, list(row))))
                div_by = 1 if div_by == 0 else div_by
                # date = row.name.strftime('%Y%m%d')
                index = row.sum()/div_by
                data_list.append(index)
            tmp = np.array(data_list)
            index_list = []
            for j in range(len(tmp)):
                if j == 0:
                    rt = (tmp[j] + 1)
                else:
                    rt = index_list[j-1]*(tmp[j] + 1)
                index_list.append(rt)
            index_list = list(map(lambda x: x*100, index_list))
            df['Index'] = index_list
            data_list = []
            for n in range(len(df)):
                date = df.ix[n].name.strftime('%Y%m%d')
                name = ind
                index = df.ix[n]['Index']
                category = 'I'
                index_inst = Index(date=date,
                                   name=name,
                                   index=index,
                                   category=category)
                data_list.append(index_inst)
            Index.objects.bulk_create(data_list)
            print('Finished {} data'.format(ind))
