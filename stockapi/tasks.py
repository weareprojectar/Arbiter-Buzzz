from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info
import pandas as pd
import math

from stockapi.concurrent_tasks.ohlcv import (
    ohlcv_1,
    ohlcv_2,
    ohlcv_3,
    ohlcv_4,
    ohlcv_5,
    ohlcv_6,
    ohlcv_7,
    ohlcv_8,
    ohlcv_9,
    ohlcv_10,

    ohlcv_fillin_1,
    ohlcv_fillin_2,
    ohlcv_fillin_3,
    ohlcv_fillin_4,
)
# from stockapi.concurrent_tasks.stockinfo import (
#     scrape_kospi_stockinfo,
#     scrape_kosdaq_stockinfo,
# )
# from stockapi.concurrent_tasks.info import (
#     info_1,
#     info_2,
#     info_3,
#     info_4,
#     info_5,
# )
from stockapi.concurrent_tasks.buysell import (
    today_buysell_1,
    today_buysell_2,
    today_buysell_3,
    today_buysell_4,
    today_buysell_5,

    total_buysell_1,
    total_buysell_2,
    total_buysell_3,
    total_buysell_4,
    total_buysell_5,
    total_buysell_6,
    total_buysell_7,
    total_buysell_8,
)
# from stockapi.concurrent_tasks.financial import (
#     scrape_sejong_financial_1,
#     scrape_sejong_financial_2,
#     scrape_sejong_financial_3,
#     scrape_sejong_financial_4,
#     scrape_sejong_financial_5,
#     scrape_sejong_financial_6,
#     scrape_sejong_financial_7,
#     scrape_sejong_financial_8,
#     scrape_sejong_financial_9,
#     scrape_sejong_financial_10,
#
#     scrape_sejong_financialratio_1,
#     scrape_sejong_financialratio_2,
#     scrape_sejong_financialratio_3,
#     scrape_sejong_financialratio_4,
#     scrape_sejong_financialratio_5,
#     scrape_sejong_financialratio_6,
#     scrape_sejong_financialratio_7,
#     scrape_sejong_financialratio_8,
#     scrape_sejong_financialratio_9,
#     scrape_sejong_financialratio_10,
#
#     scrape_sejong_quarterfinancial_1,
#     scrape_sejong_quarterfinancial_2,
#     scrape_sejong_quarterfinancial_3,
#     scrape_sejong_quarterfinancial_4,
#     scrape_sejong_quarterfinancial_5,
#     scrape_sejong_quarterfinancial_6,
#     scrape_sejong_quarterfinancial_7,
#     scrape_sejong_quarterfinancial_8,
#     scrape_sejong_quarterfinancial_9,
#     scrape_sejong_quarterfinancial_10,
# )

# Issue: None
@task(name="scrape_stock_ticker")
def scrape_ticker():
    data_list = []
    page = 1
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    date = datetime.now().strftime('%Y%m%d')
    exists = Ticker.objects.filter(date=date).exists()
    if exists:
        print('Tickers already updated for {}'.format(date))
    while not exists:
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
                    # data saves here
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
