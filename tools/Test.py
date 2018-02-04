## @Ver     0.8v
## @Author  Phillip Park
## @Date    2018/2/2
## @Details 테스트

from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info, BuySell
import pandas as pd
import math


class Test:
    def __init__(self):
        print('Tester initialized')

    def test_scrape_today_buysell(self):
        # get tickers
        today = '20180202'
        ticker = Ticker.objects.filter(date=today).order_by('id')
        ticker_count = ticker.count()
        ticker_cut = ticker_count//5
        ticker = ticker[:ticker_cut]
        # start scraping
        success = False
        data_list = []
        for i in range(len(ticker)):
            url = 'http://finance.naver.com/item/frgn.nhn?code='+ ticker[i].code
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers=user_agent, auth=('user', 'pass'))
            if r.status_code == 200:
                print('{} request successful'.format(ticker[i].code))
                soup = BeautifulSoup(r.text, 'html.parser')
                tmp = soup.findAll('table',{'class':'type2'})
                table = soup.findAll('tr',{'onmouseout':'mouseOut(this)'})
                date = table[0].find('span',{'class':'tah p10 gray03'}).text.replace('.','')
                print(date)
                code = ticker[i].code
                print(code)
                name = ticker[i].name
                print(name)
                institution = table[0].findAll('td')[5].text
                if type(institution) == int:
                    institution = institution
                else:
                    institution = institution.replace(',','')
                print(institution)
                foreign = table[0].findAll('td')[6].text
                if type(foreign) == int:
                    foreign = foreign
                else:
                    foreign = foreign.replace(',','')
                print(foreign)
                tmp_data = BuySell(date=date,name=name,code=code,institution=institution,foreigner=foreign)
                data_list.append(tmp_data)
        BuySell.objects.bulk_create(data_list)
        success = True
        return success, "Data request complete"
