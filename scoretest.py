from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import math
import time
import os, sys, glob

start_path = os.getcwd()
proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbiter.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV, Ticker
from defacto.models import SupplyDemand, DefactoData
import pandas as pd
import numpy as np
import math
import time
import statsmodels.formula.api as smf

ticker = SupplyDemand.objects.all().distinct('code')
ticker_count = ticker.count()
sd_queryset = SupplyDemand.objects.all()
ohlcv_queryset = OHLCV.objects.all()
print(ticker_count)


data_list = []
A = time.time()
for i in range(ticker_count):
    B = time.time()
    code = ticker[i].code
    print(code)
    name = ticker[i].name
    loop = i
    bs_qs = sd_queryset.filter(code=code).distinct('date').order_by('date').values_list('date','institution_possession','foreigner_possession')
    list_date = [data[0] for data in bs_qs]
    list_institution_possession = [data[1] for data in bs_qs]
    list_foreigner_possession = [data[2] for data in bs_qs]
    tmp_pandas_1 = pd.DataFrame({'institution_possession':list_institution_possession, 'foreigner_possession': list_foreigner_possession}, index=list_date)
    cp_qs= ohlcv_queryset.filter(code=code).distinct('date').order_by('date').filter(date__gte=list_date[0]).filter(date__lte=list_date[-1]).values_list('date','close_price')
    list_close_price_date = [data[0] for data in cp_qs]
    list_close_price = [data[1] for data in cp_qs]
    tmp_pandas_2 = pd.DataFrame({'close_price':list_close_price}, index=list_close_price_date)
    data_pandas = pd.concat([tmp_pandas_1, tmp_pandas_2], axis=1)
    data_pandas.index = pd.to_datetime(data_pandas.index)
    date_list = sorted(list(set(data_pandas.index.strftime('%Y-%m'))))
    for date in date_list[:-1]:
        try:
            result = smf.ols(formula='close_price ~ institution_possession + foreigner_possession', data=data_pandas[date]).fit()
            ip_coef = round(result.params[1],4)
            fp_coef = round(result.params[2],4)
            if result.tvalues[1] == np.inf:
                ip_tv = 0
            else:
                ip_tv = round(result.tvalues[1],4)
            if result.tvalues[2] == np.inf:
                fp_tv = 0
            else:
                fp_tv = round(result.tvalues[2],4)
            ip_total = 0.5*ip_coef + 0.5*ip_tv
            fp_total = 0.5*fp_coef + 0.5*ip_tv
        except ValueError:
            ip_coef = 0
            fp_coef = 0
            ip_tv = 0
            fp_tv = 0
            ip_total = 0
            fp_total = 0
        except IndexError:
            ip_coef = 0
            fp_coef = 0
            ip_tv = 0
            fp_tv = 0
            ip_total = 0
            fp_total = 0
        month_list=[date,code,ip_coef,fp_coef,ip_tv,fp_tv,ip_total,fp_total]
        data_list.append(month_list)
    C = time.time()
    percent = round((loop/len(ticker))*100,2)
    print(percent,"%",C-B)
print('complete')
Labels = ['date','code','institution_coefficient','foreigner_coefficient','institution_tvalue','foreigner_tvalue','institution_total','foreigner_total']
rank_pandas = pd.DataFrame(data_list,columns=Labels)
rank_pandas.fillna(0, inplace =True)
rank_pandas['institution_rank'] = rank_pandas.groupby('date')['institution_total'].rank(ascending=False)
rank_pandas['foreigner_rank'] = rank_pandas.groupby('date')['foreigner_total'].rank(ascending=False)
rank_pandas['tmp_score'] = 0.5*(1-(rank_pandas['institution_rank']/ticker_count))+0.5*(1-(rank_pandas['foreigner_rank']/ticker_count))
rank_pandas['total_rank'] = rank_pandas.groupby('date')['tmp_score'].rank(ascending=False)
rank_pandas['total_score'] = round((1-(rank_pandas['total_rank']/ticker_count)),2) *100
rank_pandas.to_csv('score.csv')
qs = []
for i in range(rank_pandas.shape[0]):
    date = rank_pandas['date'][i]
    code = rank_pandas['code'][i]
    institution_coefficient = rank_pandas['institution_coefficient'][i]
    foreigner_coefficient = rank_pandas['institution_coefficient'][i]
    institution_tvalue = rank_pandas['institution_tvalue'][i]
    foreigner_tvalue = rank_pandas['foreigner_tvalue'][i]
    institution_rank = rank_pandas['institution_rank'][i]
    foreigner_rank = rank_pandas['foreigner_rank'][i]
    total_rank = rank_pandas['total_rank'][i]
    score = rank_pandas['total_score'][i]
    tmp_qs = DefactoData(date=date,code=code,institution_coefficient=institution_coefficient,foreigner_coefficient=foreigner_coefficient,
                        institution_tvalue=institution_tvalue,foreigner_tvalue=foreigner_tvalue,institution_rank=institution_rank,
                        foreigner_rank=foreigner_rank, total_rank=total_rank, score=score)
    qs.append(tmp_qs)
DefactoData.objects.bulk_create(qs)
E = time.time()
print(E-A)
