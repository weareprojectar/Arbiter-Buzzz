from marketsignal.tasks import index_industry_data, score_data, init_ohlcv_csv_save
from stockapi.concurrent_tasks.bm import scrape_today_bm

from stockapi.models import FinancialRatio
import pandas as pd
import os

print(os.getcwd())
os.chdir('./tmp')

df = pd.read_csv('financialratio.csv', header=None)

data_list = []
for i in range(len(df)):
    row = df.ix[i]
    date = row[0]
    code = row[1]
    name = row[2]
    debt_ratio = 0 if row[3] == '\\N' else row[3]
    profit_ratio = 0 if row[4] == '\\N' else row[4]
    net_profit_ratio = 0 if row[5] == '\\N' else row[5]
    consolidate_profit_ratio = 0 if row[6] == '\\N' else row[6]
    net_ROE = 0 if row[7] == '\\N' else row[7]
    consolidate_ROE = 0 if row[8] == '\\N' else row[8]
    revenue_growth = 0 if row[9] == '\\N' else row[9]
    profit_growth = 0 if row[10] == '\\N' else row[10]
    net_profit_growth = 0 if row[11] == '\\N' else row[11]
    f_inst = FinancialRatio(date=date,
                            code=code,
                            name=name,
                            debt_ratio=debt_ratio,
                            profit_ratio=profit_ratio,
                            net_profit_ratio=net_profit_ratio,
                            consolidate_profit_ratio=consolidate_profit_ratio,
                            net_ROE=net_ROE,
                            consolidate_ROE=consolidate_ROE,
                            revenue_growth=revenue_growth,
                            profit_growth=profit_growth,
                            net_profit_growth=net_profit_growth)
    data_list.append(f_inst)

FinancialRatio.objects.bulk_create(data_list)
