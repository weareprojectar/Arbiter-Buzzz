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


class Processor:

    def __init__(self, filter_date=False):
        self.recent_update_date = list(Ticker.objects.distinct('date').values_list('date'))[-1][0]
        tickers = Ticker.objects.filter(date=self.recent_update_date).values_list('code')
        self.ticker_list = [ticker[0] for ticker in list(tickers)]
        if not filter_date:
            last_year = str(datetime.now().year - 4)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date
        else:
            self.filter_date = filter_date

    ### STEP 1: reqesting data, saving tmp files locally before processing ###
    def make_base_data(self):
        # performance: approx. 3 mins
        start = time.time()
        init_qs = OHLCV.objects.filter(code__in=self.ticker_list)
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        ohlcv_qs = filtered_qs.values_list('code', 'date', 'close_price', 'volume')
        print('DB query successfully sent and data received.')
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

    def make_index_data(self):
        ### should be called after Indexer class created all size, style, and industry indexes
        start = time.time()
        # get index types
        index_types = list(set([name[0] for name in Index.objects.all().distinct('name').values_list('name')]))
        init_qs = Index.objects.all()
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        index_qs = filtered_qs.values_list('name', 'date', 'index')
        print('Index DB query successfully sent and data received.')
        self.index_list = []
        for index in index_types:
            index_set = set([index_data for index_data in index_qs if index_data[0] == index])
            index_price = [{'date': data[1], 'index': float(format(round(data[2], 3), '.3f'))} for data in index_qs if data[0] == index]
            self.index_list.append(index_price)
        end = time.time()
        print('time took: ', str(end-start))

        start = time.time()
        for i in range(len(index_types)):
            index = index_types[i]
            price = self.index_list[i]
            if i == 0:
                index_df = self._create_df(index, price, 'index')
            else:
                temp_index_df = self._create_df(index, price, 'index')
                index_df = pd.concat([index_df, temp_index_df], axis=1)
        index_df.index = pd.to_datetime(index_df.index)
        self.index_df = index_df
        self.index_df.to_csv(DATA_PATH + '/index_df.csv')
        end = time.time()
        print('time took: ', str(end-start))
        print('created csv files')

    def _create_df(self, index, data, col_name):
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        df = df.sort_index()
        df.rename(columns={col_name: index}, inplace=True)
        return df

    ### STEP 2: processing data, adding/mergin data together into one df ###
    def score_data(self):
        self._get_data_local()
        self.vol = self.ohlcv_df * self.vol_df
        self._set_return_portfolio()
        self._add_bm_data()
        self._save_mom_volt_cor_vol()


class Scorer:

    def __init__(self, task_name):
        self.task_name = task_name
        if self.task_name == 'stock':
            self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
            self.vol_df = pd.read_csv(DATA_PATH + '/vol_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
            self.portfolio_data = self.ohlcv_df.pct_change()
        elif self.task_name == 'index':
            self.index_df = pd.read_csv(DATA_PATH + '/index_df.csv', encoding='cp949', header=0, index_col='date', parse_dates=True)
            self.portfolio_data = self.index_df.pct_change()
        self._add_bm_data()

    def _add_bm_data(self):
        for bm_type in ['KOSPI', 'KOSDAQ']:
            from stockapi.models import BM
            BM_qs = BM.objects.filter(name=bm_type)
            BM_data = list(BM_qs.exclude(date__lte=self.filter_date).values('date', 'index'))
            BM = pd.DataFrame(BM_data)
            BM.set_index('date', inplace=True)
            BM.index = pd.to_datetime(BM.index)
            BM.rename(columns={'index': bm_type}, inplace=True)
            BM = BM.pct_change()
            self.portfolio_data.index = pd.to_datetime(self.portfolio_data.index)
            self.portfolio_data = pd.concat([self.portfolio_data, BM], axis=1)
            self.portfolio_data.fillna(0, inplace=True)

    def save_mom_volt_cor_vol(self):
        self._dual_momentum()
        print('calculated momentum')
        self._calc_volatility()
        print('calculated volatility')
        self._calc_correlation()
        print('calculated correlation')

        self.mom.fillna(0, inplace=True)
        self.volt.fillna(0, inplace=True)

        for date in range(len(self.portfolio_data)):
            mom_s = self.mom.ix[date].rank(ascending=True)
            mom_s = (mom_s/mom_s.max())*100
            mom_s.fillna(0, inplace=True)

            volt_s = self.volt.ix[date].rank(ascending=False)
            volt_s = (volt_s/volt_s.max())*100
            volt_s.fillna(0, inplace=True)

            cor_s = self.cor.rank(ascending=False)
            cor_s = (cor_s/cor_s.max())*100
            cor_s.fillna(0, inplace=True)

            # date = self.recent_update_date
            save_date = str(self.portfolio_data.ix[date].name)[:10].replace('-', '')
            # if Specs.objects.filter(date=date).exists() == False:
            specs_list = []
            for index in self.index_types:
                momentum_score = mom_s[index]
                volatility_score = volt_s[index]
                correlation_score = cor_s[index]
                total_score = (momentum_score + volatility_score + correlation_score + 100)//4

                specs_inst = MarketScore(date=save_date,
                                         name=index,
                                         momentum=self.mom.ix[date][index],
                                         volatility=self.volt.ix[date][index],
                                         correlation=self.cor[index],
                                         momentum_score=momentum_score,
                                         volatility_score=volatility_score,
                                         correlation_score=correlation_score,
                                         volume_score=100,
                                         total_score=total_score)
                specs_list.append(specs_inst)
            MarketScore.objects.bulk_create(specs_list)
            print('Saved {} specs data'.format(save_date))

    def _dual_momentum(self):
        return_data = self.portfolio_data
        for i in range(1, 13):
            momentum = return_data - return_data.shift(i*20)
            if i == 1:
                temp = momentum
            else:
                temp += momentum
        mom = temp/12
        self.mom = mom

    def _calc_volatility(self):
        self.volt = pd.DataFrame(self.portfolio_data).rolling(window=60).std()

    def _calc_correlation(self):
        self.cor = self.portfolio_data.corr()['KOSPI']

    def calculate_score_ratings(self):
        for index in self.index_types:
            print('Starting {}'.format(index))
            ms_qs = MarketScore.objects.filter(name=index).order_by('-date')
            index_scores = [data[0] for data in ms_qs.values_list('total_score')]
            scores_arr = np.array(index_scores)
            bins = np.linspace(scores_arr.min(), scores_arr.max(), 5)
            scores_section = np.digitize(scores_arr, bins)
            scores_section = 6 - scores_section
            for i in range(len(scores_section)):
                print(ms_qs[i].score_rating)
                if scores_section[i] == 1:
                    ms_qs[i].score_rating = 'A'
                elif (scores_section[i] == 2) or (scores_section[i] == 3):
                    ms_qs[i].score_rating = 'B'
                else:
                    ms_qs[i].score_rating = 'C'
                ms_qs[i].save()
                print('saved {}'.format(i))
                if i == 20:
                    break
            print('Finished {}'.format(index))


@task(name="market_signal_task")
def market_signal_task():
    # initialize Processor
    p = Processor()
    p.make_data()
