from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arbiter.settings')
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

def add_task(task_name, task_func, task_cron, task_args):
    task_def = {
        'task': task_func,
        'schedule': task_cron,
        'args': task_args
    }
    app.conf.beat_schedule[task_name] = task_def


coins = {
    'main': ['BTC', 'BCC', 'ETH', 'ETC', 'XRP', 'ADA', 'XLM', 'QTUM', 'NEO', 'STEEM', 'SBD', 'LTC'],
    'second-tier': ['SNT', 'XEM', 'MER', 'BTG', 'ARDR', 'STRAT', 'TIX', 'OMG', 'POWR', 'GRS', 'STORJ'],
    'third-tier': ['PIVX', 'KMD', 'XMR', 'ARK', 'REP', 'LSK', 'WAVES', 'MTL', 'DASH', 'VTC', 'ZEC']
}

app.conf.beat_schedule = {}


### Task #1 UPBIT ###
# upbit minute chart data requests
for key, val in coins.items():
    task_name = 'add-upbit-{}-every-60-seconds'.format(key)
    task_func = 'request_upbit'
    task_cron = 60.0
    task_args = (val,)
    add_task(task_name, task_func, task_cron, task_args)

# app.conf.beat_schedule = {
#     'scrape-daum-ticker-at-9': {
#         'task': 'stock-ticker',
#         'schedule': crontab(hour=9, day_of_week='mon-fri'),
#         'args': ()
#         },
#     'scrape-naver-ohlvc-at-9to4': {
#         'task': 'ohlcv-get',
#         'schedule': crontab(minute='*/1', hour='9-16', day_of_week='mon-fri'),
#         'args': ()
#         },
# }
