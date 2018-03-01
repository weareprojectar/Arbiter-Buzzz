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
from marketsignal.models import Index, MarketScore, MSHome2, RankData

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

    def init_ohlcv_csv_save(self):
        ticker_count = len(self.ticker_list)
        print('Initializing OHLCV csv local save: {} tickers exist'.format(ticker_count))
        processed_count = 1
        init_qs = OHLCV.objects.filter(code__in=self.ticker_list)
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        ohlcv_qs = list(filtered_qs.values_list('code', 'date', 'close_price', 'volume'))
        print('DB request sent successfully')
        for ticker in self.ticker_list:
            print('Starting {}'.format(ticker))
            ohlcv_set = set([ohlcv for ohlcv in ohlcv_qs if ohlcv[0] == ticker])
            ticker_price = [{'date': data[1], 'close_price': data[2]} for data in ohlcv_set if data[0] == ticker]
            ticker_volume = [{'date': data[1], 'volume': data[3]} for data in ohlcv_set if data[0] == ticker]
            price_df = self._create_df(ticker, ticker_price, 'close_price')
            vol_df = self._create_df(ticker, ticker_volume, 'volume')
            price_df.to_csv(CLOSE_PATH + '/{}.csv'.format(ticker))
            price_df.index = pd.to_datetime(price_df.index)
            vol_df.to_csv(VOLUME_PATH + '/{}.csv'.format(ticker))
            vol_df.index = pd.to_datetime(vol_df.index)
            print('{} {} price/volume csv saved'.format(processed_count, ticker))
            processed_count += 1

    ### STEP 1: reqesting data, saving tmp files locally before processing ###
    def make_data(self):
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

    def make_financial_data(self):
        ### financial ###
        start = time.time()
        init_qs = Financial.objects.filter(code__in=self.ticker_list)
        filter_date = self.filter_date[:6]
        filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        financial_qs = filtered_qs.values_list('code', 'date', 'revenue', 'capital', 'net_profit')
        print('Financial DB query successfully sent and data received.')
        self.revenue_list = []
        self.capital_list = []
        self.net_profit_y_list = []
        for ticker in self.ticker_list:
            financial_set = set([financial for financial in financial_qs if financial[0] == ticker])
            ticker_revenue = [{'date': data[1], 'revenue': data[2]} for data in financial_set if data[0] == ticker]
            ticker_capital = [{'date': data[1], 'capital': data[3]} for data in financial_set if data[0] == ticker]
            ticker_net_profit_y = [{'date': data[1], 'net_profit': data[3]} for data in financial_set if data[0] == ticker]
            self.revenue_list.append(ticker_revenue)
            self.capital_list.append(ticker_capital)
            self.net_profit_y_list.append(ticker_net_profit_y)
        end = time.time()
        print('time took: ', str(end-start))

        start = time.time()
        for i in range(len(self.ticker_list)):
            ticker = self.ticker_list[i]
            revenue = self.revenue_list[i]
            capital = self.capital_list[i]
            net_profit_y = self.net_profit_y_list[i]
            if (revenue == []) and (capital == []) and (net_profit_y == []):
                revenue_df[ticker] = [0]*len(revenue_df)
                capital_df[ticker] = [0]*len(capital_df)
                net_profit_y_df[ticker] = [0]*len(net_profit_y_df)
                continue
            if i == 0:
                revenue_df = self._create_df(ticker, revenue, 'revenue')
                capital_df = self._create_df(ticker, capital, 'capital')
                net_profit_y_df = self._create_df(ticker, net_profit_y, 'net_profit')
            else:
                temp_revenue_df = self._create_df(ticker, revenue, 'revenue')
                temp_capital_df = self._create_df(ticker, capital, 'capital')
                temp_net_profit_y_df = self._create_df(ticker, net_profit_y, 'net_profit')
                revenue_df = pd.concat([revenue_df, temp_revenue_df], axis=1)
                capital_df = pd.concat([capital_df, temp_capital_df], axis=1)
                net_profit_y_df = pd.concat([net_profit_y_df, temp_net_profit_y_df], axis=1)
        revenue_df.index = pd.to_datetime(revenue_df.index, format='%Y%m')
        capital_df.index = pd.to_datetime(capital_df.index, format='%Y%m')
        net_profit_y_df.index = pd.to_datetime(net_profit_y_df.index, format='%Y%m')
        self.revenue_df = revenue_df
        self.capital_df = capital_df
        self.net_profit_y_df = net_profit_y_df
        self.revenue_df.to_csv(DATA_PATH + '/revenue_df.csv')
        self.capital_df.to_csv(DATA_PATH + '/capital_df.csv')
        self.net_profit_y_df.to_csv(DATA_PATH + '/net_profit_y_df.csv')
        end = time.time()
        print('time took: ', str(end-start))
        print('created csv files')

        # ### quarterfinancial ###
        # start = time.time()
        # init_qs = QuarterFinancial.objects.filter(code__in=self.ticker_list)
        # filter_date = self.filter_date[:6]
        # filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        # quarter_qs = filtered_qs.values_list('code', 'date', 'revenue', 'net_profit')
        # print('QuarterFinancial DB query successfully sent and data received.')
        # self.qrevenue_list = []
        # self.net_profit_list = []
        # for ticker in self.ticker_list:
        #     financial_set = set([financial for financial in quarter_qs if financial[0] == ticker])
        #     ticker_qrevenue = [{'date': data[1], 'revenue': data[2]} for data in financial_set if data[0] == ticker]
        #     ticker_net_profit = [{'date': data[1], 'net_profit': data[3]} for data in financial_set if data[0] == ticker]
        #     self.qrevenue_list.append(ticker_qrevenue)
        #     self.net_profit_list.append(ticker_net_profit)
        # end = time.time()
        # print('time took: ', str(end-start))
        #
        # start = time.time()
        # for i in range(len(self.ticker_list)):
        #     ticker = self.ticker_list[i]
        #     qrevenue = self.qrevenue_list[i]
        #     net_profit = self.net_profit_list[i]
        #     if (qrevenue == []) and (net_profit == []):
        #         qrevenue_df[ticker] = [0]*len(qrevenue_df)
        #         net_profit_df[ticker] = [0]*len(net_profit_df)
        #         continue
        #     if i == 0:
        #         qrevenue_df = self._create_df(ticker, qrevenue, 'revenue')
        #         net_profit_df = self._create_df(ticker, net_profit, 'net_profit')
        #     else:
        #         temp_qrevenue_df = self._create_df(ticker, qrevenue, 'revenue')
        #         temp_net_profit_df = self._create_df(ticker, net_profit, 'net_profit')
        #         qrevenue_df = pd.concat([qrevenue_df, temp_qrevenue_df], axis=1)
        #         net_profit_df = pd.concat([net_profit_df, temp_net_profit_df], axis=1)
        # qrevenue_df.index = pd.to_datetime(qrevenue_df.index, format='%Y%m')
        # net_profit_df.index = pd.to_datetime(net_profit_df.index, format='%Y%m')
        # self.qrevenue_df = qrevenue_df
        # self.net_profit_df = net_profit_df
        # self.qrevenue_df.to_csv(DATA_PATH + '/qrevenue_df.csv')
        # self.net_profit_df.to_csv(DATA_PATH + '/net_profit_df.csv')
        # end = time.time()
        # print('time took: ', str(end-start))
        # print('created csv files')

        # ### financialratio ###
        # start = time.time()
        # init_qs = FinancialRatio.objects.filter(code__in=self.ticker_list)
        # filter_date = self.filter_date[:6]
        # filtered_qs = init_qs.exclude(date__lte=self.filter_date).order_by('date')
        # rfinancial_qs = filtered_qs.values_list('code', 'date', 'consolidate_roe')
        # print('FinancialRatio DB query successfully sent and data received.')
        # self.roe_list = []
        # for ticker in self.ticker_list:
        #     financial_set = set([financial for financial in rfinancial_qs if financial[0] == ticker])
        #     ticker_roe = [{'date': data[1], 'consolidate_roe': data[2]} for data in financial_set if data[0] == ticker]
        #     self.roe_list.append(ticker_roe)
        # end = time.time()
        # print('time took: ', str(end-start))
        #
        # start = time.time()
        # for i in range(len(self.ticker_list)):
        #     ticker = self.ticker_list[i]
        #     roe = self.roe_list[i]
        #     if (roe == []):
        #         roe_df[ticker] = [0]*len(roe_df)
        #         continue
        #     if i == 0:
        #         roe_df = self._create_df(ticker, roe, 'consolidate_roe')
        #     else:
        #         temp_roe_df = self._create_df(ticker, roe, 'consolidate_roe')
        #         print(temp_roe_df)
        #         print(len(temp_roe_df))
        #         roe_df = pd.concat([roe_df, temp_roe_df], axis=1)
        #         print(roe_df)
        # roe_df.index = pd.to_datetime(roe_df.index, format='%Y%m')
        # self.roe_df = roe_df
        # self.roe_df.to_csv(DATA_PATH + '/roe_df.csv')
        # end = time.time()
        # print('time took: ', str(end-start))
        # print('created csv files')

    def _create_df(self, ticker, ohlcv, col_name):
        df = pd.DataFrame(ohlcv)
        df.set_index('date', inplace=True)
        df = df.sort_index()
        df.rename(columns={col_name: ticker}, inplace=True)
        return df

    ### STEP 2: processing data, adding/merging data together into one df ###
    def score_data(self):
        self._get_data_local()
        # self.vol = (self.ohlcv_df * self.vol_df).ix[-1]
        self.vol = self.ohlcv_df * self.vol_df
        print('calculated volume')
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
        print('calculated momentum')
        self._calc_volatility()
        print('calculated volatility')
        self._calc_correlation()
        print('calculated correlation')

        self.mom.fillna(0, inplace=True)
        self.volt.fillna(0, inplace=True)
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

            vol_s = self.vol.ix[date].rank(ascending=True)
            vol_s = (vol_s/vol_s.max())*100
            vol_s.fillna(0, inplace=True)

            # date = self.recent_update_date
            save_date = str(self.portfolio_data.ix[date].name)[:10].replace('-', '')
            # if Specs.objects.filter(date=date).exists() == False:
            specs_list = []
            for ticker in self.ticker_list:
                momentum_score = mom_s[ticker]
                volatility_score = volt_s[ticker]
                correlation_score = cor_s[ticker]
                volume_score = vol_s[ticker]
                total_score = (momentum_score + volatility_score + correlation_score + volume_score)//4

                specs_inst = Specs(code=ticker,
                                   date=save_date,
                                   momentum=self.mom.ix[date][ticker],
                                   volatility=self.volt.ix[date][ticker],
                                   correlation=self.cor[ticker],
                                   volume=self.vol.ix[date][ticker],
                                   momentum_score=momentum_score,
                                   volatility_score=volatility_score,
                                   correlation_score=correlation_score,
                                   volume_score=volume_score,
                                   total_score=total_score)
                specs_list.append(specs_inst)
            Specs.objects.bulk_create(specs_list)
            print('Saved {} specs data'.format(save_date))

    def _dual_momentum(self):
        # codes = list(close_data.columns)
        return_data = self.portfolio_data
        for i in range(1, 13):
            momentum = return_data - return_data.shift(i*20)
            if i == 1:
                temp = momentum
            else:
                temp += momentum
        mom = temp/12
        # self.mom = mom.ix[-1]
        self.mom = mom

    def _calc_volatility(self):
        # self.volt = pd.DataFrame(self.portfolio_data).rolling(window=12).std().ix[-1]
        self.volt = pd.DataFrame(self.portfolio_data).rolling(window=60).std()

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


