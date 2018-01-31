from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info
import pandas as pd
import math

@task(name="scrape_kospi_stockinfo")
def scrape_kospi_stockinfo():
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d%H%M')
    page = 0
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    while 1:
        page = page + 1
        url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            break
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            price = table[i].text.split("\n")[3].replace(',','')
            volume = table[i].text.split("\n")[6].replace(',','')
            market_type = market_dic['P']
            stockinst = StockInfo(date=date_time,
                                  name=name,
                                  code=code,
                                  price=price,
                                  volume=volume,
                                  market_type=market_type)
            data_list.append(stockinst)
    StockInfo.objects.bulk_create(data_list)
    success = True
    return success, "Data request complete"

@task(name="scrape_kosdaq_stockinfo")
def scrape_kosdaq_stockinfo():
    # start = time.time()
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d%H%M')
    page = 0
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    while 1:
        page = page + 1
        url = 'http://finance.daum.net/quote/volume.daum?stype=Q&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            break
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            price = table[i].text.split("\n")[3].replace(',','')
            volume = table[i].text.split("\n")[6].replace(',','')
            market_type = market_dic['Q']
            stockinst = StockInfo(date=date_time,
                                  name=name,
                                  code=code,
                                  price=price,
                                  volume=volume,
                                  market_type=market_type)
            data_list.append(stockinst)
    StockInfo.objects.bulk_create(data_list)
    success = True
    return success, "Data request complete"
