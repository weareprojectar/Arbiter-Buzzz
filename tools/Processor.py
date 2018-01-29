## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/1/2
## @Details 종목 점수 매김과 오늘의 포트폴리오 생성

import pandas as pd
import numpy as np
from datetime import datetime
import time

from restapi.models import Info, Ticker, OHLCV, Specs
from portfolio.models import TodayPortfolio
from portfolio.analysis import InitialPortfolio

DATA_PATH = 'C:/Users/hori9/Desktop/MINED/devcode/data'


class Processor(object):
    def __init__(self, filter_date=False):
        date = datetime.now().strftime('%Y%m%d')
        tickers = Ticker.objects.filter(date=date).values_list('code')
        # self.ticker_list = ['005930', '000660', '005380', '005490']
        self.ticker_list = [ticker[0] for ticker in list(tickers)]
        if not filter_date:
            last_year = str(datetime.now().year - 1)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date

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
            ticker_price = [{'date': data[1], 'close_price': data[2]} for data in ohlcv_qs if data[0] == ticker]
            ticker_volume = [{'date': data[1], 'volume': data[3]} for data in ohlcv_qs if data[0] == ticker]
            self.price_list.append(ticker_price)
            self.volume_list.append(ticker_volume)
        end = time.time()
        print('time took: ', str(end-start))

        start = time.time()
        for i in range(len(self.ticker_list)):
            print(i)
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

    def score_data(self):
        self._get_data_local()
        self.vol = (self.ohlcv_df * self.vol_df).ix[-1]
        self._set_return_portfolio()
        self._add_bm_data()
        self._save_mom_volt_cor_vol()

    def _get_data_local(self):
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0, index_col='date', parse_dates=True)
        self.vol_df = pd.read_csv(DATA_PATH + '/vol_df.csv', header=0, index_col='date', parse_dates=True)

    def _set_return_portfolio(self):
        self.portfolio_data = self.ohlcv_df.pct_change()

    def _add_bm_data(self):
        BM_qs = OHLCV.objects.filter(code='BM')
        BM_data = list(BM_qs.exclude(date__lte=self.filter_date).values('date', 'close_price'))
        BM = pd.DataFrame(BM_data)
        BM.set_index('date', inplace=True)
        BM.index = pd.to_datetime(BM.index)
        BM.rename(columns={'close_price': 'Benchmark'}, inplace=True)
        BM = BM.pct_change()
        self.portfolio_data.index = pd.to_datetime(self.portfolio_data.index)
        self.portfolio_data = pd.concat([self.portfolio_data, BM], axis=1)
        self.portfolio_data.fillna(0, inplace=True)

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

    def _save_mom_volt_cor_vol(self):
        self._dual_momentum()
        self._calc_volatility()
        self._calc_correlation()

        mom_s = self.mom.rank(ascending=True)
        mom_s = (mom_s/mom_s.max())*100
        volt_s = self.volt.rank(ascending=False)
        volt_s = (volt_s/volt_s.max())*100
        cor_s = self.cor.rank(ascending=False)
        cor_s = (cor_s/cor_s.max())*100
        vol_s = self.vol.rank(ascending=True)
        vol_s = (vol_s/vol_s.max())*100

        date = datetime.now().strftime('%Y%m%d')
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

    def make_todays_portfolio(self):
        # set BM as the standard for checking recent updated dates
        recent_date = Specs.objects.filter(code='005930').order_by('-date').first().date
        print('Recent date: ', recent_date)
        specs = Specs.objects.filter(date=recent_date)
        specs = list(specs.values_list('code', 'momentum_score', 'correlation_score', 'volume_score'))
        rank_list = []
        scores = []
        for spec in specs:
            ticker = spec[0]
            rank_score = (spec[1] + spec[2] + spec[3])/3
            rank_list.append([ticker, rank_score])
            scores.append(rank_score)
        cut_score = int(sorted(scores)[-10:][0])
        print('Cut score: ', str(cut_score))
        rank_list = list(filter(lambda x: x[1] > cut_score, rank_list))
        top_tickers = [score_data[0] for score_data in rank_list]
        ticker_count = len(top_tickers)
        print('Top score tickers: ', top_tickers)
        print('Ticker count: ', str(ticker_count))

        year = recent_date[:4]
        month = recent_date[4:6]
        last_year = str(int(year) - 5)
        last_month = int(month) - 1 or 12
        last_month = str(last_month).zfill(2)
        filter_date = last_year + last_month + '00'
        print('Filter date: ', filter_date)

        def create_df(ticker, ohlcv):
            df = pd.DataFrame(ohlcv)
            df.set_index('date', inplace=True)
            df.rename(columns={'close_price': ticker}, inplace=True)
            return df

        ohlcv_df = pd.DataFrame()
        # setting ohlcv_list
        init_qs = OHLCV.objects.filter(code__in=top_tickers)
        filtered_qs = init_qs.exclude(date__lte=filter_date).order_by('date')
        ohlcv_qs = filtered_qs.values_list('code', 'date', 'close_price')
        ohlcv_list = []
        for ticker in top_tickers:
            ticker_ohlcv = [{'date': data[1], 'close_price': data[2]} for data in ohlcv_qs if data[0] == ticker]
            ohlcv_list.append(ticker_ohlcv)

        if ticker_count == 0:
            pass
        elif ticker_count == 1:
            ticker = top_tickers[0]
            ohlcv = ohlcv_list[0]
            ohlcv_df = create_df(ticker, ohlcv)
        else:
            for i in range(ticker_count):
                ticker = top_tickers[i]
                ohlcv = ohlcv_list[i]
                if i == 0:
                    df = create_df(ticker, ohlcv)
                else:
                    temp_df = create_df(ticker, ohlcv)
                    df = pd.concat([df, temp_df], axis=1)
            df.index = pd.to_datetime(df.index)
            ohlcv_df = df
        print('OHLCV DF: ', ohlcv_df.tail(5))

        # returns df
        R = ohlcv_df.resample('M').last().pct_change()
        R.dropna(how='all', inplace=True)
        # monthly close df
        monthly_close = ohlcv_df.resample('M').last()
        monthly_close.dropna(how='all', inplace=True)

        def _bm_specs(period='M'):
            BM_qs = OHLCV.objects.filter(code='BM').distinct('date')
            BM_data = list(BM_qs.exclude(date__lte=filter_date).values('date', 'close_price'))
            BM = pd.DataFrame(BM_data)
            BM.set_index('date', inplace=True)
            BM.index = pd.to_datetime(BM.index)
            BM.rename(columns={'close_price': 'Benchmark'}, inplace=True)
            BM_R = BM.resample(period).last().pct_change()
            BM_R.dropna(how='all', inplace=True)
            W = pd.Series([1], index=['Benchmark'])
            return _backtest_port(W, BM_R)

        def _backtest_port(W=None, BM=None):
            W_R = W*BM
            WR = W_R.sum(axis=1)
            port_ret = WR.mean()
            port_var = WR.std()
            yield_curve = (WR + 1).cumprod()
            return WR, port_ret, port_var, yield_curve

        def _sharpe_ratio(r, bm_r, v):
            return (r - bm_r)/v

        def _dual_momentum():
            for i in range(1, 13):
                momentum = (monthly_close - monthly_close.shift(i))/monthly_close.shift(i)
                if i == 1:
                    temp = momentum
                else:
                    temp += momentum
            mom = temp/12
            # return mom.ix[-1]
            return mom.fillna(0)

        def _volatility():
            # return self.R.rolling(window=12).std().ix[-1]
            return R.rolling(window=12).std().fillna(0)

        def _correlation():
            corr = R.copy()
            corr['Eq_weight'] = list(pd.DataFrame(corr.values.T*(1.0/len(corr.columns))).sum())
            return corr.corr().ix[-1][:-1]

        def EAA(mom, vol, corr):
            cash_amount = (len(mom) - len(mom[mom > 0]))/len(mom)
            stock_amount = 1 - cash_amount
            eaa_amount = (1 - corr[mom > 0])/vol[mom > 0]
            stock_amount = stock_amount*eaa_amount/eaa_amount.sum()
            return cash_amount, stock_amount

        mom = _dual_momentum()
        print('Momentum: ', mom.tail(5))
        vol = _volatility()
        print('Volatility: ', vol.tail(5))
        corr = _correlation()
        print('Correlation: ', corr)
        returns_list = []
        for date in range(len(R)):
            _, stock_amt = EAA(mom.ix[date], vol.ix[date], corr)
            returns = ( R.ix[date] * (stock_amt/stock_amt.sum()) ).fillna(0)
            returns_list.append(returns.sum())
        print('Returns list: ', returns_list)
        weights = []
        for ticker in top_tickers:
            wt_df = stock_amt/stock_amt.sum()
            try:
                weight = wt_df[ticker]
            except KeyError:
                weight = 0
            weights.append(float(format(round(weight, 4), '.4f')))
        port_ratio = []
        name_list = []
        for i in range(len(top_tickers)):
            if weights[i] != 0:
                name = Ticker.objects.filter(code=top_tickers[i]).first().name
                port_ratio.append([top_tickers[i], weights[i]])
                name_list.append(name)
            else:
                continue
        print('Weights: ', weights)
        print('Portfolio ratio: ', port_ratio)

        wr = pd.DataFrame(returns_list)
        r = wr.mean()[0]
        v = wr.std()[0]
        yc = (wr + 1).cumprod()
        BM_wr, BM_r, BM_v, BM_yc = _bm_specs()
        sr = _sharpe_ratio(r, BM_r, v)
        yield_r = (yc.ix[len(yc) - 1] - 1)[0]
        yc.index = BM_yc.index
        bt = pd.concat([yc, BM_yc], axis=1)
        bt.columns = ['Portfolio', 'Benchmark']

        def change_bt_format(bt):
            new_data = dict()
            for column in bt.columns:
                ret_data = list()
                dates = bt.index.astype(np.int64)//1000000 # pandas timestamp returns in microseconds, divide by million
                for i in range(len(bt)):
                    data = bt.ix[i]
                    date = dates[i]
                    ret_data.append([float(date), float(format(round(data[column], 4), '.4f'))])
                new_data[column] = ret_data
            return new_data

        new_bt = change_bt_format(bt)
        print('Portfolio mean return: ', str(r))
        print('Portfolio mean variance: ', str(v))
        print('Sharpe ratio: ', str(sr))
        print('Portfolio return: ', str(yield_r))
        print('Portfolio backtest results: ', new_bt)

        mom_s, volt_s, cor_s, vol_s, tot_s = 0, 0, 0, 0, 0
        for i in range(len(port_ratio)):
            code = port_ratio[i][0]
            name = name_list[i]
            port_ratio[i][0] = name
            specs = Specs.objects.filter(code=code).order_by('-date').first()
            weight = port_ratio[i][1]
            mom_s += int(specs.momentum_score*weight)
            volt_s += int(specs.volatility_score*weight)
            cor_s += int(specs.correlation_score*weight)
            vol_s += int(specs.volume_score*weight)
            tot_s += int(((specs.momentum_score + specs.volatility_score + specs.correlation_score + specs.volume_score)/4)*weight)

        result_json_data = {
            'port_situation': port_ratio,
            'port_specs': [tot_s, mom_s, volt_s, cor_s, vol_s],
            'port_info': {
                'port_return': float(format(round(yield_r, 3)*100, '.3f')),
                'port_mean_return': float(format(round(r, 3)*100, '.3f')),
                'port_mean_var': float(format(round(v, 3)*100, '.3f')),
                'sharpe_ratio': float(format(round(sr, 3)*100, '.3f'))
            },
            'backtest_results': new_bt
        }

        date = datetime.now().strftime('%Y%m%d')
        today_port_inst = TodayPortfolio(date=date, portfolio=result_json_data)
        today_port_inst.save()
        print('Data saved')
