from marketsignal.tasks import index_industry_data, score_data, init_ohlcv_csv_save
from stockapi.concurrent_tasks.bm import scrape_today_bm

from stockapi.models import FinancialRatio, OHLCV
import pandas as pd
import os
import pickle

print(os.getcwd())
os.chdir('./data/data')
files = os.listdir()
total_num = len(files)

done_num = 1
for filename in files:
    log = open('../../log.txt', 'w')
    code = filename[:6]
    df = pd.read_csv(filename)
    df['0'] = [str(data).zfill(6) for data in df['0']]
    data_list = []
    for i in range(len(df)):
        row = df.ix[i]
        date = str(row[1])[:8]
        code = str(row[0])[:6]
        open_price = int(row[2])
        high_price = int(row[3])
        low_price = int(row[4])
        close_price = int(row[5])
        volume = int(row[6])
        ohlcv_inst = OHLCV(date=date,
                           code=code,
                           open_price=open_price,
                           high_price=high_price,
                           low_price=low_price,
                           close_price=close_price,
                           volume=volume)
        data_list.append(ohlcv_inst)
    OHLCV.objects.bulk_create(data_list)
    uniq_dates = OHLCV.objects.filter(code=code).distinct('date')
    OHLCV.objects.filter(code=code).exclude(id__in=uniq_dates).delete()
    print('{} done: {}% done'.format(code, str(int((done_num/total_num)*100))))
    done_num += 1
    log.writelines(code + '\n')
    log.close()




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
