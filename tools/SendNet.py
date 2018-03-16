from defacto.models import AgentData, ScoreData
from stockapi.models import KospiWeeklyNet, KosdaqWeeklyNet

import pandas as pd
import os


class SendNet:
    def __init__(self):
        self.data_dir = './dev/data/'
        self.models = {
            'kospi': KospiWeeklyNet,
            'kosdaq': KosdaqWeeklyNet,
            'etf': KospiWeeklyNet
        }

    def send_net(self):
        os.chdir(self.data_dir)
        files = [filename for filename in os.listdir() if '.csv' in filename]
        for filename in files:
            market_type = filename.split('_')[0]
            df = pd.read_csv(filename)
            df.fillna(0, inplace=True)
            data_list = []
            for i in range(len(df)):
                row = df.ix[i]
                date = str(row['date'])[:8]
                code = str(row['code']).zfill(6)
                name = row['name']
                close_price = row['close_price']
                individual = row['individual']
                foreign_retail = row['foreign_retail']
                institution = row['institution']
                financial = row['financial']
                insurance = row['insurance']
                trust = row['trust']
                etc_finance = row['etc_finance']
                bank = row['bank']
                pension = row['pension']
                private = row['private']
                nation = row['nation']
                etc_corporate = row['etc_corporate']
                foreign = row['foreign']
                data_inst = self.models[market_type](date=date,
                                                     code=code,
                                                     name=name,
                                                     individual=individual,
                                                     foreign_retail=foreign_retail,
                                                     institution=institution,
                                                     financial=financial,
                                                     insurance=insurance,
                                                     trust=trust,
                                                     etc_finance=etc_finance,
                                                     bank=bank,
                                                     pension=pension,
                                                     private=private,
                                                     nation=nation,
                                                     etc_corporate=etc_corporate,
                                                     foreign=foreign)
                data_list.append(data_inst)
            self.models[market_type].objects.bulk_create(data_list)
            print('{} done'.format(filename))
