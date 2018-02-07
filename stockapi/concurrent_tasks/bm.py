from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re, time
from stockapi.models import BM
import pandas as pd
import math

def init_scrape_bm():
    for market in ['kospi', 'kosdaq']:
        done = False
        data_list = []
        page = 1
        while not done:
            url = 'http://finance.daum.net/quote/{}_yyyymmdd.daum?page={}'.format(market, page)
            table = pd.read_html(url)
            table = table[0]
            for i in range(1, len(table)):
                row = table.ix[i]
                if str(row[0])[0] == '9':
                    done = True
                    continue
                try:
                    date = '20' + str(row[0]).replace('.', '')[:8]
                    index = float(str(row[1]).replace(',', ''))
                    volume = int(str(row[4]).replace(',', ''))
                    individual = int(str(row[6]).replace(',', '').replace('+', ''))
                    foreigner = int(str(row[7]).replace(',', '').replace('+', ''))
                    institution = int(str(row[8]).replace(',', '').replace('+', ''))
                    bm_inst = BM(date=date,
                                 name=market.upper(),
                                 index=index,
                                 volume=volume,
                                 individual=individual,
                                 foreigner=foreigner,
                                 institution=institution)
                    data_list.append(bm_inst)
                except:
                    for j in [0, 1, 4, 6, 7, 8]:
                        print('Check data {}: {}'.format(j, row[j]))
            page += 1
            print('{}: {} page scraped, on date {}'.format(market.upper(), page, date))
        BM.objects.bulk_create(data_list)

def scrape_today_bm():
    start = time.time()
    bm_recent_updated = BM.objects.order_by('date').last().date
    url = 'http://finance.daum.net/quote/kospi_yyyymmdd.daum'
    table = pd.read_html(url)
    table = table[0]
    market_date = '20' + str(table.ix[1][0]).replace('.', '')[:8]
    if str(bm_recent_updated) != str(market_date):
        for market in ['kospi', 'kosdaq']:
            url = 'http://finance.daum.net/quote/{}_yyyymmdd.daum'.format(market)
            table = pd.read_html(url)
            table = table[0]
            row = table.ix[1]
            date = '20' + str(row[0]).replace('.', '')[:8]
            index = float(str(row[1]).replace(',', ''))
            volume = int(str(row[4]).replace(',', ''))
            individual = int(str(row[6]).replace(',', '').replace('+', ''))
            foreigner = int(str(row[7]).replace(',', '').replace('+', ''))
            institution = int(str(row[8]).replace(',', '').replace('+', ''))
            bm_inst = BM(date=date,
                         name=market.upper(),
                         index=index,
                         volume=volume,
                         individual=individual,
                         foreigner=foreigner,
                         institution=institution)
            bm_inst.save()
        print('{} data updated'.format(market_date))
    else:
        print('No data to update')
    end = time.time()
    print('Time took: ', str(end - start))
