## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/8
## @Details 데이터 업데이트 등

import os
import pandas as pd
from stockapi.models import Ticker, OHLCV, Info

DATA_PATH = os.getcwd() + '/arbiter/data/'

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
        data_count = 1
        for filename in files:
            data_list = []
            df = pd.read_csv(filename)
            for i in range(len(df)):
                code = str(df.ix[i][0]).zfill(6)
                date = str(df.ix[i][1])
                open_price = df.ix[i][2]
                high_price = df.ix[i][3]
                low_price = df.ix[i][4]
                close_price = df.ix[i][5]
                volume = int(df.ix[i][6])
                ohlcv_inst = OHLCV(code=code,
                                   date=date,
                                   open_price=open_price,
                                   high_price=high_price,
                                   low_price=low_price,
                                   close_price=close_price,
                                   volume=volume)
                data_list.append(ohlcv_inst)
            print('{} Added {} to db'.format(data_count, filename))
            data_count += 1
            OHLCV.objects.bulk_create(data_list)
            print('Saved data to db')
        print('DONE')

    def split_ohlcv_1(self):
        cut = len(self.files)//5
        files = self.files[:cut]
        self.init_db_with_ohlcv(files)

    def split_ohlcv_2(self):
        cut = len(self.files)//5
        files = self.files[cut:2*cut]
        self.init_db_with_ohlcv(files)

    def split_ohlcv_3(self):
        cut = len(self.files)//5
        files = self.files[2*cut:3*cut]
        self.init_db_with_ohlcv(files)

    def split_ohlcv_4(self):
        cut = len(self.files)//5
        files = self.files[3*cut:4*cut]
        self.init_db_with_ohlcv(files)

    def split_ohlcv_5(self):
        cut = len(self.files)//5
        files = self.files[4*cut:]
        self.init_db_with_ohlcv(files)
