from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import BM
import pandas as pd
import math

def scrape_bm():
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
                if row[0][0] == '9':
                    done = True
                    continue
                date = '20' + row[0].replace('.', '')
                index = float(row[1].replace(',', ''))
                volume = int(row[4].replace(',', ''))
                individual = int(row[6].replace(',', '').replace('+', ''))
                foreigner = int(row[7].replace(',', '').replace('+', ''))
                institution = int(row[8].replace(',', '').replace('+', ''))
                bm_inst = BM(date=date,
                             name=market.upper(),
                             index=index,
                             volume=volume,
                             individual=individual,
                             foreigner=foreigner,
                             institution=institution)
                data_list.append(bm_inst)
            page += 1
            print('{}: {} page scraped, on date {}'.format(market.upper(), page, date))
        BM.objects.bulk_create(data_list)

scrape_bm()
