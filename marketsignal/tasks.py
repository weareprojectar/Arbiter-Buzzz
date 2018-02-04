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
    QuarterFinacial,
    BuySell,
)
from marketsignal.models import Index

DATA_PATH = os.getcwd() + '/tmp'

class Processor:
    def __init__(self, filter_date=False):
        recent_update_date = Ticker.objects.distinct('date').values_list('date')
        self.recent_update_date = [data[0] for data in recent_update_date][-1]
        tickers = Ticker.objects.filter(date=self.recent_update_date).values_list('code')
        self.ticker_list = [ticker[0] for ticker in list(tickers)]
        if not filter_date:
            last_year = str(datetime.now().year - 1)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date

    ### STEP 1: reqesting data, saving tmp files locally before processing ###
    def make_data(self):
        start = time.time()
        self.ohlcv_list = []
        self.volume_list = []
        init_qs = OHLCV.objects.filter(code__in=self.ticker_list)
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        ohlcv_qs = filtered_qs.values_list('code', 'date', 'close_price', 'volume')
        self.price_list = []
        self.volume_list = []
        for ticker in self.ticker_list:
            ohlcv_set = set([ohlcv for ohlcv in ohlcv_qs if ohlcv[0] == ticker])
            ticker_price = [{'date': data[1], 'close_price': data[2]} for data in ohlcv_set if data[0] == ticker]
            ticker_volume = [{'date': data[1], 'volume': data[3]} for data in ohlcv_set if data[0] == ticker]
            self.price_list.append(ticker_price)
            self.volume_list.append(ticker_volume)
        end = time.time()
        print('time took: ', str(end-start))

        start = time.time()
        for i in range(len(self.ticker_list)):
            ticker = self.ticker_list[i]
            ohlcv = self.price_list[i]
            vol = self.volume_list[i]
            if i == 0:
                ohlcv_df = self._create_df(ticker, ohlcv, 'close_price')
                vol_df = self._create_df(ticker, vol, 'volume')
            else:
                temp_ohlcv_df = self._create_df(ticker, ohlcv, 'close_price')
                temp_vol_df = self._create_df(ticker, vol, 'volume')
                ohlcv_df = pd.concat([ohlcv_df, temp_ohlcv_df], axis=1)
                vol_df = pd.concat([vol_df, temp_vol_df], axis=1)
        ohlcv_df.index = pd.to_datetime(ohlcv_df.index)
        vol_df.index = pd.to_datetime(vol_df.index)
        self.ohlcv_df = ohlcv_df
        self.vol_df = vol_df
        self.ohlcv_df.to_csv(DATA_PATH + '/ohlcv_df.csv')
        self.vol_df.to_csv(DATA_PATH + '/vol_df.csv')
        end = time.time()
        print('time took: ', str(end-start))
        print('created csv files')

    def _create_df(self, ticker, ohlcv, col_name):
        df = pd.DataFrame(ohlcv)
        df.set_index('date', inplace=True)
        if col_name == 'close_price':
            df.rename(columns={col_name: ticker}, inplace=True)
        if col_name == 'volume':
            df.rename(columns={col_name: ticker}, inplace=True)
        return df

    ### STEP 2: processing data, adding/merging data together into one df ###
    def score_data(self):
        self._get_data_local()
        self.vol = (self.ohlcv_df * self.vol_df).ix[-1]
        self._set_return_portfolio()
        self._add_bm_data()
        self._save_mom_volt_cor_vol() # go to STEP 3

    def _get_data_local(self):
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
        self.vol_df = pd.read_csv(DATA_PATH + '/vol_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)

    def _set_return_portfolio(self):
        self.portfolio_data = self.ohlcv_df.pct_change()

    def _add_bm_data(self):
        from stockapi.models import BM
        BM_qs = BM.objects.filter(name='KOSPI')
        BM_data = list(BM_qs.exclude(date__lte=self.filter_date).values('date', 'index'))
        BM = pd.DataFrame(BM_data)
        BM.set_index('date', inplace=True)
        BM.index = pd.to_datetime(BM.index)
        BM.rename(columns={'index': 'Benchmark'}, inplace=True)
        BM = BM.pct_change()
        self.portfolio_data.index = pd.to_datetime(self.portfolio_data.index)
        self.portfolio_data = pd.concat([self.portfolio_data, BM], axis=1)
        self.portfolio_data.fillna(0, inplace=True)

    ### STEP 3: analyzing data, scoring stocks ###
    def _save_mom_volt_cor_vol(self):
        self._dual_momentum()
        self._calc_volatility()
        self._calc_correlation()

        mom_s = self.mom.rank(ascending=True)
        mom_s = (mom_s/mom_s.max())*100
        mom_s.fillna(0, inplace=True)

        volt_s = self.volt.rank(ascending=False)
        volt_s = (volt_s/volt_s.max())*100
        volt_s.fillna(0, inplace=True)

        cor_s = self.cor.rank(ascending=False)
        cor_s = (cor_s/cor_s.max())*100
        cor_s.fillna(0, inplace=True)

        vol_s = self.vol.rank(ascending=True)
        vol_s = (vol_s/vol_s.max())*100
        vol_s.fillna(0, inplace=True)

        date = self.recent_update_date
        if Specs.objects.filter(date=date).exists() == False:
            specs_list = []
            for ticker in self.ticker_list:
                momentum_score = mom_s[ticker]
                volatility_score = volt_s[ticker]
                correlation_score = cor_s[ticker]
                volume_score = vol_s[ticker]
                total_score = (momentum_score + volatility_score + correlation_score + volume_score)//4

                specs_inst = Specs(code=ticker,
                                   date=date,
                                   momentum=self.mom[ticker],
                                   volatility=self.volt[ticker],
                                   correlation=self.cor[ticker],
                                   volume=self.vol[ticker],
                                   momentum_score=momentum_score,
                                   volatility_score=volatility_score,
                                   correlation_score=correlation_score,
                                   volume_score=volume_score,
                                   total_score=total_score)
                specs_list.append(specs_inst)
                print('Added {} specs'.format(ticker))
            Specs.objects.bulk_create(specs_list)

    def _dual_momentum(self):
        # codes = list(close_data.columns)
        return_data = self.portfolio_data
        for i in range(1, 13):
            momentum = return_data - return_data.shift(i)
            if i == 1:
                temp = momentum
            else:
                temp += momentum
        mom = temp/12
        self.mom = mom.ix[-1]

    def _calc_volatility(self):
        self.volt = pd.DataFrame(self.portfolio_data).rolling(window=12).std().ix[-1]

    def _calc_correlation(self):
        self.cor = self.portfolio_data.corr()['Benchmark']


class Indexer:
    def __init__(self):
        self.markets = ['KOSPI', 'KOSDAQ']
        recent_update_date = Ticker.objects.distinct('date').values_list('date')
        self.recent_update_date = [data[0] for data in recent_update_date][-1]

    ### STEP 4: finding size, style type for stocks ###
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
            inst_list = Info.objects.filter(size_type=size)
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

    def calc_style_index(self):
        style_types = ['G', 'V']
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
        for style in style_types:
            inst_list = Info.objects.filter(style_type=style)
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

@task(name="score_data")
def score_data():
    p = Processor()
    p.score_data()

@task(name="index_data")
def index_size_data():
    i = Indexer()
    # i.size_type_of_stock()
    i.calc_size_index()

@task(name="index_style_data")
def index_style_data():
    i = Indexer()
    # i.style_type_of_stock()
    i.calc_style_index()

@task(name="index_industry_data")
def index_industry_data():
    i = Indexer()
    # i.style_type_of_stock()
    i.calc_industry_index()
