from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import re
import pandas as pd
import math
import time

from stockapi.models import (
    Ticker,
    OHLCV,
    StockInfo,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinancial,
)


class SejongScraper(object):
    def __init__(self, ticker):
        self.today = datetime.now().strftime('%Y%m%d')
        # self.ticker = Ticker.objects.filter(date=self.today).order_by('id')
        self.ticker = ticker
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        self.string = ['-','흑전','적전','적지','자본잠식']
        self.success = False
        # self.ticker_count = Ticker.objects.all().count()
        # self.ticker_cut = self.ticker_count//10
        # self.ticker_list = self.ticker[:self.ticker_cut]

    def scrape_sejong_financial(self):
        data_list = []
        start = time.time()
        for i in range(len(self.ticker)):
            for gubun_num in [1, 2]:
                url = 'http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?&no={}&gubun={}'.format(self.ticker[i].code, gubun_num)
                code = self.ticker[i].code
                name = self.ticker[i].name
                r = requests.get(url, headers= self.user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                df1= pd.read_html(url, thousands='')
                financial =  df1[1]
                for i in range(1,len(df1[1].columns)):
                    date = financial[[i]].iloc[0,0].replace('.','')[:6]
                    revenue = financial[[i]].iloc[1,0]
                    if type(revenue) == float:
                        revenue = 0
                    else:
                        revenue = financial[[i]].iloc[1,0].replace(',','')
                    profit = financial[[i]].iloc[2,0]
                    if type(profit) == float:
                        profit = 0
                    else:
                        profit = financial[[i]].iloc[2,0].replace(',','')
                    net_profit= financial[[i]].iloc[3,0]
                    if type(net_profit) == float:
                        net_profit=0
                    else:
                        net_profit= financial[[i]].iloc[3,0].replace(',','')
                    consolidate_profit = financial[[i]].iloc[4,0]
                    if type(consolidate_profit) == float:
                        consolidate_profit = 0
                    else:
                        consolidate_profit = financial[[i]].iloc[4,0].replace(',','')
                    total_asset = financial[[i]].iloc[5,0]
                    if type(total_asset) == float:
                        total_asset = 0
                    else:
                        total_asset = financial[[i]].iloc[5,0].replace(',','')
                    total_debt = financial[[i]].iloc[6,0]
                    if type(total_debt)==float:
                        total_debt = 0
                    else:
                        total_debt = financial[[i]].iloc[6,0].replace(',','')
                    total_capital = financial[[i]].iloc[7,0]
                    if type(total_capital) == float:
                        total_capital = 0
                    else:
                        total_capital = financial[[i]].iloc[7,0].replace(',','')
                    tmp = Financial(date=date,
                                    code=code,
                                    name=name,
                                    revenue=revenue,
                                    profit= profit,
                                    net_profit=net_profit,
                                    consolidate_profit=consolidate_profit,
                                    asset=total_asset,
                                    debt=total_debt,
                                    capital=total_capital)
                    data_list.append(tmp)
        end = time.time()
        Financial.objects.bulk_create(data_list)
        self.success = True
        return end-start, self.success

    def scrape_sejong_financialratio(self):
        data_list = []
        start = time.time()
        for i in range(len(self.ticker)):
            url = 'http://www.sejongdata.com/business_include_fr/table_main0_bus_01.html?&no='+ self.ticker[i].code
            code = self.ticker[i].code
            name = self.ticker[i].name
            r = requests.get(url, headers= self.user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            df1= pd.read_html(url, thousands='')
            financial_ratio = df1[4]
            for i in range(1,len(financial_ratio.columns)):
                date = financial_ratio[[i]].iloc[0,0].replace('.','')[:6]
                debt_ratio = financial_ratio[[i]].iloc[1,0]
                if type(debt_ratio) == float:
                    if math.isnan(debt_ratio):
                        debt_ratio = 0
                    else:
                        debt_ratio = debt_ratio
                elif debt_ratio in self.string:
                    debt_ratio = 0
                else:
                    debt_ratio = debt_ratio.replace(',','')
                profit_ratio = financial_ratio[[i]].iloc[2,0]
                if type(profit_ratio) == float:
                    if math.isnan(profit_ratio):
                        profit_ratio = 0
                    else:
                        profit_ratio = float(profit_ratio)
                elif profit_ratio in self.string:
                    profit_ratio = 0
                else:
                    profit_ratio = profit_ratio.replace(',','')
                net_profit_ratio = financial_ratio[[i]].iloc[3,0]
                if type(net_profit_ratio) == float:
                    if math.isnan(net_profit_ratio):
                        net_profit_ratio = 0
                    else:
                        net_profit_ratio = float(net_profit_ratio)
                elif net_profit_ratio in self.string:
                    net_profit_ratio = 0
                else:
                    net_profit_ratio = net_profit_ratio.replace(',','')
                consolidate_profit_ratio = financial_ratio[[i]].iloc[4,0]
                if type(consolidate_profit_ratio) == float:
                    if math.isnan(consolidate_profit_ratio):
                        consolidate_profit_ratio = 0
                    else:
                        consolidate_profit_ratio = float(consolidate_profit_ratio)
                elif consolidate_profit_ratio in self.string:
                    consolidate_profit_ratio = 0
                else:
                    consolidate_profit_ratio = consolidate_profit_ratio.replace(',','')
                net_roe = financial_ratio[[i]].iloc[5,0]
                if type(net_roe) == float:
                    if math.isnan(float(net_roe)):
                        net_roe = 0
                    else:
                        net_roe = net_roe
                elif net_roe in self.string:
                    net_roe = 0
                else:
                    net_roe = net_roe.replace(',','')
                consolidate_roe = financial_ratio[[i]].iloc[6,0]
                if type(consolidate_roe) == float:
                    if math.isnan(float(consolidate_roe)):
                        consolidate_roe = 0
                    else:
                        consolidate_roe = consolidate_roe
                elif consolidate_roe in self.string:
                    consolidate_roe = 0
                else:
                    consolidate_roe = consolidate_roe.replace(',','')
                revenue_growth = financial_ratio[[i]].iloc[8,0]
                if type(revenue_growth) == float:
                    if math.isnan(float(revenue_growth)):
                        revenue_growth = 0
                    else:
                        revenue_growth = revenue_growth
                elif revenue_growth in self.string:
                    revenue_growth = 0
                elif type(revenue_growth)==int:
                    revenue_growth = int(revenue_growth)
                else:
                    revenue_growth = revenue_growth.replace(',','')
                profit_growth = financial_ratio[[i]].iloc[9,0]
                if type(profit_growth) == float:
                    if math.isnan(float(profit_growth)):
                        profit_growth = 0
                    else:
                        profit_growth = profit_growth
                elif profit_growth in self.string:
                    profit_growth = 0
                elif type(profit_growth)==int:
                    profit_growth = int(profit_growth)
                else:
                    profit_growth = profit_growth.replace(',','')
                net_profit_growth = financial_ratio[[i]].iloc[10,0]
                if type(net_profit_growth) == float:
                    if math.isnan(float(net_profit_growth)):
                        net_profit_growth = 0
                    else:
                        net_profit_growth = net_profit_growth
                elif net_profit_growth in self.string:
                    net_profit_growth = 0
                else:
                    net_profit_growth = net_profit_growth.replace(',','')
                tmp = FinancialRatio(date=date, code=code, name=name, debt_ratio=debt_ratio, profit_ratio=profit_ratio,
                                    net_profit_ratio=net_profit_ratio, consolidate_profit_ratio=consolidate_profit_ratio,
                                    net_roe=net_roe, consolidate_roe=consolidate_roe, revenue_growth=revenue_growth,
                                    profit_growth=profit_growth, net_profit_growth=net_profit_growth)
                data_list.append(tmp)
        end = time.time()
        FinancialRatio.objects.bulk_create(data_list)
        self.success = True
        return end-start, self.success

    def scrape_sejong_quarterfinancial(self):
        data_list = []
        start = time.time()
        for i in range(len(self.ticker)):
            url = 'http://www.sejongdata.com/business_include_fr/table_main0_bus_02.html?&no='+ self.ticker[i].code
            r = requests.get(url, headers= self.user_agent, auth=('user', 'pass'))
            code = self.ticker[i].code
            name = self.ticker[i].name
            soup = BeautifulSoup(r.text, 'html.parser')
            df2= pd.read_html(url, thousands='')
            quarter_financial =  df2[0]
            for i in range(1,len(df2[0].columns)):
                date = quarter_financial[[i]].iloc[0,0].replace('.','')[:6]
                revenue = quarter_financial[[i]].iloc[1,0]
                if type(revenue) == float:
                    if math.isnan(revenue):
                        revenue = 0
                    else:
                        revenue = revenue
                elif revenue in self.string:
                    revenue = 0
                else:
                    revenue = revenue.replace(',','')
                profit = quarter_financial[[i]].iloc[2,0]
                if type(profit) == float:
                    if math.isnan(profit):
                        profit = 0
                    else:
                        profit = profit
                elif profit in self.string:
                    profit = 0
                else:
                    profit = profit.replace(',','')
                net_profit= quarter_financial[[i]].iloc[3,0]
                if type(net_profit) == float:
                    if math.isnan(net_profit):
                        net_profit=0
                    else:
                        net_profit = net_profit
                elif net_profit in self.string:
                    net_profit = 0
                else:
                    net_profit= net_profit.replace(',','')
                consolidate_profit = quarter_financial[[i]].iloc[4,0]
                if type(consolidate_profit) == float:
                    if math.isnan(consolidate_profit):
                        consolidate_profit = 0
                    else:
                        consolidate_profit = consolidate_profit
                elif consolidate_profit in self.string:
                    consolidate_profit = 0
                else:
                    consolidate_profit = consolidate_profit.replace(',','')
                profit_ratio = quarter_financial[[i]].iloc[5,0]
                if type(profit_ratio) == float:
                    if math.isnan(profit_ratio):
                        profit_ratio = 0
                    else:
                        profit_ratio = profit_ratio
                elif profit_ratio in self.string:
                    profit_ratio = 0
                else:
                    profit_ratio = profit_ratio.replace(',','')
                net_profit_ratio = quarter_financial[[i]].iloc[6,0]
                if type(net_profit_ratio)==float:
                    if math.isnan(net_profit_ratio):
                        net_profit_ratio = 0
                    else:
                        net_profit_ratio = net_profit_ratio
                elif net_profit_ratio in self.string:
                    net_profit_ratio = 0
                else:
                    net_profit_ratio = net_profit_ratio.replace(',','')
                tmp = QuarterFinancial(date=date,code=code,name=name,revenue=revenue,profit=profit,
                                    net_profit=net_profit, consolidate_profit=consolidate_profit,
                                    profit_ratio=profit_ratio, net_profit_ratio=net_profit_ratio)
                data_list.append(tmp)
        end = time.time()
        QuarterFinancial.objects.bulk_create(data_list)
        self.success = True
        return end-start, self.success


### split tasks ###

######## sejong financial ########
@task(name="scrape-sejong-financial-01")
def scrape_sejong_financial_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[:ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financial()

@task(name="scrape-sejong-financial-02")
def scrape_sejong_financial_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financial()

@task(name="scrape-sejong-financial-03")
def scrape_sejong_financial_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financial()

@task(name="scrape-sejong-financial-04")
def scrape_sejong_financial_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financial()

@task(name="scrape-sejong-financial-05")
def scrape_sejong_financial_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[4*ticker_cut:]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financial()


######## sejong financial ratio ########
@task(name="scrape-sejong-financialratio-01")
def scrape_sejong_financialratio_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[:ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-02")
def scrape_sejong_financialratio_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-03")
def scrape_sejong_financialratio_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-04")
def scrape_sejong_financialratio_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-05")
def scrape_sejong_financialratio_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-06")
def scrape_sejong_financialratio_6():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-07")
def scrape_sejong_financialratio_7():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-08")
def scrape_sejong_financialratio_8():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[7*ticker_cut:8*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-09")
def scrape_sejong_financialratio_9():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[8*ticker_cut:9*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()

@task(name="scrape-sejong-financialratio-10")
def scrape_sejong_financialratio_10():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[9*ticker_cut:]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_financialratio()


######## sejong quarter financial ########
@task(name="scrape-sejong-quarterfinancial-01")
def scrape_sejong_quarterfinancial_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[:ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-02")
def scrape_sejong_quarterfinancial_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-03")
def scrape_sejong_quarterfinancial_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-04")
def scrape_sejong_quarterfinancial_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-05")
def scrape_sejong_quarterfinancial_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-06")
def scrape_sejong_quarterfinancial_6():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-07")
def scrape_sejong_quarterfinancial_7():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-08")
def scrape_sejong_quarterfinancial_8():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[7*ticker_cut:8*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-09")
def scrape_sejong_quarterfinancial_9():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[8*ticker_cut:9*ticker_cut]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()

@task(name="scrape-sejong-quarterfinancial-10")
def scrape_sejong_quarterfinancial_10():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[9*ticker_cut:]
    ss = SejongScraper(ticker_list)
    ss.scrape_sejong_quarterfinancial()
