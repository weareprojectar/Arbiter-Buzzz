## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/17
## @Details 로컬에 존재하는 데이터를 서버로 전송, 서버에 있는 데이터를 로컬로 저장

import os, time, datetime
import pandas as pd
import numpy as np
import simplejson as json

from .Tracker import timeit

from defacto.models import AgentData, ScoreData


class DataImport(object):
    def __init__(self):
        os.chdir('./buzzz/')
        os.chdir('./data/agent_data/')
        print(os.getcwd())
        self.agent_file = [json for json in os.listdir()]
        agent_tuple = AgentData.objects.all().values_list('code')
        agent_list = sorted(list(set([x[0] + '.csv' for x in agent_tuple])))
        self.agent_file = [filename for filename in self.agent_file if filename not in agent_list]
        print(len(agent_list), len(self.agent_file), 'left')
        os.chdir('..')
        os.chdir('./score_data/')
        print(os.getcwd())
        self.score_file = [json for json in os.listdir()]
        score_tuple = ScoreData.objects.all().values_list('code')
        score_list = sorted(list(set([x[0] + '.csv' for x in score_tuple])))
        self.score_file = [filename for filename in self.score_file if filename not in score_list]
        os.chdir('..')
        print(len(score_list), len(self.score_file), 'left')

    @timeit
    def send_agent_data(self):
        for filename in self.agent_file:
            start = time.time()
            agent_df = pd.read_csv('./agent_data/{}'.format(filename), sep=',', encoding='CP949')
            agent_list = []
            for row_n in range(agent_df.shape[0]):
                date,code,ind_possession,for_possession,ins_possession,cor_possession,ind_apps,for_apps,ins_apps,cor_apps,lead_agent= list(agent_df.ix[row_n])
                # print(date.replace('-',''),code.zfill(6),ind_possession,for_possession,ins_possession,cor_possession,ind_apps,for_apps,ins_apps,cor_apps,lead_agent)
                agent_inst = AgentData(date=date.replace('-',''),
                                        code=str(code)[:6].zfill(6),
                                        ind_possession = ind_possession,
                                        for_possession = for_possession,
                                        ins_possession = ins_possession,
                                        cor_possession = cor_possession,
                                        ind_apps = ind_apps,
                                        for_apps = for_apps,
                                        ins_apps = ins_apps,
                                        cor_apps = cor_apps,
                                        lead_agent = lead_agent)
                agent_list.append(agent_inst)
            AgentData.objects.bulk_create(agent_list)
            end = time.time()
            print('save success', 'time :{}'.format(end-start))
            ## test df count and db count ##

    @timeit
    def send_score_data(self):
        for filename in self.score_file:
            start = time.time()
            score_df = pd.read_csv('./agent_data/{}'.format(filename), sep=',', encoding='CP949')
            score_list = []
            for row_n in range(score_df.shape[0]):
                date,code,absolute_score,relative_score,total_score,score_rank,rank_change,score_change = list(score_df.ix[row_n])
                # print(date,code.zfill(6),absolute_score,relative_score,total_score,score_rank,rank_change,score_change)
                score_inst = ScoreData(date = date.replace('-',''),
                                    code = str(code).zfill(6),
                                    absolute_score = absolute_score,
                                    relative_score = relative_score,
                                    total_score = total_score,
                                    score_rank = score_rank,
                                    rank_change = rank_change,
                                    score_change = score_change)
                score_list.append(score_inst)
            ScoreData.objects.bulk_create(score_list)
            end = time.time()
            print('save success', 'time :{}'.format(end-start))
            ## test df count and db count ##
