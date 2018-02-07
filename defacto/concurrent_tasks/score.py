from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime, timedelta
from stockapi.models import BuySell, OHLCV, Ticker
from defacto.models import SupplyDemand
import pandas as pd
import math
import statsmodels.formula.api as smf

@task(name="compute_score")
def score_calc():
    success = False
    data_list = []
    ticker = Ticker.objects.all()
    ticker_count = ticker.count()
    print(ticker_count)
    for i in range(ticker_count):
        name = ticker[i].name
        code = ticker[i].code
        loop = i
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
        data_pandas.index = pd.to_datetime(data_pandas.index)
        date_list = sorted(list(set(data_pandas.index.strftime('%Y-%m'))))
        for date in date_list:
            result = smf.ols(formula='close_price ~ institution_possession + foreigner_possession', data=data_pandas[date]).fit()
            ip_coef = round(result.params[1],4)
            fp_coef = round(result.params[2],4)
            ip_tv = round(result.tvalues[1],4)
            fp_tv = round(result.tvalues[2],4)
            ip_total = 0.5*ip_coef + 0.5*ip_tv
            fp_total = 0.5*fp_coef + 0.5*ip_tv
            month_list=[date,code,ip_coef,fp_coef,ip_tv,fp_tv,ip_total,fp_total]
            data_list.append(month_list)
        C = time.time()
        percent = round((loop/len(ticker))*100,2)
        print(percent,"%",C-B)
    Labels = ['date','code','institution_coefficient','foreigner_coefficient','institution_tvalue','foreigner_tvalue','institution_total','foreigner_total']
    rank_pandas = pd.DataFrame(data_list,columns=Labels)
    rank_pandas['institution_rank'] = rank_pandas.groupby('date')['institution_total'].rank(ascending=False)
    rank_pandas['foreigner_rank'] = rank_pandas.groupby('date')['foreigner_total'].rank(ascending=False)
    rank_pandas['tmp_score'] = 0.5*(1-(rank_pandas['institution_rank']/ticker_count))+0.5*(1-(rank_pandas['foreigner_rank']/ticker_cut))
    rank_pandas['total_rank'] = rank_pandas.groupby('date')['tmp_score'].rank(ascending=False)
    rank_pandas['total_score'] = round((1-(rank_pandas['total_rank']/ticker_count)),2) *100
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
    D = time.time()
    print(D-A)
    success = True
    return success, "data calculate complete"
