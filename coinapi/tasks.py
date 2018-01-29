from __future__ import absolute_import, unicode_literals
import random
import time
import requests
from celery.decorators import task
from datetime import datetime
from coinapi.models import Candle, Price

@task(name="request_upbit")
def request_upbit(coins_list):
    success = False
    for coin in coins_list:
        user_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        }
        url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-{}'.format(coin)
        r = requests.get(url, headers = user_agent, auth=('user', 'pass'))
        try:
            r = requests.get(url)
            while(r.status_code != 200):
                sec = random.random()
                time.sleep(sec)
                r = requests.get(url)
        except:
            print("status_code error")

        upbitdata = r.json()
        high_price = upbitdata[0]['highPrice']
        low_price = upbitdata[0]['lowPrice']
        open_price = upbitdata[0]['openingPrice']
        close_price = upbitdata[0]['tradePrice']
        trade_price = upbitdata[0]['candleAccTradePrice']
        volume = upbitdata[0]['candleAccTradeVolume']
        mean_price = trade_price/volume
        date = datetime.fromtimestamp(int(upbitdata[0]['timestamp'])/1000).strftime("%Y%m%d%H%M")
        ticker = coin

        record = Candle(date=date,
                        ticker=ticker,
                        high_price=high_price,
                        low_price=low_price,
                        open_price=open_price,
                        close_price=close_price,
                        trade_price=trade_price,
                        volume=volume,
                        mean_price=mean_price,)
        record.save()
        success = True
    return success, "Data request complete"

@task(name="request_upbit_price")
def request_data_price(coins_list):
    success = False
    for coin in coins_list:
        url = 'https://crix-api-endpoint.upbit.com/v1/crix/trades/ticks?code=CRIX.UPBIT.KRW-{}'.format(coin)

        try:
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers = user_agent, auth=('user', 'pass'))
            while(r.status_code != 200):
                sec = random.random()
                time.sleep(sec)
                r = requests.get(url)
        except:
            print("status_code error!")

        ticker = coin
        upbitprice=r.json()
        date = datetime.fromtimestamp(int(upbitprice[0]['timestamp'])/1000).strftime("%Y-%m-%d %H:%M:%S.%f")
        price = upbitprice[0]['tradePrice']
        vol = upbitprice[0]['tradeVolume']
        prev_price = upbitprice[0]['prevClosingPrice']
        change = upbitprice[0]['change']
        ch_price = upbitprice[0]['changePrice']
        AB = upbitprice[0]['askBid']

        record = Price(date=date,
                       ticker=ticker,
                       price=price,
                       volume=vol,
                       prev_price=prev_price,
                       change=change,
                       ch_price=ch_price,
                       AB=AB,)

        record.save()
        success = True
    return success, "Data request complete"
