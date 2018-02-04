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

markets = ['kospi', 'kosdaq']
coins = {
    'main': ['BTC', 'BCC', 'ETH', 'ETC', 'XRP', 'ADA', 'XLM', 'QTUM', 'NEO', 'STEEM', 'SBD', 'LTC'],
    'second-tier': ['SNT', 'XEM', 'MER', 'BTG', 'ARDR', 'STRAT', 'TIX', 'OMG', 'POWR', 'GRS', 'STORJ'],
    'third-tier': ['PIVX', 'KMD', 'XMR', 'ARK', 'REP', 'LSK', 'WAVES', 'MTL', 'DASH', 'VTC', 'ZEC']
}

app.conf.beat_schedule = {}


# ### Task #1 UPBIT ###
# # upbit minute chart data requests
# for key, val in coins.items():
#     task_name = 'add-upbit-{}-every-60-seconds'.format(key)
#     task_func = 'request_upbit'
#     task_cron = 60.0
#     task_args = (val,)
#     add_task(task_name, task_func, task_cron, task_args)
#
# ### Task #2 StockInfo ###
# # scrape daum stock info every minute from 9 to 16
# for market in markets:
#     app.conf.beat_schedule['scrape-daum-{}-stock-price'.format(market)] = {
#         'task': 'scrape_{}_stockinfo'.format(market),
#         'schedule': 60.0,
#         'args': ()
#     }
#
# ### Task #3 Info ###
# # scrape naver stock info: per, bps etc.
# for i in range(1, 6):
#     task_name = 'scrape_info_{}'.format(str(i))
#     task_func = 'info-get-0{}'.format(str(i))
#     task_cron = 500.0
#     task_args = ()
#     add_task(task_name, task_func, task_cron, task_args)

### Task #4 BuySell ###
for i in range(1, 11):
    task_name = 'calc-buysell-{}'.format(str(i).zfill(2))
    task_func = 'calc-buysell-{}'.format(str(i).zfill(2))
    task_cron = crontab(minute=50, hour=19, day_of_week='sun-sat')
    task_args = ()
    add_task(task_name, task_func, task_cron, task_args)



# ### Task #5 Financial ###
# # scrape sejong financial data
# for taskname in ['financial', 'financialratio', 'quarterfinancial']:
#     for i in range(1, 11):
#         task_name = 'scrape-sejong-{}-{}'.format(taskname, str(i).zfill(2))
#         task_func = 'scrape-sejong-{}-{}'.format(taskname, str(i).zfill(2))
#         task_cron = 5000.0
#         task_args = ()
#         add_task(task_name, task_func, task_cron, task_args)


# app.conf.beat_schedule['scrape-daum-ticker-at-9'] = {
#     'task': 'scrape_stock_ticker',
#     'schedule': crontab(hour=9, day_of_week='mon-fri'),
#     'args': ()
# }

app.conf.timezone = 'Asia/Seoul'