class IndexScorer(object):
    def __init__(self, filter_date=False):
        self.recent_update_date = list(Ticker.objects.distinct('date').values_list('date'))[-1][0]
        self.index_types = list(set([name[0] for name in Index.objects.all().distinct('name').values_list('name')]))
        if not filter_date:
            last_year = str(datetime.now().year - 4)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date
        else:
            self.filter_date = filter_date

    def make_data(self):
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

    def _create_df(self, ticker, ohlcv, col_name):
        df = pd.DataFrame(ohlcv)
        df.set_index('date', inplace=True)
        df = df.sort_index()
        df.rename(columns={col_name: ticker}, inplace=True)
        return df

    def score_data(self):
        self._get_data_local()
        self._set_return_portfolio()
        self._add_bm_data()
        self._save_mom_volt_cor_vol()

    def _get_data_local(self):
        self.index_df = pd.read_csv(DATA_PATH + '/index_df.csv', encoding='cp949', header=0, index_col='date', parse_dates=True)

    def _set_return_portfolio(self):
        self.portfolio_data = self.index_df.pct_change()

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

    ### STEP 3: analyzing data, scoring stocks ###
    def _save_mom_volt_cor_vol(self):
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
        # codes = list(close_data.columns)
        return_data = self.portfolio_data
        for i in range(1, 13):
            momentum = return_data - return_data.shift(i*20)
            if i == 1:
                temp = momentum
            else:
                temp += momentum
        mom = temp/12
        # self.mom = mom.ix[-1]
        self.mom = mom

    def _calc_volatility(self):
        # self.volt = pd.DataFrame(self.portfolio_data).rolling(window=12).std().ix[-1]
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


