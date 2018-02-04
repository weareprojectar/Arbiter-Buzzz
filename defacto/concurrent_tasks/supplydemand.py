from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV
from defacto.models import SupplyDemand
import pandas as pd



def calc_supply_demand_all(ticker):
    success=False
    data_list=[]
    for i in range(len(ticker)):
        code = ticker[i].code
        name = ticker[i].name
        date_value = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('date')
        institution_value = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('institution')
        foreigner_value = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('foreigner')
        list_date = [data[0] for data in date_value]
        list_instutions = [data[0] for data in institution_value]
        list_foreigner = [data[0] for data in foreigner_value]
        close_price = OHLCV.objects.filter(code=code).order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('close_price')
        list_close_price = [data[0] for data in close_price]
        data_pandas = pd.DataFrame({'date':list_date, 'close_price':list_close_price, 'institution':list_instutions, 'foreigner':list_foreigner})
        data_pandas['institution_possession'] = data_pandas['institution'].cumsum()
        data_pandas['institution_possession'] = data_pandas['institution_possession'] + abs(min(data_pandas['institution_possession']))
        data_pandas['institution_possession'] = [1 if x==0 else x for x in data_pandas['institution_possession']] # 0을 로 변환
        data_pandas['institution_average_price'] = round((data_pandas['close_price']*data_pandas['institution'])/data_pandas['institution_possession'],3)
        data_pandas['foreigner_possesion'] = data_pandas['foreigner'].cumsum()
        data_pandas['foreigner_possesion'] = data_pandas['foreigner_possesion'] + abs(min(data_pandas['foreigner_possesion']))
        data_pandas['foreigner_possesion'] = [1 if x==0 else x for x in data_pandas['foreigner_possesion']]
        data_pandas['foreigner_average_price'] = round((data_pandas['close_price']*data_pandas['foreigner'])/data_pandas['foreigner_possesion'],3)
        for i in range(data_pandas.shape[0]):
            date = data_pandas.iloc[i,0]
            code = code
            name = name
            institution_possession = data_pandas.iloc[i,4]
            institution_average_price = data_pandas.iloc[i,5]
            foreigner_possesion = data_pandas.iloc[i,6]
            foreigner_average_price = data_pandas.iloc[i,7]
            tmp = SupplyDemand(date=date,name=name,code=code,inst,institution_possession=institution_possession,institution_average_price=institution_average_price,
                            foreigner_possesion=foreigner_possesion, foreigner_average_price=foreigner_average_price)
            data_list.append(tmp)
    SupplyDemand.objects.bulk_create(data_list)
    success=True
    return success, "Data calculate complete"




# @task(name="calc-buysell-01")
# def calc_buysell_1():
#     today = datetime.now().strftime('%Y%m%d')
#     ticker = Ticker.objects.filter(date=today).order_by('id')
#     ticker_count = ticker.count()
#     ticker_cut = ticker_count//5
#     ticker_list = ticker[:ticker_cut]
#     calc_supply_demand_all(ticker_list)
#
# @task(name="calc-buysell-02")
# def calc_buysell_2():
#     today = datetime.now().strftime('%Y%m%d')
#     ticker = Ticker.objects.filter(date=today).order_by('id')
#     ticker_count = ticker.count()
#     ticker_cut = ticker_count//5
#     ticker_list = ticker[ticker_cut:2*ticker_cut]
#     calc_supply_demand_all(ticker_list)
#
# @task(name="calc-buysell-03")
# def calc_buysell_3():
#     today = datetime.now().strftime('%Y%m%d')
#     ticker = Ticker.objects.filter(date=today).order_by('id')
#     ticker_count = ticker.count()
#     ticker_cut = ticker_count//5
#     ticker_list = ticker[2*ticker_cut:3*ticker_cut]
#     calc_supply_demand_all(ticker_list)
#
# @task(name="calc-buysell-04")
# def calc_buysell_4():
#     today = datetime.now().strftime('%Y%m%d')
#     ticker = Ticker.objects.filter(date=today).order_by('id')
#     ticker_count = ticker.count()
#     ticker_cut = ticker_count//5
#     ticker_list = ticker[3*ticker_cut:4*ticker_cut]
#     calc_supply_demand_all(ticker_list)
#
# @task(name="calc-buysell-05")
# def calc_buysell_5():
#     today = datetime.now().strftime('%Y%m%d')
#     ticker = Ticker.objects.filter(date=today).order_by('id')
#     ticker_count = ticker.count()
#     ticker_cut = ticker_count//5
#     ticker_list = ticker[4*ticker_cut:]
#     calc_supply_demand_all(ticker_list)
