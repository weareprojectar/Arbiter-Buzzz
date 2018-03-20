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


class Scorer:

    def __init__(self, task_name, filter_date=False):
        self.task_name = task_name
        self.recent_update_date = list(Ticker.objects.distinct('date').values_list('date'))[-1][0]
        tickers = Ticker.objects.filter(date=self.recent_update_date).values_list('code')
        self.ticker_list = [ticker[0] for ticker in list(tickers)]
        if self.task_name == 'stock':
            self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
            self.vol_df = pd.read_csv(DATA_PATH + '/vol_df.csv', header=0, index_col='Unnamed: 0', parse_dates=True)
            self.vol = self.ohlcv_df * self.vol_df
            self.portfolio_data = self.ohlcv_df.pct_change()
        elif self.task_name == 'index':
            self.index_types = list(set([name[0] for name in Index.objects.all().distinct('name').values_list('name')]))
            self.index_df = pd.read_csv(DATA_PATH + '/index_df.csv', encoding='cp949', header=0, index_col='date', parse_dates=True)
            self.portfolio_data = self.index_df.pct_change()
        if not filter_date:
            last_year = str(datetime.now().year - 4)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date
        else:
            self.filter_date = filter_date
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
        if self.task_name == 'stock':
            self.vol.fillna(0, inplace=True)

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

            if self.task_name == 'stock':
                vol_s = self.vol.ix[date].rank(ascending=True)
                vol_s = (vol_s/vol_s.max())*100
                vol_s.fillna(0, inplace=True)

            # date = self.recent_update_date
            save_date = str(self.portfolio_data.ix[date].name)[:10].replace('-', '')
            # if Specs.objects.filter(date=date).exists() == False:
            specs_list = []

            if self.task_name == 'stock':
                index_list = self.ticker_list
            elif self.task_name == 'index':
                index_list = self.index_types

            for index in index_list:
                if index == '':
                    continue
                momentum_score = mom_s[index]
                volatility_score = volt_s[index]
                correlation_score = cor_s[index]
                if self.task_name == 'stock':
                    volume_score = vol_s[index]
                total_score = (momentum_score + volatility_score + correlation_score + 100)//4

                if self.task_name == 'stock':
                    specs_inst = Specs(code=index,
                                       date=save_date,
                                       momentum=self.mom.ix[date][index],
                                       volatility=self.volt.ix[date][index],
                                       correlation=self.cor[index],
                                       volume=self.vol.ix[date][index],
                                       momentum_score=momentum_score,
                                       volatility_score=volatility_score,
                                       correlation_score=correlation_score,
                                       volume_score=volume_score,
                                       total_score=total_score)
                elif self.task_name == 'index':
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
            if self.task_name == 'stock':
                Specs.objects.bulk_create(specs_list)
            elif self.task_name == 'index':
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
        if self.task_name == 'stock':
            print('Unable to rate stock scores')
        elif self.task_name == 'index':
            for index in self.index_types:
                if index == '':
                    print('No index, skipping')
                    continue
                print('Starting {}'.format(index))
                ms_qs = MarketScore.objects.filter(name=index).order_by('-date')
                index_scores = [data[0] for data in ms_qs.values_list('total_score')]
                ms_qs = list(ms_qs)
                scores_arr = np.array(index_scores)
                bins = np.linspace(scores_arr.min(), scores_arr.max(), 5)
                scores_section = np.digitize(scores_arr, bins)
                scores_section = 6 - scores_section
                for i in range(len(scores_section)):
                    initial_value = ms_qs[i].score_rating
                    if scores_section[i] == 1:
                        ms_qs[i].score_rating = 'A'
                    elif (scores_section[i] == 2) or (scores_section[i] == 3):
                        ms_qs[i].score_rating = 'B'
                    else:
                        ms_qs[i].score_rating = 'C'
                    ms_qs[i].save()
                    saved_value = ms_qs[i].score_rating
                    print('saved {} {}'.format(index, i))
                    print('value then: {}, and now: {}'.format(initial_value, saved_value))
                    if i == 20:
                        break
                print('Finished {}'.format(index))
