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
    len_ticker = Ticker.objects.all()
    for i in range(len(ticker)):
        name = ticker[i].name
        code = ticker[i].code
        bs_qs = SupplyDemand.objects.filter(code=code).distinct('date').order_by('date').values_list('date','institution_possession','foreigner_possession')
        list_date = [data[0] for data in bs_qs]
        list_institution_possession = [data[1] for data in bs_qs]
        list_foreigner_possession = [data[2] for data in bs_qs]
        tmp_pandas_1 = pd.DataFrame({'institution_possession':list_institution_possession, 'foreigner_possession': list_foreigner_possession}, index=list_date)
        cp_qs= OHLCV.objects.filter(code=code).distinct('date').order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('date','close_price')
        list_close_price_date = [data[0] for data in cp_qs]
        list_close_price = [data[1] for data in cp_qs]
        tmp_pandas_2 = pd.DataFrame({'close_price':list_close_price}, index=list_close_price_date)
        data_pandas = pd.concat([tmp_pandas_1, tmp_pandas_2], axis=1)
        result = smf.ols(formula='close_price ~ institution_possession + foreigner_possession', data=data_pandas).fit()
        ip_coef = result.params[1]
        fp_coef = resutl.params[2]
        ip_tv = result.tvalues[1]
        fp_tv = result.tvalues[2]
        ip_total = 0.5*ip_coef + 0.5*ip_tv
        fp_total = 0.5*fp_coef + 0.5*ip_tv
        score_pandas = pd.DataFrame({'ip_coef':ip_coef,'fp_coef':fp_coef, 'ip_total':ip_total, 'fp_total':fp_total})
        score_pandas['']
