from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info, BuySell
import pandas as pd
import math

def scrape_buysell_today(ticker):
    success = False
    data_list = []
    for i in range(len(ticker)):
        url = 'http://finance.naver.com/item/frgn.nhn?code='+ ticker[i].code
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers=user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        tmp = soup.findAll('table',{'class':'type2'})
        table = soup.findAll('tr',{'onmouseout':'mouseOut(this)'})
        date=table[0].find('span',{'class':'tah p10 gray03'}).text.replace('.','')
        code=ticker[i].code
        name=ticker[i].name
        institution = table[0].findAll('td')[5].text
        if type(institution) == int:
            institution = institution
        else:
            institution = institution.replace(',','')
        foreign = table[0].findAll('td')[6].text
        if type(foreign) == int:
            foreign = foreign
        else:
            foreign = foreign.replace(',','')
        tmp_data = BuySell(date=date,name=name,code=code,institution=institution,foreigner=foreign)
        data_list.append(tmp_data)
    BuySell.objects.bulk_create(data_list)
    success = True
    return success, "Data request complete"

def scrape_buysell_total(ticker):
    success = False
    today = datetime.now()
    date_ago = today-timedelta(days=366)
    date_ago = date_ago.strftime('%Y%m%d')
    print(date_ago)
    data_list = []
    for i in range(len(ticker)):
        code = ticker[i].code
        name = ticker[i].name
        page = 1
        table_html_list = {
            'prev': '',
            'current': ''
        }
        while page:
            table_html_list['prev'] = table_html_list['current']
            url = 'http://finance.naver.com/item/frgn.nhn?code={}&page={}'.format(code,str(page))
            print(url)
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.findAll('tr',{'onmouseout':'mouseOut(this)'})
            table_html_list['current'] = table[0]
            if table_html_list['prev'] == table_html_list['current']:
                break
            for i in range(len(table)):
                date = table[i].find('span',{'class':'tah p10 gray03'})
                if date == None:
                    break
                else:
                    date = date.text.replace('.','')
                if date <= date_ago:
                    break
                close_price = table[i].findAll('td')[1].text
                if type(close_price) == int:
                    close_price = close_price
                else:
                    close_price = close_price.replace(',','')
                institution = table[i].findAll('td')[5].text
                if type(institution) == int:
                    institution = institution
                else:
                    institution = institution.replace(',','')
                foreign = table[i].findAll('td')[6].text
                if type(foreign) == int:
                    foreign = foreign
                else:
                    foreign = foreign.replace(',','')
                tmp = BuySell(date=date,name=name,code=code,close_price=close_price,institution=institution,foreigner=foreign)
                data_list.append(tmp)
            if date == None:
                page = 0
                # 데이터가 1년 전까지 없을 경우
            else:
                if date <= date_ago:
                    page = 0
                else:
                    page+=1
    BuySell.objects.bulk_create(data_list)
    success =True
    return success, "Data request complete"


### split tasks ###
@task(name="get-today-buysell-01")
def today_buysell_1():
    # today = datetime.now().strftime('%Y%m%d')
    today = '20180202'
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[:ticker_cut]
    scrape_buysell_today(ticker_list)

@task(name="get-today-buysell-02")
def today_buysell_2():
    # today = datetime.now().strftime('%Y%m%d')
    today = '20180202'
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    scrape_buysell_today(ticker_list)

@task(name="get-today-buysell-03")
def today_buysell_3():
    # today = datetime.now().strftime('%Y%m%d')
    today = '20180202'
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    scrape_buysell_today(ticker_list)

@task(name="get-today-buysell-04")
def today_buysell_4():
    # today = datetime.now().strftime('%Y%m%d')
    today = '20180202'
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    scrape_buysell_today(ticker_list)

@task(name="get-today-buysell-05")
def today_buysell_5():
    # today = datetime.now().strftime('%Y%m%d')
    today = '20180202'
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[4*ticker_cut:]
    scrape_buysell_today(ticker_list)


@task(name="get-total-buysell-01")
def total_buysell_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[:ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-02")
def total_buysell_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-03")
def total_buysell_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-04")
def total_buysell_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-05")
def total_buysell_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-06")
def total_buysell_6():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-07")
def total_buysell_7():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    scrape_buysell_total(ticker_list)

@task(name="get-total-buysell-08")
def total_buysell_8():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//8
    ticker_list = ticker[7*ticker_cut:]
    scrape_buysell_total(ticker_list)
