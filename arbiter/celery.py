from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arbiter.settings')

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from celery.schedules import crontab

main_coins = [
    'BTC', 'BCC', 'ETH', 'ETC', 'XRP', 'ADA', 'XLM', 'QTUM', 'NEO', 'STEEM', 'SBD', 'LTC'
]
second_tier_coins = [
    'SNT', 'XEM', 'MER', 'BTG', 'ARDR', 'STRAT', 'TIX', 'OMG', 'POWR', 'GRS', 'STORJ'
]
third_tier_coins = [
    'PIVX', 'KMD', 'XMR', 'ARK', 'REP', 'LSK', 'WAVES', 'MTL', 'DASH', 'VTC', 'ZEC'
]

app.conf.beat_schedule = {
    ### UPBIT Task #1 ###
    # upbit minute chart data requests
    'add-upbit-main-every-60-seconds': {
        'task': 'request_upbit',
        'schedule': 60.0,
        'args': (main_coins,)
        },
    'add-upbit-second-every-60-seconds': {
        'task': 'request_upbit',
        'schedule': 60.0,
        'args': (second_tier_coins,)
        },
    'add-upbit-third-every-60-seconds': {
        'task': 'request_upbit',
        'schedule': 60.0,
        'args': (third_tier_coins,)
        },


    # 'scrape-daum-ticker-at-9': {
    #     'task': 'stock-ticker',
    #     'schedule': crontab(hour=9, day_of_week='mon-fri'),
    #     'args': ()
    #     },
    # 'scrape-naver-ohlvc-at-9to4': {
    #     'task': 'ohlcv-get',
    #     'schedule': crontab(minute='*/1', hour='9-16', day_of_week='mon-fri'),
    #     'args': ()
    #     },
    }
