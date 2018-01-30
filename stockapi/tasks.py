from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info
import pandas as pd
import json

@task(name="scrape_stock_ticker")
def scrape_ticker():
    data_list = []
    page = 1
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    date = datetime.now().strftime('%Y%m%d')
    while 1:
        url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            page=1
            while 1:
                url = 'http://finance.daum.net/quote/volume.daum?stype=Q&page={}'.format(str(page))
                r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
                if len(table)==0:
                    Ticker.objects.bulk_create(data_list)
                    success = True
                    return success
                for i in range(len(table)):
                    code = table[i].find('a').attrs['href'][-6:]
                    name = table[i].text.split("\n")[2]
                    market_type = market_dic['Q']
                    ticker_inst = Ticker(date=date,
                                        name=name,
                                        code=code,
                                        market_type=market_type)
                    data_list.append(ticker_inst)
                page = page + 1
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            market_type = market_dic['P']
            ticker_inst = Ticker(date=date,
                                name=name,
                                code=code,
                                market_type=market_type)
            data_list.append(ticker_inst)
        page = page + 1
