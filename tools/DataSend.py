from defacto.models import AgentData, ScoreData

import pandas as pd
import os


class DataSend:
    def __init__(self):
        self.data_dir = './dev/data/'
        # self.dirs = ['kospi_agent/',
        #              'kosdaq_agent/',
        #              'kospi_final_score/',
        #              'kosdaq_final_score/']
        self.dirs = ['kosdaq_agent/',
                     'kosdaq_final_score/']

    def send_agent_data(self):
        for dirname in self.dirs:
            if 'agent' in dirname:
                print('Saving data init...')
            elif 'final_score' in dirname:
                continue
            os.chdir(self.data_dir + dirname)
            print(os.getcwd())
            files = os.listdir()
            for filename in files:
                file_date = (filename.split('.')[0]).replace('-', '')
                if int(file_date) <= 20130924:
                    print('Skipping {}'.format(file_date))
                    continue
                else:
                    print('Starting {}'.format(file_date))
                df = pd.read_csv(filename)
                df.fillna(0, inplace=True)
                data_list = []
                for i in range(len(df)):
                    row = df.ix[i]
                    date = str(row['date']).replace('-', '')[:8]
                    code = str(row['code']).zfill(6)[:6]
                    ind_possession = row['individual_possession']
                    for_possession = row['foreign_retail_possession']
                    ins_possession = row['institution_possession']
                    cor_possession = row['etc_corporate_possession']
                    ind_apps = row['individual_apps_tp']
                    for_apps = row['foreign_retail_apps_tp']
                    ins_apps = row['institution_apps_tp']
                    cor_apps = row['etc_corporate_apps_tp']
                    ad_inst = AgentData(date=date,
                                        code=code,
                                        ind_possession=ind_possession,
                                        for_possession=for_possession,
                                        ins_possession=ins_possession,
                                        cor_possession=cor_possession,
                                        ind_apps=ind_apps,
                                        for_apps=for_apps,
                                        ins_apps=ins_apps,
                                        cor_apps=cor_apps)
                    data_list.append(ad_inst)
                AgentData.objects.bulk_create(data_list)
                print('{} data saved completely'.format(filename))
            print('{} saved'.format(dirname))
            os.chdir('./../../../')
            print(os.getcwd())

    def send_score_data(self):
        for dirname in self.dirs:
            if 'agent' in dirname:
                continue
            elif 'final_score' in dirname:
                print('Saving data init...')
            os.chdir(self.data_dir + dirname)
            print(os.getcwd())
            files = os.listdir()
            for filename in files:
                df = pd.read_csv(filename)
                data_list = []
                for i in range(len(df)):
                    row = df.ix[i]
                    date = str(row['date']).replace('-', '')[:8]
                    code = str(row['code']).zfill(6)[:6]
                    absolute_score = row['absolute_score']
                    relative_score = row['relative_score']
                    total_score = row['total_score']
                    score_rank = row['total_rank']
                    rank_change = row['rank_change']
                    score_change = row['score_change']
                    lead_agent = row['lead_agent']
                    sd_inst = ScoreData(date=date,
                                        code=code,
                                        absolute_score=absolute_score,
                                        relative_score=relative_score,
                                        total_score=total_score,
                                        score_rank=score_rank,
                                        rank_change=rank_change,
                                        score_change=score_change,
                                        lead_agent=lead_agent)
                    data_list.append(sd_inst)
                ScoreData.objects.bulk_create(data_list)
                print('{} data saved completely'.format(filename))
            print('{} saved'.format(dirname))
            os.chdir('./../../../')
            print(os.getcwd())
