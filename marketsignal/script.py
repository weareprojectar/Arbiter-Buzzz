from marketsignal.tasks import index_industry_data, score_data, init_ohlcv_csv_save
from stockapi.concurrent_tasks.bm import scrape_today_bm

scrape_today_bm()
