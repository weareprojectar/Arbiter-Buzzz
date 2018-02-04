## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/8
## @Details 데이터 업데이트 등

import os
import pandas as pd
from stockapi.models import Ticker, OHLCV, Info

DATA_PATH = os.getcwd() + '/arbiter/data/'
LOG_PATH = os.getcwd() + '/arbiter/log/'

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
