import pandas as pd
from datetime import datetime

from restapi.models import Info, Ticker, OHLCV, Specs

DATA_PATH = 'C:/Users/hori9/Desktop/MINED/devcode/data'

class Processor(object):
    def __init__(self, filter_date=False):
        date = datetime.now().strftime('%Y%m%d')
        tickers = Ticker.objects.filter(date=date).values_list('code')
        # self.ticker_list = [ticker[0] for ticker in tickers]
        self.ticker_list = ['005930', '000660', '005380', '005490', '035420', '051910',
                            '105560', '012330', '015760', '032830', '068270', '091990',
                            '130960', '263750', '086900', '003670', '034230', '036490',
                            '253450', '046890', '151910']
        self.ind_list = ['전기전자', '전기전자', '운수장비', '철강금속', '서비스업',
                         '화학', '기타금융업', '운수장비', '전기가스', '보험업',
                         '제약', '도매', '방송서비스', '디지털컨텐츠', '제약',
                         '비금속', '오락문화', '반도체', '오락문화', '반도체', 'IT부품']
        if not filter_date:
            last_year = str(datetime.now().year - 1)
            last_month = datetime.now().month - 1 or 12
            last_month = str(last_month).zfill(2)
            filter_date = last_year + last_month + '00'
            self.filter_date = filter_date

    def get_data(self):
        self._make_data()
        # print(self.ohlcv_df)
        # print(self.vol_df)

    def _make_data(self):
        self.ohlcv_list = []
        self.volume_list = []
        for ticker in self.ticker_list:
            print(ticker)
            ohlcv_qs = OHLCV.objects.filter(code=ticker).distinct('date')
            ohlcv = list(ohlcv_qs.exclude(date__lte=self.filter_date).values('date', 'close_price'))
            volume = list(ohlcv_qs.exclude(date__lte=self.filter_date).values_list('date', 'close_price', 'volume'))
            volume = [{'date': data[0], 'volume': data[1]*data[2]} for data in volume]
            self.ohlcv_list.append(ohlcv)
            self.volume_list.append(volume)
        for i in range(len(self.ticker_list)):
            print(i)
            ticker = self.ticker_list[i]
            ohlcv = self.ohlcv_list[i]
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
        self.ohlcv_df.to_csv('ohlcv_df.csv')
        self.vol_df.to_csv('vol_df.csv')

    def _create_df(self, ticker, ohlcv, col_name):
        df = pd.DataFrame(ohlcv)
        df.set_index('date', inplace=True)
        if col_name == 'close_price':
            df.rename(columns={col_name: ticker}, inplace=True)
        if col_name == 'volume':
            df.rename(columns={col_name: ticker}, inplace=True)
        return df

    def update_info(self):
        date = '20171219'
        info_list = []
        for i in range(len(self.ticker_list)):
            info_inst = Info(code=self.ticker_list[i],
                             date=date,
                             size_type='L',
                             industry=self.ind_list[i])
            info_list.append(info_inst)
        Info.objects.bulk_create(info_list)

    def get_data_local(self):
        self.ohlcv_df = pd.read_csv(DATA_PATH + '/ohlcv_df.csv', header=0)
        self.ohlcv_df.set_index('date', inplace=True)
        self.vol_df = pd.read_csv(DATA_PATH + '/vol_df.csv', header=0)
        self.vol_df.set_index('date', inplace=True)

    def set_return_portfolio(self):
        self.portfolio_data = self.ohlcv_df.pct_change()

    def bm_data(self):
        BM_qs = OHLCV.objects.filter(code='BM').distinct('date')
        BM_data = list(BM_qs.exclude(date__lte=self.filter_date).values('date', 'close_price'))
        BM = pd.DataFrame(BM_data)
        BM.set_index('date', inplace=True)
        BM.index = pd.to_datetime(BM.index)
        BM.rename(columns={'close_price': 'Benchmark'}, inplace=True)
        BM = BM.pct_change()
        self.portfolio_data.index = pd.to_datetime(self.portfolio_data.index)
        self.portfolio_data = pd.concat([self.portfolio_data, BM], axis=1)

    def dual_momentum(self):
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

    def calc_volatility(self):
        """ calculates volatility with rolling yearly standard deviation and returns the volatility array """
        self.volt = pd.DataFrame(self.portfolio_data).rolling(window=12).std().ix[-1]

    def calc_correlation(self):
        self.cor = self.portfolio_data.corr()['Benchmark']

    def save_mom_volt_cor_vol(self):
        self.dual_momentum()
        self.calc_volatility()
        self.calc_correlation()

        mom_s = 100 - self.mom.rank(ascending=False)
        volt_s = 100 - self.volt.rank(ascending=True)
        cor_s = 100 - self.cor.rank(ascending=True)
        vol_s = 100 - self.vol_df.ix[len(self.vol_df)-1].rank(ascending=False)
        date = '20171219'
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
                               volume=self.vol_df.ix[len(self.vol_df)-1][ticker],
                               momentum_score=momentum_score,
                               volatility_score=volatility_score,
                               correlation_score=correlation_score,
                               volume_score=volume_score,
                               total_score=total_score)
            specs_list.append(specs_inst)
        Specs.objects.bulk_create(specs_list)
