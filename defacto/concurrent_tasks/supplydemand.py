from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV, Ticker
from defacto.models import SupplyDemand
import pandas as pd
import math


def calc_supply_demand_all(ticker):
    success=False
    data_list=[]
    for i in range(len(ticker)):
        code = ticker[i].code
        print(code)
        name = ticker[i].name
        print(name)
        bs_queryset = BuySell.objects.all()
        date_value = bs_queryset.filter(code=code).distinct('date').order_by('date').values_list('date')
        institution_value = bs_queryset.filter(code=code).distinct('date').order_by('date').values_list('institution')
        foreigner_value = bs_queryset.filter(code=code).distinct('date').order_by('date').values_list('foreigner')
        list_date = [data[0] for data in date_value]
        list_instutions = [data[0] for data in institution_value]
        list_foreigner = [data[0] for data in foreigner_value]
        ohlcv_queryset = OHLCV.objects.all()
        close_price_date = ohlcv_queryset.filter(code=code).distinct('date').order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('date')
        list_close_price_date = [data[0] for data in close_price_date]
        close_price = ohlcv_queryset.filter(code=code).order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('close_price')
        list_close_price = [data[0] for data in close_price]
        buysell_pandas = pd.DataFrame({'institution':list_instutions, 'foreigner':list_foreigner}, index=list_date)
        cp_pandas = pd.DataFrame({'close_price':list_close_price}, index=list_close_price_date)
        data_pandas = pd.concat([buysell_pandas,cp_pandas], axis=1)
        # data_pandas['close_price'] = [0 if math.isnan(x) else x for x in data_pandas['close_price']]
        data_pandas['institution_possession'] = data_pandas['institution'].cumsum()
        data_pandas['institution_possession'] = data_pandas['institution_possession'] + abs(min(data_pandas['institution_possession']))
        data_pandas['institution_possession'] = [1 if x==0 else x for x in data_pandas['institution_possession']] # 0을 로 변환
        data_pandas['institution_average_price'] = data_pandas['close_price']*data_pandas['institution']
        data_pandas['institution_average_price'] = data_pandas['institution_average_price'].cumsum()
        data_pandas['institution_average_price'] = round(data_pandas['institution_average_price']/data_pandas['institution_possession'],3)
        data_pandas['foreigner_possesion'] = data_pandas['foreigner'].cumsum()
        data_pandas['foreigner_possesion'] = data_pandas['foreigner_possesion'] + abs(min(data_pandas['foreigner_possesion']))
        data_pandas['foreigner_possesion'] = [1 if x==0 else x for x in data_pandas['foreigner_possesion']]
        data_pandas['foreigner_average_price'] = data_pandas['close_price']*data_pandas['foreigner']
        data_pandas['foreigner_average_price'] = data_pandas['foreigner_average_price'].cumsum()
        data_pandas['foreigner_average_price'] = round(data_pandas['foreigner_average_price']/data_pandas['foreigner_possesion'],3)
        data_pandas = data_pandas.fillna(0, inplace=True)
        for i in range(data_pandas.shape[0]):
            date = data_pandas.index[i]
            code = code
            name = name
            institution_possession = data_pandas.iloc[i,2]
            institution_average_price = data_pandas.iloc[i,3]
            foreigner_possesion = data_pandas.iloc[i,4]
            foreigner_average_price = data_pandas.iloc[i,5]
            tmp = SupplyDemand(date=date,name=name,code=code,institution_possession=institution_possession,institution_average_price=institution_average_price,
                                foreigner_possesion=foreigner_possesion, foreigner_average_price=foreigner_average_price)
            data_list.append(tmp)
    print("complet loop")
    SupplyDemand.objects.bulk_create(data_list)
    success=True
    return success, "Data calculate complete"




@task(name="calc-buysell-01")
def calc_buysell_1():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[:ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-02")
def calc_buysell_2():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-03")
def calc_buysell_3():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-04")
def calc_buysell_4():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-05")
def calc_buysell_5():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-06")
def calc_buysell_6():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-07")
def calc_buysell_7():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-08")
def calc_buysell_8():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[7*ticker_cut:8*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-09")
def calc_buysell_9():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[8*ticker_cut:9*ticker_cut]
    calc_supply_demand_all(ticker_list)

@task(name="calc-buysell-10")
def calc_buysell_10():
    date_value = Ticker.objects.all().distinct('date').order_by('date').values_list('date')
    list_date = [data[0] for data in date_value]
    date = list_date[-1]
    ticker = Ticker.objects.filter(date=date).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[9*ticker_cut:]
    calc_supply_demand_all(ticker_list)
