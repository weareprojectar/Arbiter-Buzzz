from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, StockInfo, Info
import pandas as pd
import math

### scrape ohlcv base function
def scrape_ohlcv(tickers):
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d')
    for i in range(len(tickers)):
        url = 'http://finance.naver.com/item/sise.nhn?code=' + tickers[i].code
        code = tickers[i].code
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('dt')[1].text
        df = pd.read_html(url, thousands='')
        market = tickers[i].market_type
        name = name
        code = code
        date = date_time
        open_price = df[1].iloc[3,3].replace(",","")  #시가
        close_price = df[1].iloc[0,1].replace(",","") #현재가, 종가
        high_price = df[1].iloc[4,3].replace(",","")  #고가
        low_price = df[1].iloc[5,3].replace(",","") #저가
        volume = df[1].iloc[3,1].replace(",","")
        ohlcv_inst = OHLCV(date=date,
                           # name=name,
                           code=code,
                           # market_type=market,
                           open_price=open_price,
                           close_price=close_price,
                           high_price=high_price,
                           low_price=low_price,
                           volume=volume)
        data_list.append(ohlcv_inst)
    OHLCV.objects.bulk_create(data_list)
    success = True
    return success, "Data request complete"


### Task splits ###
@task(name="ohlcv-get-01")
def ohlcv_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//4
    ticker_list = ticker[:ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-02")
def ohlcv_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//4
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-03")
def ohlcv_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//4
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-04")
def ohlcv_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//4
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-05")
def ohlcv_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-06")
def ohlcv_6():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-07")
def ohlcv_7():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-08")
def ohlcv_8():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[7*ticker_cut:8*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-09")
def ohlcv_9():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[8*ticker_cut:9*ticker_cut]
    scrape_ohlcv(ticker_list)

@task(name="ohlcv-get-10")
def ohlcv_10():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[9*ticker_cut:]
    scrape_ohlcv(ticker_list)

from tools.Update import Update

@task(name="ohlcv-fillin-1")
def ohlcv_fillin_1():
    u = Update()
    u.fillin_1()

@task(name="ohlcv-fillin-2")
def ohlcv_fillin_2():
    u = Update()
    u.fillin_2()

@task(name="ohlcv-fillin-3")
def ohlcv_fillin_3():
    u = Update()
    u.fillin_3()

@task(name="ohlcv-fillin-4")
def ohlcv_fillin_4():
    u = Update()
    u.fillin_4()
