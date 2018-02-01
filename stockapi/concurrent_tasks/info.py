from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info
import pandas as pd
import math

def scrape_info(ticker):
    success = False
    data_list=[]
    date = datetime.now().strftime('%Y%m%d')
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    for i in range(len(ticker)) :
        url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cn=&cmp_cd='+ ticker[i].code
        code = ticker[i].code
        name = ticker[i].name
        r = requests.get(url, headers=user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        tmp = soup.findAll('td',{'class':'cmp-table-cell td0101'})
        if len(tmp) != 0:
            tmp = tmp[0].findAll('dt',{'class':'line-left'})[1].text.replace(' ','').split(':')
            market_type = tmp[0]
            industry = tmp[1]
            url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            todayinfo = soup.findAll('dl',{'class':'blind'})
            stockinfo = pd.read_html(url, thousands='')
            price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
            if len(stockinfo[1]) == 5:
                face_val = stockinfo[1].iloc[3,1].replace(' ','').replace(',','').replace('원','').split('l')[0]
                stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                #per, eps
                per_td = soup.findAll('table',{'class':'per_table'})
                td = per_td[0].findAll('em')
                per_table = []
                for t in td:
                    a = t.text
                    per_table.append(a)
                per = 0 if per_table[0] == "N/A" else per_table[0].replace(',','')
                eps = 0 if per_table[1] == "N/A" else per_table[1].replace(',','')
                yield_ret = 0 if per_table[8] == "N/A" else per_table[8]
                bps = 0 if per_table[7] == "N/A" else per_table[7].replace(',','')
                pbr = 0 if bps == 0 else round(int(price)/int(bps),2)
                print(code,stockinfo[5].iloc[0,1])
                try:
                    math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                    industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                except AttributeError:
                    industry_per = 0
                print(code,industry_per)
                market_cap = int(price)*int(stock_nums) #시가총액
            elif len(stockinfo[1]) == 4:
                face_val = 0
                stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                #per, eps
                per_td = soup.findAll('table',{'class':'per_table'})
                td = per_td[0].findAll('em')
                per_table = []
                for t in td:
                    a = t.text
                    per_table.append(a)
                per = per_table[0]
                eps = per_table[1].replace(',','')
                yield_ret = 0 if per_table[8] == "N/A" else per_table[8]
                bps = 0 if per_table[7] == "N/A" else per_table[7].replace(',','')
                pbr = 0 if bps == 0 else round(int(price)/int(bps),2)
                try:
                    math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                    industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                except AttributeError:
                    industry_per = 0
                print(code,industry_per)
                market_cap = int(price)*int(stock_nums)
            else:
                face_val = 0
                stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
                foreign_limit = 0
                foreign_possession = 0
                foreign_ratio = 0
                per = 0
                eps = 0
                pbr = 0
                bps = 0
                industry_per = 0
                yield_ret = 0
                market_cap = int(price)*int(stock_nums)
            tmp_json = Info(date=date,
                            code=code,
                            name=name,
                            market_type=market_type,
                            industry=industry,
                            price=price,
                            face_val=face_val,
                            stock_nums=stock_nums,
                            market_cap=market_cap,
                            foreign_limit=foreign_limit,
                            foreign_possession=foreign_possession,
                            foreign_ratio=foreign_ratio,
                            per=per,
                            eps=eps,
                            bps=bps,
                            pbr=pbr,
                            industry_per=industry_per,
                            yield_ret=yield_ret)
            data_list.append(tmp_json)
        else:
            url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            market_type = "KOSPI"
            industry = "ETF"
            soup = BeautifulSoup(r.text, 'html.parser')
            todayinfo = soup.findAll('dl',{'class':'blind'})
            price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
            stockinfo = pd.read_html(url, thousands='')
            stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
            face_val = 0
            market_cap = int(price)*int(stock_nums) #시가총액
            foreign_limit = 0
            foreign_possession = 0
            foreign_ratio = 0
            per = 0
            eps = 0
            pbr = 0
            bps = 0
            industry_per = 0
            yield_ret = 0
            tmp_json = Info(date=date,
                            code=code,
                            name=name,
                            market_type=market_type,
                            industry=industry,
                            price=price,
                            face_val=face_val,
                            stock_nums=stock_nums,
                            market_cap=market_cap,
                            foreign_limit=foreign_limit,
                            foreign_possession=foreign_possession,
                            foreign_ratio=foreign_ratio,
                            per=per,
                            eps=eps,
                            bps=bps,
                            pbr=pbr,
                            industry_per=industry_per,
                            yield_ret=yield_ret)
            data_list.append(tmp_json)
    f.close()
    success = True
    Info.objects.bulk_create(data_list)
    return success


### Task splits ###
@task(name="info-get-01")
def info_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[:ticker_cut]
    scrape_info(ticker_list)

@task(name="info-get-02")
def info_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    scrape_info(ticker_list)

@task(name="info-get-03")
def info_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    scrape_info(ticker_list)

@task(name="info-get-04")
def info_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    scrape_info(ticker_list)

@task(name="info-get-05")
def info_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[4*ticker_cut:]
    scrape_info(ticker_list)
