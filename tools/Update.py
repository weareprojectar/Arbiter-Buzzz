## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/8
## @Details 데이터 업데이트 등

import os
import pandas as pd
from stockapi.models import Ticker, OHLCV

DATA_PATH = os.getcwd() + '/arbiter/data/'

class Update:

    def __init__(self):
        os.chdir(DATA_PATH)
        self.files = os.listdir()

    def init_db_with_ohlcv(self):
        data_count = 1
        data_list = []
        for filename in self.files:
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
            if data_count % 500 == 0:
                OHLCV.objects.bulk_create(data_list)
                print('Saved data to db')
                data_list = []
        OHLCV.objects.bulk_create(data_list)
        print('Saved data to db')

    def save_ohlcv_data_to_pg(self):
        clean_ohlcv_file = [filename for filename in self.files if filename == 'clean_ohlcv.csv'][0]
        df = pd.read_csv(clean_ohlcv_file)

        total_data_num = len(df)
        data_saved = 1
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
            ohlcv_inst.save()
            print('{} data saved: {}% done'.format(data_saved, data_saved//total_data_num))
            data_saved += 1
