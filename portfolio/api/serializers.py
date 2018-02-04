import time, datetime
from decimal import Decimal
import numpy as np
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from portfolio.algorithms import BlackLitterman, EAA, PortfolioAlgorithm
from portfolio.analysis import InitialPortfolio
from portfolio.models import Portfolio, PortfolioDiagnosis, PortfolioHistory, TodayPortfolio
from stockapi.models import Info, StockInfo, Ticker, OHLCV, Specs

User = get_user_model()


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id',
                  'user',
                  'name',
                  'capital',
                  'portfolio_type',
                  'description',
                  'created',
                  'updated',)


class PortfolioHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioHistory
        fields = ('id',
                  'portfolio',
                  'date',
                  'code',
                  'status',
                  'quantity',
                  'price',)


class PortfolioRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioDiagnosis
        fields = ('id',
                  'portfolio',
                  'ratio',)


class TodayPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayPortfolio
        fields = ('date', 'portfolio')


### Data Analysis Serializers ###
# needs to fix optimization issues...
class PortfolioDiagnosisSerializer(serializers.ModelSerializer):
    stock_num = serializers.SerializerMethodField()
    port_info = serializers.SerializerMethodField()
    port_specs = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ('id',
                  'user',
                  'name',
                  'capital',
                  'portfolio_type',
                  'description',
                  'stock_num',
                  'port_info',
                  'port_specs',
                  'created',
                  'updated',)

    def get_stock_num(self, obj):
        return obj.history.count()

    def get_port_info(self, obj):
        # STEP 1: Calculate portfolio ratio
        ### performance: 2s ###
        stocks = obj.history.all()
        capital = obj.capital
        ip = InitialPortfolio(obj, stocks, capital)
        ratio_dict = ip.ratio_dict

        port_info = {'status': '동일 비중 포트폴리오', 'ratio': ratio_dict}
        pa = PortfolioAlgorithm(ratio_dict)
        r, v, sr, yield_r, bt = pa.portfolio_info()
        new_bt = pa.change_bt_format(bt)
        port_info['return'] = float(format(round(yield_r, 3)*100, '.3f'))
        port_info['average_return'] = float(format(round(r, 3)*100, '.3f'))
        port_info['average_volatility'] = float(format(round(v, 3)*100, '.3f'))
        port_info['sharpe_ratio'] = float(format(round(sr, 3), '.3f'))
        port_info['backtest_result'] = new_bt
        return port_info

    def get_port_specs(self, obj):
        stocks = obj.history.all()
        stock_counts = stocks.count()
        mom_s, volt_s, cor_s, vol_s, tot_s = 0, 0, 0, 0, 0
        for stock in stocks:
            code = stock.code.code
            specs = Specs.objects.filter(code=stock.code.code).order_by('date').first()
            mom_s += specs.momentum_score
            volt_s += specs.volatility_score
            cor_s += specs.correlation_score
            vol_s += specs.volume_score
            tot_s += (specs.momentum_score + specs.volatility_score + specs.correlation_score + specs.volume_score)/4
        mom_s = mom_s//stock_counts
        volt_s = volt_s//stock_counts
        cor_s = cor_s//stock_counts
        vol_s = vol_s//stock_counts
        tot_s = int(tot_s//stock_counts)
        return [tot_s, mom_s, volt_s, cor_s, vol_s]


class PortfolioOptimizationSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ('id',
                  'user',
                  'name',
                  'capital',
                  'portfolio_type',
                  'description',
                  'result',
                  'created',
                  'updated',)

    def get_result(self, obj):
        ratio_dict = PortfolioDiagnosis.objects.filter(portfolio=obj).order_by('-id').first().ratio
        old_weights = []
        for key, val in ratio_dict.items():
            if key != 'cash':
                ratio_data = [val['name'], float(val['ratio'])]
                old_weights.append(ratio_data)
        eaa = EAA(ratio_dict)
        r, v, sr, yield_r, bt, weights = eaa.backtest_EAA()
        new_bt = eaa.change_bt_format(bt)
        # bl = BlackLitterman(ratio_dict)
        # weights = bl.optimize()
        # r, v, sr, yield_r, bt = bl.new_portfolio_info(weights)
        # new_bt = bl.change_bt_format(bt)
        stock_counts = len(weights)
        port_info = {'status': '최적화 포트폴리오'}
        port_info['old_weights'] = old_weights
        port_info['weights'] = [[old_weights[i][0], weights[i]] for i in range(stock_counts)]
        weight_diffs = []
        for i in range(stock_counts):
            code = eaa.settings['ticker_list'][i]
            name = port_info['weights'][i][0]
            weight_diff = port_info['weights'][i][1] - port_info['old_weights'][i][1]
            weight_diff = float(format(round(weight_diff, 4), '.4f'))
            weight_diff_data = [name, code, weight_diff]
            weight_diffs.append(weight_diff_data)
        port_info['weight_differences'] = weight_diffs
        port_info['return'] = float(format(round(yield_r, 3)*100, '.3f'))
        port_info['average_return'] = float(format(round(r, 3)*100, '.3f'))
        port_info['average_volatility'] = float(format(round(v, 3)*100, '.3f'))
        port_info['sharpe_ratio'] = float(format(round(sr, 3), '.3f'))
        port_info['backtest_result'] = new_bt
        mom_s, volt_s, cor_s, vol_s, tot_s = 0, 0, 0, 0, 0
        score_weights = list(np.array(weights)/sum(weights))

        for i in range(stock_counts):
            code = eaa.settings['ticker_list'][i]
            specs = Specs.objects.filter(code=code).order_by('date').first()
            weight = score_weights[i]
            mom_s += int(specs.momentum_score*weight)
            volt_s += int(specs.volatility_score*weight)
            cor_s += int(specs.correlation_score*weight)
            vol_s += int(specs.volume_score*weight)
            tot_s += int(((specs.momentum_score + specs.volatility_score + specs.correlation_score + specs.volume_score)/4)*weight)
        port_info['port_specs'] = [tot_s, mom_s, volt_s, cor_s, vol_s]

        market_dict = {}
        size_dict = {}
        ind_dict = {}
        for i in range(stock_counts):
            code = eaa.settings['ticker_list'][i]
            weight = port_info['weights'][i][1]
            # market types
            market_type = Ticker.objects.filter(code=code).first().market_type
            market_name = '코스피' if market_type == 'KP' else '코스닥'
            if not market_name in market_dict.keys():
                market_dict[market_name] = weight
            else:
                market_dict[market_name] += weight
            # size types, industry types
            info = Info.objects.filter(code=code).order_by('-date').first()
            size_type = info.size_type
            industry = info.industry
            if size_type == 'L':
                size_type = '대형주'
            elif size_type == 'M':
                size_type = '중형주'
            else:
                size_type = '소형주'
            if not size_type in size_dict.keys():
                size_dict[size_type] = weight
            else:
                size_dict[size_type] += weight
            if not industry in ind_dict.keys():
                ind_dict[industry] = weight
            else:
                ind_dict[industry] += weight
        port_info['market'] = market_dict.items()
        port_info['size'] = size_dict.items()
        port_info['industry'] = ind_dict.items()
        return port_info
