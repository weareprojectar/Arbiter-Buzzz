from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV, Ticker
from defacto.models import SupplyDemand
import pandas as pd
import math
import statsmodels.formula.api as smf


def score_calc(ticker):
    date = datetime.now().strftime('%Y%m%d')
    data_list = []
    for i in range(len(ticker)):
        name = ticker[i].name
        code = ticker[i].code
        date_qs = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('date')
        institution_possession_qs = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('institution_possession')
        foreigner_possesion_qs = BuySell.objects.filter(code=code).distinct('date').order_by('date').values_list('foreigner_possesion')
        list_date = [data[0] for data in date_qs]
        list_institution_possession = [data[0] for data in institution_possession_qs]
        list_foreigner_possession = [data[0] for data in foreigner_possesion_qs]
        tmp_pandas_1 = pd.DataFrame({'institution_possession':list_institution_possession, 'foreigner_possession': list_foreigner_possession}, index=list_date)
        close_price_date = OHLCV.objects.filter(code=code).distinct('date').order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('date')
        list_close_price_date = [data[0] for data in close_price_date]
        close_price = OHLCV.objects.filter(code=code).order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('close_price')
        list_close_price = [data[0] for data in close_price]
        tmp_pandas_2 = pd.DataFrame({'close_price':list_close_price}, index=list_close_price_date)
        data_pandas = pd.concat([tmp_pandas_1, tmp_pandas_2], axis=1)
        result = smf.ols(formula='close_price~institution_possession+foreigner_possession', data=data_pandas).fit()
        result.summary()
