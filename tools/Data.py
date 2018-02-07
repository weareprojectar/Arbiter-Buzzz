## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/17
## @Details 로컬에 존재하는 데이터를 서버로 전송, 서버에 있는 데이터를 로컬로 저장

import os, time, datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import simplejson as json

from .Tracker import timeit

from stockapi.models import Ticker, OHLCV


class Data(object):
    def __init__(self, start_path):
        self.START_PATH = start_path
        self.TICKER_PATH = start_path + '/data'
        self.BM_PATH = start_path + '/data/bm'
        self.OHLCV_PATH = start_path + '/management/kiwoomapi/ohlcv'

    def _exists(self, directory, filename):
        full_path = directory + '/{}'.format(filename)
        return os.path.exists(full_path), full_path

    def _retrieve_data(self, directory, filename):
        os.chdir(directory)
        exists, full_path = self._exists(directory, filename)
        if exists:
            print('{} file exists, skipping download'.format(filename))
            return pd.read_csv(full_path, encoding='euc-kr', header=None)
        else:
            print('File does not exist, create first')

    def _retrieve_ticker(self):
        df = self._retrieve_data(self.TICKER_PATH, 'tickers.csv')
        return df

    def _retrieve_bm(self):
        df = self._retrieve_data(self.BM_PATH, 'BM.csv')
        return df

    def _retrieve_ohlcv(self, filename):
        df = self._retrieve_data(self.OHLCV_PATH, filename)
        return df

    @timeit
    def send_ticker(self):
        df = self._retrieve_ticker()
        tickers_list = []
        for row_n in range(len(df)):
            code, date, name, market_type = list(df.ix[row_n])
            ticker_inst = Ticker(code=code,
                                 date=date,
                                 name=name,
                                 market_type=market_type)
            tickers_list.append(ticker_inst)
        Ticker.objects.bulk_create(tickers_list)
        ## test df count and db count ##
        df_len = len(df)
        db_count = Ticker.objects.count()
        if df_len == db_count:
            print('Ticker instances successfully saved to database')
        else:
            print('Ticker instance count mismatch with the file')

    @timeit
    def send_bm(self):
        df = self._retrieve_bm()
        code = 'BM'
        ohlcv_list = []
        for row_n in range(len(df)):
            date, open_price, high_price, low_price, close_price, adj_close_price, volume = list(df.ix[row_n])
            ohlcv_inst = OHLCV(code=code,
                                date=str(date).replace('-', '')[:8],
                                open_price=open_price,
                                high_price=high_price,
                                low_price=low_price,
                                close_price=adj_close_price,
                                volume=volume)
            ohlcv_list.append(ohlcv_inst)
        OHLCV.objects.bulk_create(ohlcv_list)
        ## test df count and db count ##
        df_len = len(df)
        db_count = OHLCV.objects.filter(code=code).count()
        if df_len == db_count:
            print('{} OHLCV instances successfully saved to database'.format(code))
        else:
            print('{} OHLCV instance count mismatch with the file'.format(code))

    @timeit
    def send_ohlcv(self):
        ohlcv_files = [ohlcv_file for ohlcv_file in os.listdir(self.OHLCV_PATH) if '.csv' in ohlcv_file]
        done_count = 0
        for ohlcv_file in ohlcv_files:
            ticker = ohlcv_file.split('.')[0]
            if OHLCV.objects.filter(code=ticker).exists():
                done_count += 1
                print('{} Data exists, skipping {}'.format(str(done_count), ticker))
                continue
            else:
                df = self._retrieve_ohlcv(ohlcv_file)
                ohlcv_list = []
                for row_n in range(len(df)):
                    code = ohlcv_file.split('.')[0]
                    date, open_price, high_price, low_price, close_price, volume = list(df.ix[row_n])
                    ohlcv_inst = OHLCV(code=code,
                                       date=str(date)[:8],
                                       open_price=open_price,
                                       high_price=high_price,
                                       low_price=low_price,
                                       close_price=close_price,
                                       volume=volume)
                    ohlcv_list.append(ohlcv_inst)
                OHLCV.objects.bulk_create(ohlcv_list)
                ## test df count and db count ##
                df_len = len(df)
                db_count = OHLCV.objects.filter(code=code).count()
                if df_len == db_count:
                    done_count += 1
                    print('{} {} OHLCV instances successfully saved to database'.format(str(done_count), code))
                else:
                    print('{} OHLCV instance count mismatch with the file'.format(code))

    def update_ohlcv(self):
        upd_num = 0
        recent_update_date = Ticker.objects.order_by('date').last().date
        today_date = datetime.datetime.now().strftime('%Y%m%d')
        if recent_update_date != today_date:
            tickers = Ticker.objects.filter(date=today_date)
            for ticker in tickers:
                code = ticker.code
                if OHLCV.objects.filter(code=code).filter(date=today_date).exists():
                    print('{} {} already updated. Skipping...'.format(str(upd_num), code))
                    upd_num += 1
                    continue
                else:
                    url = "http://finance.naver.com/item/sise_day.nhn?code=" + code
                    print('{} {}'.format(str(upd_num), url))
                    df = pd.read_html(url, thousands='')
                    df = df[0]

                    ohlcv_list = []
                    index = 1
                    while index:
                        try:
                            date = str(df.ix[index][0].replace(".", ""))
                            if date == recent_update_date:
                                break
                            else:
                                open_price = int(df.ix[index][3].replace(",", ""))
                                high_price = int(df.ix[index][4].replace(",", ""))
                                low_price = int(df.ix[index][5].replace(",", ""))
                                close_price = int(df.ix[index][1].replace(",", ""))
                                volume = int(df.ix[index][6].replace(",", ""))
                                data = OHLCV(code=code,
                                             date=date,
                                             open_price=open_price,
                                             high_price=high_price,
                                             low_price=low_price,
                                             close_price=close_price,
                                             volume=volume)
                                ohlcv_list.append(data)
                                print(str(upd_num)+ ' added ' + code + ' data')
                                index += 1
                        except:
                            break
                    OHLCV.objects.bulk_create(ohlcv_list)
                    upd_num += 1

    def update_ohlcv_with_date(self, tickers):
        upd_num = 0
        total_num = len(tickers)
        # recent_update_date = OHLCV.objects.order_by('date').last().date
        recent_update_date = '20171215'
        today_date = '20180207'
        if recent_update_date != today_date:
            for ticker in tickers:
                code = ticker.code
                page = 1
                if OHLCV.objects.filter(code=code).filter(date=today_date).exists():
                    print('{} {} already updated. Skipping... {}%'.format(str(upd_num), code, str(int((upd_num/total_num)*100))))
                    upd_num += 1
                    continue
                else:
                    done = False
                    ohlcv_list = []
                    while not done:
                        url = "http://finance.naver.com/item/sise_day.nhn?code={}&page={}".format(code, page)
                        print('{} {}'.format(str(upd_num), url))
                        df = pd.read_html(url, thousands='')
                        df = df[0]
                        for i in range(1, len(df)):
                            date_check = df.ix[i][0]
                            if type(date_check) == float:
                                done = True
                                break
                            else:
                                comp_date = str(date_check).replace('.', '')[:8]
                            if comp_date == recent_update_date:
                                print('Date now: {}, ending loop and moving on'.format(comp_date))
                                done = True
                                break
                            else:
                                open_price = int(str(df.ix[i][3]).replace(",", ""))
                                high_price = int(str(df.ix[i][4]).replace(",", ""))
                                low_price = int(str(df.ix[i][5]).replace(",", ""))
                                close_price = int(str(df.ix[i][1]).replace(",", ""))
                                volume = int(str(df.ix[i][6]).replace(",", ""))
                                data = OHLCV(code=code,
                                             date=comp_date,
                                             open_price=open_price,
                                             high_price=high_price,
                                             low_price=low_price,
                                             close_price=close_price,
                                             volume=volume)
                                ohlcv_list.append(data)
                        if not done:
                            if page > 4:
                                print('Data does not exist anymore, breaking loop and skipping...')
                                done = True
                            page += 1
                            print('Data not done yet, requesting page {}'.format(page))
                    OHLCV.objects.bulk_create(ohlcv_list)
                    print('{} added {} data: {}% done'.format(upd_num, code, str(int((upd_num/total_num)*100))))
                    upd_num += 1

    def upd_ohlcv_1(self):
        today = '20180207'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker_list = ticker[:ticker_cut]
        self.update_ohlcv_with_date(ticker_list)

    def upd_ohlcv_2(self):
        today = '20180207'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker_list = ticker[ticker_cut:2*ticker_cut]
        self.update_ohlcv_with_date(ticker_list)

    def upd_ohlcv_3(self):
        today = '20180207'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker_list = ticker[2*ticker_cut:3*ticker_cut]
        self.update_ohlcv_with_date(ticker_list)

    def upd_ohlcv_4(self):
        today = '20180207'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker_list = ticker[3*ticker_cut:4*ticker_cut]
        self.update_ohlcv_with_date(ticker_list)

    def upd_ohlcv_5(self):
        today = '20180207'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker_list = ticker[4*ticker_cut:]
        self.update_ohlcv_with_date(ticker_list)

    def clean_ohlcv(self):
        today_date = datetime.datetime.now().strftime('%Y%m%d')
        tickers = Ticker.objects.filter(date=today_date)
        for ticker in tickers:
            ohlcv_qs = OHLCV.objects.filter(code=ticker.code)
            unique_qs = ohlcv_qs.distinct('date')
            ohlcv_qs.exclude(id__in=unique_qs).delete()
            print('{}: deleted duplicates'.format(ticker.code))

    def clean_bm(self):
        ohlcv_qs = OHLCV.objects.filter(code='BM')
        unique_qs = ohlcv_qs.distinct('date')
        ohlcv_qs.exclude(id__in=unique_qs).delete()
        print('BM duplicates deleted')

    # def _make_data(self, directory, filename, values):
    #     full_path = directory + '\\{}'.format(filename)
    #     data = pd.DataFrame(values)
    #     data.to_csv(full_path, index=False, header=False)
    #     print('{} file saved'.format(filename))
    #     return pd.read_csv(full_path, encoding='euc-kr', header=None)
    #
    # @property
    # def _ticker_values(self):
    #     ticker_qs = Ticker.objects.all()
    #     ticker_values = list(ticker_qs.values_list('code',
    #                                                'date',
    #                                                'name',
    #                                                'market_type'))
    #     return ticker_values
    #
    # def _ohlcv_values(self, ticker):
    #     ohlcv_qs = OHLCV.objects.filter(code=ticker)
    #     ohlcv_values = list(ohlcv_qs.values_list('code',
    #                                              'date',
    #                                              'open_price',
    #                                              'high_price',
    #                                              'low_price',
    #                                              'close_price',
    #                                              'volume'))
    #     return ohlcv_values
