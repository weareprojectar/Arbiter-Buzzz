from marketsignal.tasks import index_industry_data, score_data, init_ohlcv_csv_save
from stockapi.concurrent_tasks.bm import scrape_today_bm

from stockapi.models import (
    FinancialRatio,
    OHLCV,
    KospiWeeklyBuy,
    KosdaqWeeklyBuy,
    KospiWeeklySell,
    KosdaqWeeklySell,
)
import pandas as pd
import os
import pickle

os.chdir('./data')
print(os.getcwd())
files = [filename for filename in os.listdir() if '.csv' in filename ]
total_num = len(files)
print(total_num)

loop_num = 1
for csv_file in files:
    df = pd.read_csv(csv_file, engine='python', encoding='cp949')
    codes = list(set(df['code']))
    for code in codes:
        print('Filter {}'.format(code))
        tmp = df[df['code'] == code]
        data_list = []
        for i in tmp.index:
            row = tmp.ix[i]
            inst = OHLCV(date=row['date'],
                         code=code,
                         open_price=row['open_price'],
                         high_price=row['high_price'],
                         low_price=row['low_price'],
                         close_price=row['close_price'],
                         volume=row['volume'])
            data_list.append(inst)
        OHLCV.objects.bulk_create(data_list)
        print('{}: successfully inserted {} data'.format(loop_num, code))
        loop_num += 1

# done = 1
# for filename in files:
#     df = pd.read_csv(filename)
#     df.drop(['Unnamed: 0'], axis=1, inplace=True)
#     buy_df = df[df['buysell'] == 'buy']
#     sell_df = df[df['buysell'] == 'sell']
#
#     buy_data_list = []
#     for i in buy_df.index:
#         row = buy_df.ix[i]
#         buy_data_inst = KosdaqWeeklyBuy(
#             date=str(row['date']),
#             code=str(row['code']).zfill(6),
#             name=str(row['name']),
#             individual=int(row['individual']),
#             foreign_retail=int(row['foreign_retail']),
#             institution=int(row['institution']),
#             financial=int(row['financial']),
#             insurance=int(row['insurance']),
#             trust=int(row['trust']),
#             etc_finance=int(row['etc_finance']),
#             bank=int(row['bank']),
#             pension=int(row['pension']),
#             private=int(row['private']),
#             nation=int(row['nation']),
#             etc_corporate=int(row['etc_corporate']),
#             foreign=int(row['foreign'])
#         )
#         buy_data_list.append(buy_data_inst)
#     KosdaqWeeklyBuy.objects.bulk_create(buy_data_list)
#     print('Saved {} buy data'.format(filename[:6]))
#
#     sell_data_list = []
#     for j in sell_df.index:
#         row = sell_df.ix[j]
#         sell_data_inst = KosdaqWeeklySell(
#             date=str(row['date']),
#             code=str(row['code']).zfill(6),
#             name=str(row['name']),
#             individual=int(row['individual']),
#             foreign_retail=int(row['foreign_retail']),
#             institution=int(row['institution']),
#             financial=int(row['financial']),
#             insurance=int(row['insurance']),
#             trust=int(row['trust']),
#             etc_finance=int(row['etc_finance']),
#             bank=int(row['bank']),
#             pension=int(row['pension']),
#             private=int(row['private']),
#             nation=int(row['nation']),
#             etc_corporate=int(row['etc_corporate']),
#             foreign=int(row['foreign'])
#         )
#         sell_data_list.append(sell_data_inst)
#     KosdaqWeeklySell.objects.bulk_create(sell_data_list)
#     print('Saved {} sell data'.format(filename[:6]))
#
#     print('{} Saved {}'.format(done, filename))
#
#     uniq_buy = KosdaqWeeklyBuy.objects.filter(code=filename[:6]).distinct('date')
#     KospiWeeklyBuy.objects.filter(code=filename[:6]).exclude(id__in=uniq_buy).delete()
#
#     uniq_sell = KosdaqWeeklySell.objects.filter(code=filename[:6]).distinct('date')
#     KospiWeeklySell.objects.filter(code=filename[:6]).exclude(id__in=uniq_sell).delete()
#     print('Deleted redundant/duplicate data')
#     done += 1

# done_num = 1
# for filename in files:
#     log = open('../../log.txt', 'w')
#     code = filename[:6]
#     df = pd.read_csv(filename)
#     df['0'] = [str(data).zfill(6) for data in df['0']]
#     data_list = []
#     for i in range(len(df)):
#         row = df.ix[i]
#         date = str(row[1])[:8]
#         code = str(row[0])[:6]
#         open_price = int(row[2])
#         high_price = int(row[3])
#         low_price = int(row[4])
#         close_price = int(row[5])
#         volume = int(row[6])
#         ohlcv_inst = OHLCV(date=date,
#                            code=code,
#                            open_price=open_price,
#                            high_price=high_price,
#                            low_price=low_price,
#                            close_price=close_price,
#                            volume=volume)
#         data_list.append(ohlcv_inst)
#     OHLCV.objects.bulk_create(data_list)
#     uniq_dates = OHLCV.objects.filter(code=code).distinct('date')
#     OHLCV.objects.filter(code=code).exclude(id__in=uniq_dates).delete()
#     print('{} done: {}% done'.format(code, str(int((done_num/total_num)*100))))
#     done_num += 1
#     log.writelines(code + '\n')
#     log.close()




# os.chdir('./tmp')
#
# df = pd.read_csv('financialratio.csv', header=None)
#
# data_list = []
# for i in range(len(df)):
#     row = df.ix[i]
#     date = row[0]
#     code = row[1]
#     name = row[2]
#     debt_ratio = 0 if row[3] == '\\N' else row[3]
#     profit_ratio = 0 if row[4] == '\\N' else row[4]
#     net_profit_ratio = 0 if row[5] == '\\N' else row[5]
#     consolidate_profit_ratio = 0 if row[6] == '\\N' else row[6]
#     net_ROE = 0 if row[7] == '\\N' else row[7]
#     consolidate_ROE = 0 if row[8] == '\\N' else row[8]
#     revenue_growth = 0 if row[9] == '\\N' else row[9]
#     profit_growth = 0 if row[10] == '\\N' else row[10]
#     net_profit_growth = 0 if row[11] == '\\N' else row[11]
#     f_inst = FinancialRatio(date=date,
#                             code=code,
#                             name=name,
#                             debt_ratio=debt_ratio,
#                             profit_ratio=profit_ratio,
#                             net_profit_ratio=net_profit_ratio,
#                             consolidate_profit_ratio=consolidate_profit_ratio,
#                             net_ROE=net_ROE,
#                             consolidate_ROE=consolidate_ROE,
#                             revenue_growth=revenue_growth,
#                             profit_growth=profit_growth,
#                             net_profit_growth=net_profit_growth)
#     data_list.append(f_inst)
#
# FinancialRatio.objects.bulk_create(data_list)
