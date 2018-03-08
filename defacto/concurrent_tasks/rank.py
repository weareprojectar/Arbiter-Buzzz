from __future__ import absolute_import, unicode_literals
from defacto.models import AgentData, ScoreData, RankData
from stockapi.models import Ticker
import pandas as pd
import time

def makeDataFrame():
    for agent in ['foreigner', 'institution', 'total']:
        if agent == 'total':
            score_qs = AgentData.objects.all()
        else:
            score_qs = AgentData.objects.filter(lead_agent=agent)
        last_date = score_qs.order_by('-date').first().date
        score_data = score_qs.filter(date=last_date).values_list('code', 'total_score','rank_change', 'lead_agent')
        cols = ['date','code','lead_agent','sign', 'total_score', 'rank_change']
        last_date_ticker = Ticker.objects.order_by('-date').first().date
        name_data = Ticker.objects.filter(code__in=ticker_list).filter(date=last_date_ticker).values_list('code','name')
        cols2 = ['code', 'name']
        rank_df = pd.DataFrame(columns=cols)
        rank_df['date'] = last_date
        rank_df['code'] = [x[0] for x in score_data]
        rank_df['total_score'] = [x[1] for x in score_data]
        rank_df['rank_change'] = [x[2] for x in score_data]
        rank_df['lead_agent'] = [x[3] for x in score_data]
        name_df = pd.DataFrame(columns=cols2)
        name_df['code'] = [x[0] for x in name_data]
        name_df['name'] = [x[1] for x in name_data]
        rank_df = pd.merge(rank_df, name_df, how='inner', on='code')
        cols3 = ['date', 'code', 'name', 'lead_agent', 'total_score', 'rank_change', 'sign']
        rank_df = rank_df[cols3]
        rank_df.loc[rank_df['rank_change'] > 0, 'sign'] = 'plus-line'
        rank_df.loc[rank_df['rank_change'] == 0, 'sign'] = ''
        rank_df.loc[rank_df['rank_change'] < 0, 'sign'] = 'minus-line'
        rank_df['rank_change'] = abs(rank_df['rank_change'])
        print(rank_df.isnull().sum())
        rank_df.dropna(axis=0, how='any', inplace=True)
        print(rank_df)
        do_list = {'foreigner':['foreigner_socre', 'foreigner_increase'], 'institution':['institution_score', 'institution_increase']}
        if agent in ['foreigner', 'institution']:
            score_rank = rank_df.sort_values(by=['total_score'], axis=0, ascending=False)
            score_rank = score_rank[:50]
            score_rank['cartegory'] = do_list[agent][0]
            print('------first-------')
            print(foreigner_score)
            start=time.time()
            score_rank_list = score_rank.tolist()
            score_list = []
            for row_n in range(len(score_rank_list)):
                print(score_rank_list[row_n])
                date, code, name, lead_agent, total_score, rank_change, sign, cartegory = score_rank_list[row_n]
                score_inst = RankData(date = date,
                                    code = str(code).zfill(6),
                                    name = name,
                                    lead_agent = lead_agent,
                                    total_score = float(format(total_score, '.2f')),
                                    rank_change = rank_change,
                                    sign = sign,
                                    cartegory = cartegory)
                score_list.append(score_inst)
            RankData.objects.bulk_create(score_list)
            end = time.time()
            print('save success', 'time :{}'.format(end-start))
            rank_change = rank_df[rank_df['sign'] == 'plus-line'].sort_values(by=['rank_change'], axis=0, ascending=False)
            rank_change = rank_change[:30]
            rank_change['cartegory'] = do_list[agent][1]
            print('------second-------')
            print(foreigner_rank_change)
            start=time.time()
            rank_change_list = rank_change.tolist()
            rank_list = []
            for row_n in range(len(rank_change_list)):
                print(rank_change_list[row_n])
                date, code, name, lead_agent, total_score, rank_change, sign, cartegory= rank_change_list[row_n]
                rank_inst = RankData(date = date,
                                    code = str(code).zfill(6),
                                    name = name,
                                    lead_agent = lead_agent,
                                    total_score = float(format(total_score, '.2f')),
                                    rank_change = rank_change,
                                    sign = sign,
                                    cartegory = cartegory)
                rank_list.append(rank_inst)
            RankData.objects.bulk_create(rank_list)
            end = time.time()
            print('save success', 'time :{}'.format(end-start))
        else:
            rank_change = rank_df[rank_df['sign'] == 'plus-line'].sort_values(by=['rank_change'], axis=0, ascending=False)
            rank_change = rank_change[:30]
            rank_change['cartegory'] = 'total_increase'
            print('------second-------')
            print(foreigner_rank_change)
            start=time.time()
            rank_change_list = rank_change.tolist()
            rank_list = []
            for row_n in range(len(rank_change_list)):
                print(rank_change_list[row_n])
                date, code, name, lead_agent, total_score, rank_change, sign, cartegory= rank_change_list[row_n]
                rank_inst = RankData(date = date,
                                    code = str(code).zfill(6),
                                    name = name,
                                    lead_agent = lead_agent,
                                    total_score = float(format(total_score, '.2f')),
                                    rank_change = rank_change,
                                    sign = sign,
                                    cartegory = cartegory)
                rank_list.append(rank_inst)
            RankData.objects.bulk_create(rank_list)
            end = time.time()
            print('save success', 'time :{}'.format(end-start))
