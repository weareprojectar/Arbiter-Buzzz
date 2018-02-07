## @Ver     0.8v
## @Author  Phillip Park
## @Date    2017/12/23
## @Details 버즈 프로젝트 관리에 필요한 툴들의 집합소

## @Comments 서버에서는 KRX.py가 작동하지 않음 (dependencies의 문제로 예상)

import os, sys, glob

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbiter.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### scripts ###
# from tools.Benchmark import Benchmark
from tools.Backup import Backup
from tools.Cleaner import Cleaner
from tools.Data import Data
# from tools.Processor import Processor
from tools.Sensitives import Sensitives
from tools.Test import Test
# import tools.KRX as KRX
from tools.Update import Update

from stockapi.tasks import scrape_ticker
from stockapi.concurrent_tasks.bm import scrape_today_bm

if sys.argv[1] == 'cleanmigrations':
    c = Cleaner(start_path)
    c.clean_migrations()
    db = start_path + '/db.sqlite3'
    if os.path.exists(db):
        os.remove(db)
        print('Removed database')

elif sys.argv[1] == 'sensitives':
    s = Sensitives(start_path)
    if sys.argv[2] == 'setup':
        s.setup()
    elif sys.argv[2] == 'check':
        s.check()
    elif sys.argv[2] == 'set':
        s.set(sys.argv[3], sys.argv[4])
        s.save()

elif sys.argv[1] == 'update':
    u = Update()
    if sys.argv[2] == 'db_init_1':
        u.split_ohlcv_1()
    elif sys.argv[2] == 'db_init_2':
        u.split_ohlcv_2()
    elif sys.argv[2] == 'db_init_3':
        u.split_ohlcv_3()
    elif sys.argv[2] == 'db_init_4':
        u.split_ohlcv_4()
    elif sys.argv[2] == 'db_init_5':
        u.split_ohlcv_5()
    elif sys.argv[2] == 'fillin_ohlcv':
        u.fillin_blank_ohlcv()

elif sys.argv[1] == 'backup':
    b = Backup()
    b.ticker_backup()
    b.info_backup()
    b.financial_backup()
    b.financialratio_backup()
    b.quarterfinancial_backup()
    b.buysell_backup()

elif sys.argv[1] == 'test':
    t = Test()
    t.test_scrape_today_buysell()

# elif sys.argv[1] == 'bm':
#     b = Benchmark(start_path)
#     df, exists = b.get()
#     recent_date = list(df.ix[len(df)-1])[0].replace('-', '')
#     if exists:
#         print('Recent update: ' + recent_date)
#     else:
#         print('Downloaded data to: ' + recent_date)
#
elif sys.argv[1] == 'data':
    d = Data(start_path)
    if sys.argv[2] == 'send':
        if sys.argv[3] == 'ticker':
            d.send_ticker()
        elif sys.argv[3] == 'bm':
            d.send_bm()
        elif sys.argv[3] == 'ohlcv':
            d.send_ohlcv()
    elif sys.argv[2] == 'update':
        if sys.argv[3] == 'ohlcv':
            d.update_ohlcv()
        elif sys.argv[3] == 'ohlcv_with_date_1':
            d.upd_ohlcv_1()
        elif sys.argv[3] == 'ohlcv_with_date_2':
            d.upd_ohlcv_2()
        elif sys.argv[3] == 'ohlcv_with_date_3':
            d.upd_ohlcv_3()
        elif sys.argv[3] == 'ohlcv_with_date_4':
            d.upd_ohlcv_4()
        elif sys.argv[3] == 'ohlcv_with_date_5':
            d.upd_ohlcv_5()
    elif sys.argv[2] == 'clean':
        if sys.argv[3] == 'ohlcv':
            d.clean_ohlcv()
        elif sys.argv[3] == 'bm':
            d.clean_bm()

elif sys.argv[1] == 'daily_tasks':
    # 0. scrape today tickers
    print('TASK: Ticker scrape')
    scrape_ticker()
    # 1. scrape daum benchmark data - kospi, kosdaq
    print('TASK: BM scrape')
    scrape_today_bm()
    # 2.

elif sys.argv[1] == 'fillin':
    from stockapi.concurrent_tasks.ohlcv import ohlcv_fillin_1, ohlcv_fillin_2, ohlcv_fillin_3, ohlcv_fillin_4, ohlcv_fillin_5
    if sys.argv[2] == '1':
        ohlcv_fillin_1()
    elif sys.argv[2] == '2':
        ohlcv_fillin_2()
    elif sys.argv[2] == '3':
        ohlcv_fillin_3()
    elif sys.argv[2] == '4':
        ohlcv_fillin_4()
    elif sys.argv[2] == '5':
        ohlcv_fillin_5()
#
# elif sys.argv[1] == 'krx':
#     KRX.main(start_path)
#
# elif sys.argv[1] == 'process':
#     p = Processor()
#     if sys.argv[2] == 'make':
#         p.make_data()
#     elif sys.argv[2] == 'specs':
#         p.score_data()
#     elif sys.argv[2] == 'today_port':
#         p.make_todays_portfolio()
#     # p.get_data_local()
#     # p.set_return_portfolio()
#     # p.bm_data()
#     # p.save_mom_volt_cor_vol()
