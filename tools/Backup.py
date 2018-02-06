## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/4
## @Details 데이터 업데이트 등

import os
import pandas as pd
from stockapi.models import (
    Ticker,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinacial,
    BuySell,
)

BACKUP_PATH = os.getcwd() + '/arbiter-buzzz/backup/'


class Backup:
    def __init__(self):
        os.chdir(BACKUP_PATH)
        print('Backup ready')

    def ticker_backup(self):
        tickers = Ticker.objects.values_list('date', 'name', 'code', 'market_type')
        tickers = list(tickers)
        df = pd.DataFrame(tickers)
        df.to_csv('ticker.csv', index=False)
        print('Ticker backup complete')

        # df_check = pd.read_csv('ticker.csv')
        # print(df_check)

    def info_backup(self):
        info = Info.objects.values_list('code',
                                        'name',
                                        'date',
                                        'size_type',
                                        'style_type',
                                        'market_type',
                                        'face_val',
                                        'stock_nums',
                                        'price',
                                        'market_cap',
                                        'market_cap_rank',
                                        'industry',
                                        'foreign_limit',
                                        'foreign_possession',
                                        'foreign_ratio',
                                        'per',
                                        'eps',
                                        'pbr',
                                        'bps',
                                        'industry_per',
                                        'yield_ret',)
        info = list(info)
        df = pd.DataFrame(info)
        df.to_csv('info.csv', index=False)
        print('Info backup complete')

        # df_check = pd.read_csv('info.csv')
        # print(df_check)

    def financial_backup(self):
        financial = Financial.objects.values_list('code',
                                                  'name',
                                                  'date',
                                                  'revenue',
                                                  'profit',
                                                  'net_profit',
                                                  'consolidate_profit',
                                                  'asset',
                                                  'debt',
                                                  'capital',)
        financial = list(financial)
        df = pd.DataFrame(financial)
        df.to_csv('financial.csv', index=False)
        print('Financial backup complete')

        # df_check = pd.read_csv('financial.csv')
        # print(df_check)

    def financialratio_backup(self):
        financial = FinancialRatio.objects.values_list('date',
                                                       'code',
                                                       'name',
                                                       'debt_ratio',
                                                       'profit_ratio',
                                                       'net_profit_ratio',
                                                       'consolidate_profit_ratio',
                                                       'net_ROE',
                                                       'consolidate_ROE',
                                                       'revenue_growth',
                                                       'profit_growth',
                                                       'net_profit_growth',)
        financial = list(financial)
        df = pd.DataFrame(financial)
        df.to_csv('financialratio.csv', index=False)
        print('Financial Ratio backup complete')

        # df_check = pd.read_csv('financialratio.csv')
        # print(df_check)

    def quarterfinancial_backup(self):
        financial = QuarterFinacial.objects.values_list('date',
                                                        'code',
                                                        'name',
                                                        'revenue',
                                                        'profit',
                                                        'net_profit',
                                                        'consolidate_profit',
                                                        'profit_ratio',
                                                        'net_profit_ratio',)
        financial = list(financial)
        df = pd.DataFrame(financial)
        df.to_csv('quarterfinancial.csv', index=False)
        print('Quarter Finacial backup complete')

        # df_check = pd.read_csv('quarterfinancial.csv')
        # print(df_check)

    def buysell_backup(self):
        buysell = BuySell.objects.values_list('date',
                                              'code',
                                              'name',
                                              'institution',
                                              'foreigner',)
        buysell = list(buysell)
        df = pd.DataFrame(buysell)
        df.to_csv('buysell.csv', index=False)
        print('BuySell backup complete')

        df_check = pd.read_csv('buysell.csv')
        print(df_check)