class MSHomeProcessor:
    def __init__(self, today_date=None):
        if today_date == None:
            self.today_date = datetime.now().strftime('%Y%m%d')
        else:
            self.today_date = today_date

    def format_decimal(self, data):
        return float(format(round(data, 2), '.2f'))

    def change_to_pct(self, data):
        return float(format(round(data, 4), '.4f')) * 100

    def get_bm_info(self):
        from stockapi.models import BM
        index_list = BM.objects.order_by('-date')[:4]
        kospi_index = []
        kosdaq_index = []
        for index_inst in index_list:
            index_name = index_inst.name
            if index_name == 'KOSPI':
                kospi_index.append(index_inst.index)
            elif index_name == 'KOSDAQ':
                kosdaq_index.append(index_inst.index)
        kospi_change = kospi_index[0] - kospi_index[1]
        kospi_rate = kospi_change/kospi_index[1]
        kosdaq_change = kosdaq_index[0] - kosdaq_index[1]
        kosdaq_rate = kosdaq_change/kosdaq_index[1]
        return {
            'kospi_index': self.format_decimal(kospi_index[0]),
            'kospi_change': self.format_decimal(kospi_change),
            'kospi_rate': self.change_to_pct(kospi_rate),
            'kosdaq_index': self.format_decimal(kosdaq_index[0]),
            'kosdaq_change': self.format_decimal(kosdaq_change),
            'kosdaq_rate': self.change_to_pct(kosdaq_rate)
        }

    def get_size_info(self):
        size_list = Index.objects.filter(category='S').order_by('-date')[:3]
        score_list = MarketScore.objects.filter(name__in=['L', 'M', 'S']).order_by('-date')[:6]

        for size_inst in size_list:
            index_name = size_inst.name
            if index_name == 'L':
                l_index = size_inst.index
            elif index_name == 'M':
                m_index = size_inst.index
            elif index_name == 'S':
                s_index = size_inst.index

        l_scores, m_scores, s_scores = [], [], []
        for score_inst in score_list:
            index_name = score_inst.name
            if index_name == 'L':
                l_scores.append(score_inst.total_score)
            elif index_name == 'M':
                m_scores.append(score_inst.total_score)
            elif index_name == 'S':
                s_scores.append(score_inst.total_score)

        data = {
            'l_index': self.format_decimal(l_index),
            'l_score': l_scores[0],
            'l_change': l_scores[0] - l_scores[1],
            'm_index': self.format_decimal(m_index),
            'm_score': m_scores[0],
            'm_change': m_scores[0] - m_scores[1],
            's_index': self.format_decimal(s_index),
            's_score': s_scores[0],
            's_change': s_scores[0] - s_scores[1]
        }
        for size in ['l', 'm', 's']:
            if data[size + '_change'] > 0:
                state = 'line_up'
            elif data[size + '_change'] == 0:
                state = 'line_middle'
            else:
                state = 'line_down'
            data[size + '_state'] = state
        return data

    def get_style_info(self):
        style_list = Index.objects.filter(category='ST').order_by('-date')[:4]
        score_list = MarketScore.objects.filter(name__in=['G', 'V']).order_by('-date')[:4]

        for style_inst in style_list:
            index_name = style_inst.name
            if index_name == 'G':
                g_index = style_inst.index
            elif index_name == 'V':
                v_index = style_inst.index

        g_scores, v_scores = [], []
        for score_inst in score_list:
            index_name = score_inst.name
            if index_name == 'G':
                g_scores.append(score_inst.total_score)
            elif index_name == 'V':
                v_scores.append(score_inst.total_score)

        data = {
            'g_index': self.format_decimal(g_index),
            'g_score': g_scores[0],
            'g_change': g_scores[0] - g_scores[1],
            'v_index': self.format_decimal(v_index),
            'v_score': v_scores[0],
            'v_change': v_scores[0] - v_scores[1]
        }
        for size in ['g', 'v']:
            if data[size + '_change'] > 0:
                state = 'line_up'
            elif data[size + '_change'] == 0:
                state = 'line_middle'
            else:
                state = 'line_down'
            data[size + '_state'] = state
        return data

    def get_industry_info(self):
        industry_qs = Index.objects.filter(category='I')
        last_date = industry_qs.order_by('-date').first().date
        ranked_index = [data.name for data in industry_qs.filter(date=last_date).order_by('-index')[:3]]

        industry_list = industry_qs.filter(name__in=ranked_index).order_by('-date')[:3]
        score_list = MarketScore.objects.filter(name__in=ranked_index).order_by('-date')[:6]

        for industry_inst in industry_list:
            index_name = industry_inst.name
            if index_name == ranked_index[0]:
                ind_1_index = industry_inst.name
            elif index_name == ranked_index[1]:
                ind_2_index = industry_inst.name
            elif index_name == ranked_index[2]:
                ind_3_index = industry_inst.name

        ind_1_scores, ind_2_scores, ind_3_scores = [], [], []
        for score_inst in score_list:
            index_name = score_inst.name
            if index_name == ranked_index[0]:
                ind_1_scores.append(score_inst.total_score)
            elif index_name == ranked_index[1]:
                ind_2_scores.append(score_inst.total_score)
            elif index_name == ranked_index[2]:
                ind_3_scores.append(score_inst.total_score)

        data = {
            'ind_1_index': ind_1_index,
            'ind_1_score': ind_1_scores[0],
            'ind_1_change': ind_1_scores[0] - ind_1_scores[1],
            'ind_2_index': ind_2_index,
            'ind_2_score': ind_2_scores[0],
            'ind_2_change': ind_2_scores[0] - ind_2_scores[1],
            'ind_3_index': ind_3_index,
            'ind_3_score': ind_3_scores[0],
            'ind_3_change': ind_3_scores[0] - ind_3_scores[1]
        }
        for size in ['ind_1', 'ind_2', 'ind_3']:
            if data[size + '_change'] > 0:
                state = 'line_up'
            elif data[size + '_change'] == 0:
                state = 'line_middle'
            else:
                state = 'line_down'
            data[size + '_state'] = state
        return data

    def save_data(self):
        date_exists = MSHome2.objects.filter(date=self.today_date).exists()
        if not date_exists:
            bm_info = self.get_bm_info()
            size_info = self.get_size_info()
            style_info = self.get_style_info()
            industry_info = self.get_industry_info()
            mshome_inst = MSHome2(date=self.today_date,
                                 kospi_index=bm_info['kospi_index'],
                                 kospi_change=bm_info['kospi_change'],
                                 kospi_rate=bm_info['kospi_rate'],
                                 kosdaq_index=bm_info['kosdaq_index'],
                                 kosdaq_change=bm_info['kosdaq_change'],
                                 kosdaq_rate=bm_info['kosdaq_rate'],
                                 l_index=size_info['l_index'],
                                 l_score=size_info['l_score'],
                                 l_change=abs(size_info['l_change']),
                                 l_state=size_info['l_state'],
                                 m_index=size_info['m_index'],
                                 m_score=size_info['m_score'],
                                 m_change=abs(size_info['m_change']),
                                 m_state=size_info['m_state'],
                                 s_index=size_info['s_index'],
                                 s_score=size_info['s_score'],
                                 s_change=abs(size_info['s_change']),
                                 s_state=size_info['s_state'],
                                 g_index=style_info['g_index'],
                                 g_score=style_info['g_score'],
                                 g_change=abs(style_info['g_change']),
                                 g_state=style_info['g_state'],
                                 v_index=style_info['v_index'],
                                 v_score=style_info['v_score'],
                                 v_change=abs(style_info['v_change']),
                                 v_state=style_info['v_state'],
                                 ind_1_index=industry_info['ind_1_index'],
                                 ind_1_score=industry_info['ind_1_score'],
                                 ind_1_change=abs(industry_info['ind_1_change']),
                                 ind_1_state=industry_info['ind_1_state'],
                                 ind_2_index=industry_info['ind_2_index'],
                                 ind_2_score=industry_info['ind_2_score'],
                                 ind_2_change=abs(industry_info['ind_2_change']),
                                 ind_2_state=industry_info['ind_2_state'],
                                 ind_3_index=industry_info['ind_3_index'],
                                 ind_3_score=industry_info['ind_3_score'],
                                 ind_3_change=abs(industry_info['ind_3_change']),
                                 ind_3_state=industry_info['ind_3_state'])
            mshome_inst.save()
            print('Save complete')
        else:
            print('Already exists, not saving')

    def make_rank_data(self):
        date_cut = Info.objects.order_by('-date').first().date
        ind_list = [ind[0] for ind in Info.objects.filter(date=date_cut).distinct('industry').values_list('industry')]
        loop_list = ['KOSPI', 'KOSDAQ', 'L', 'M', 'S', 'G', 'V'] + ind_list

        for filter_by in loop_list:
            print(filter_by)
            queryset = Specs.objects.all()
            if (filter_by == 'KOSPI') or (filter_by == 'KOSDAQ'):
                mkt_list = [data[0] for data in Ticker.objects.filter(market_type=filter_by).distinct('code').values_list('code')]
                queryset = queryset.filter(code__in=mkt_list).order_by('total_score').reverse()[:100]
            elif (filter_by == 'L') or (filter_by == 'M') or (filter_by == 'S'):
                s_list = [data[0] for data in Info.objects.filter(date=date_cut).filter(size_type=filter_by).values_list('code')]
                queryset = queryset.filter(code__in=s_list).order_by('total_score').reverse()[:100]
            elif (filter_by == 'G') or (filter_by == 'V'):
                st_list = [data[0] for data in Info.objects.filter(date=date_cut).filter(style_type=filter_by).values_list('code')]
                queryset = queryset.filter(code__in=st_list).order_by('total_score').reverse()[:100]
            else:
                i_list = [data[0] for data in Info.objects.filter(date=date_cut).filter(industry=filter_by).values_list('code')]
                queryset = queryset.filter(code__in=i_list).order_by('total_score').reverse()[:100]


def init_ohlcv_csv_save():
    p = Processor()
    p.init_ohlcv_csv_save()

@task(name="score_data")
def score_data():
    p = Processor()
    p.make_data()
    p.score_data()

@task(name="index_data")
def index_size_data():
    i = Indexer()
    i.size_type_of_stock()
    i.calc_size_index()

@task(name="index_style_data")
def index_style_data():
    i = Indexer()
    i.style_type_of_stock()
    i.calc_style_index()

@task(name="index_industry_data")
def index_industry_data():
    i = Indexer()
    i.calc_industry_index()


## temp processor ##
def calc_size():
    i = Indexer()
    i.calc_size_index()

def calc_style():
    i = Indexer()
    i.calc_style_index()

def calc_industry():
    i = Indexer()
    i.calc_industry_index()


## score index ##
def score_index():
    inds = IndexScorer('20000000')
    # inds.make_data()
    # inds.score_data()
    inds.calculate_score_ratings()

def save_mshome_data():
    ms = MSHomeProcessor()
    ms.save_data()

def save_mshome_rank():
    ms = MSHomeProcessor()
    ms.make_rank_data()
