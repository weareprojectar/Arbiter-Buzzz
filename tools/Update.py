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
            print('Added {} to db'.format(filename))
        OHLCV.objects.bulk_create(data_list)
        print('Saved data to db')
