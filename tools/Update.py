## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/8
## @Details 데이터 업데이트 등

import os
import pandas as pd
import numpy as np
from stockapi.models import Ticker, OHLCV, Info

DATA_PATH = os.getcwd() + '/buzzz.co.kr/data/'
LOG_PATH = os.getcwd() + '/buzzz.co.kr/log/'

class Update:

    def __init__(self):
        os.chdir(DATA_PATH)
        self.files = sorted(os.listdir())

    def init_db_with_info(self):
        info_csv = self.files[0]
        df = pd.read_csv(info_csv)
        df.fillna(0, inplace=True)
        data_num = 1
        data_list = []
        for i in range(len(df)):
            info_inst = Info(code=df.ix[i][0],
                             name=df.ix[i][1],
                             date=df.ix[i][2],
                             size_type='',
                             style_type='',
                             market_type=df.ix[i][5],
                             face_val=df.ix[i][6],
                             stock_nums=df.ix[i][7],
                             price=df.ix[i][8],
                             market_cap=df.ix[i][9],
                             market_cap_rank=df.ix[i][10],
                             industry=df.ix[i][11],
                             foreign_limit=df.ix[i][12],
                             foreign_possession=df.ix[i][13],
                             foreign_ratio=df.ix[i][14],
                             per=df.ix[i][15],
                             eps=df.ix[i][16],
                             pbr=df.ix[i][17],
                             bps=df.ix[i][18],
                             industry_per=df.ix[i][19],
                             yield_ret=df.ix[i][20])
            data_list.append(info_inst)
            print('{} data added'.format(data_num))
            data_num += 1
        Info.objects.bulk_create(data_list)
        print('Data saved successful')

    def init_db_with_ohlcv(self, files):
        log = open(LOG_PATH + "ohlcv_db_init_log.txt", 'w')
        total_data_count = len(files)
        data_count = 1
        for filename in files:
            print('Starting sending {} data'.format(filename))
            data_list = []
            df = pd.read_csv(filename)
            try:
                for i in range(len(df)):
                    code = str(df.ix[i][0]).zfill(6)
                    date = str(df.ix[i][1])
                    open_price = int(df.ix[i][2])
                    high_price = int(df.ix[i][3])
                    low_price = int(df.ix[i][4])
                    close_price = int(df.ix[i][5])
                    volume = int(df.ix[i][6])
                    ohlcv_inst = OHLCV(code=code,
                                       date=date,
                                       open_price=open_price,
                                       high_price=high_price,
                                       low_price=low_price,
                                       close_price=close_price,
                                       volume=volume)
                    data_list.append(ohlcv_inst)
                done = str(int((data_count/total_data_count)*100))
                print('{} Added {} to db - {}% processed'.format(data_count, filename, done))
                OHLCV.objects.bulk_create(data_list)
            except:
                print('Error occurred!')
                log.write(str(filename[6:]) + '\n')
                print('Wrote to log, check log...')
                print('--------------------------')
            print('Successfully saved data to db')
            print('-----------------------------')
            data_count += 1
        print('DONE')
        log.close()

    def update_ohlcv_db(self, files, recent_update_date):
        total_data_count = len(files)
        data_count = 1
        data_list = []
        for filename in files:
            code = filename[:6]
            df = pd.read_csv(filename)
            print('Starting {}'.format(code))
            try:
                for i in range(len(df)):
                    if int(df.ix[i][1]) > int(recent_update_date):
                        row = df.ix[i]
                        date = str(int(row[1]))
                        open_price = row[2]
                        high_price = row[3]
                        low_price = row[4]
                        close_price = row[5]
                        volume = row[6]
                        ohlcv_inst = OHLCV(date=date,
                                           code=code,
                                           open_price=open_price,
                                           high_price=high_price,
                                           low_price=low_price,
                                           close_price=close_price,
                                           volume=volume)
                        data_list.append(ohlcv_inst)
                        done = str(int((data_count/total_data_count)*100))
                print('{} Added {} to db - {}% processed'.format(data_count, filename, done))
            except:
                print('Error! Skipping...')
                log = open(LOG_PATH + "ohlcv_db_init_log.txt", 'w')
                log.write(filename + '\n')
                log.close()
                print('Wrote to log file')
            data_count += 1
        OHLCV.objects.bulk_create(data_list)
        print('Update complete')

    def get_val_by_date_naver(self, code, str_date):
        found = False
        page = 1
        while not found:
            url = 'http://finance.naver.com/item/sise_day.nhn?code={}&page={}'.format(code, page)
            df = pd.read_html(url)[0]
            for i in range(len(df)):
                comp_date = str(df.ix[i][0]).replace('.', '')[:8]
                if str_date == comp_date:
                    df_row = df.ix[i]
                    close_price = int(df_row[1])
                    open_price = int(df_row[3])
                    high_price = int(df_row[4])
                    low_price = int(df_row[5])
                    volume = int(df_row[6])
                    ohlcv_inst = OHLCV(date=comp_date,
                                       code=code,
                                       open_price=open_price,
                                       high_price=high_price,
                                       low_price=low_price,
                                       close_price=close_price,
                                       volume=volume)
                    ohlcv_inst.save()
                    print('Added {} {} data'.format(code, str_date))
                    found = True
            if not found:
                if page > 4:
                    print('Data does not exist, breaking loop and skipping...')
                    found = True
                page += 1
                print('Data not found yet, requesting page {}'.format(page))

    def fillin_blank_ohlcv(self, start_date, end_date):
        # start_date = '20171218'
        # end_date = '20180201'
        # dates = list(OHLCV.objects.filter(date__gte=start_date).filter(date__lte=end_date).distinct('date').values_list('date', flat=True))
        df = pd.read_csv('ohlcv_df.csv')
        df['date'] = [data.replace('-', '') for data in list(df['Unnamed: 0'])]
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        problem_dataset = df.ix['2017-12-18':'2018-02-01']
        for date in problem_dataset.index:
            str_date = date.strftime('%Y%m%d')
            row = problem_dataset.ix[date]
            row.fillna(-1, inplace=True)
            problem_tickers = (row == -1)
            clean_row = row[problem_tickers]
            for ticker in clean_row.index:
                if OHLCV.objects.filter(code=ticker).filter(date=str_date).exists():
                    print('{} for {} already exists, skipping...'.format(ticker, str_date))
                    continue
                else:
                    print('{} for {} doesn\'t exist, scraping ohlcv, requesting data from naver'.format(ticker, str_date))
                    try:
                        code = str(int(ticker)) if type(int(ticker)) == 'int' else ticker
                        self.get_val_by_date_naver(code, str_date)
                    except:
                        code = ticker
                        self.get_val_by_date_naver(code, str_date)
            print('{} data scraped successfully'.format(str_date))

    def fillin_1(self):
        start_date = '2017-12-18'
        end_date = '2017-12-26'
        self.fillin_blank_ohlcv(start_date, end_date)

    def fillin_2(self):
        start_date = '2017-12-27'
        end_date = '2018-01-05'
        self.fillin_blank_ohlcv(start_date, end_date)

    def fillin_3(self):
        start_date = '2018-01-08'
        end_date = '2018-01-15'
        self.fillin_blank_ohlcv(start_date, end_date)

    def fillin_4(self):
        start_date = '2018-01-16'
        end_date = '2018-01-23'
        self.fillin_blank_ohlcv(start_date, end_date)

    def fillin_4(self):
        start_date = '2018-01-24'
        end_date = '2018-02-01'
        self.fillin_blank_ohlcv(start_date, end_date)

    def split_ohlcv_1(self):
        cut = len(self.files)//5
        files = self.files[:cut]
        self.update_ohlcv_db(files, '20180109')

    def split_ohlcv_2(self):
        cut = len(self.files)//5
        files = self.files[cut:2*cut]
        self.update_ohlcv_db(files, '20180109')

    def split_ohlcv_3(self):
        cut = len(self.files)//5
        files = self.files[2*cut:3*cut]
        self.update_ohlcv_db(files, '20180109')

    def split_ohlcv_4(self):
        cut = len(self.files)//5
        files = self.files[3*cut:4*cut]
        self.update_ohlcv_db(files, '20180109')

    def split_ohlcv_5(self):
        cut = len(self.files)//5
        files = self.files[4*cut:]
        self.update_ohlcv_db(files, '20180109')
