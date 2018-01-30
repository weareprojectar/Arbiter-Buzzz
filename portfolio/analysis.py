import math, datetime, time
from datetime import datetime
import pandas as pd

from portfolio.models import Portfolio, PortfolioDiagnosis, PortfolioHistory
from stockapi.models import Ticker, OHLCV, Specs


class InitialPortfolio(object):

    '''Analyzes equal proportion portfolio'''

    def __init__(self, portfolio, stocks, capital):
        ### param: portfolio (Django - Model Instance)
        ### param: stocks (Django - Queryset)
        ### param: capital (int)

        # instance attributes initialization
        port = {
            'portfolio': portfolio,
            'stocks': stocks,
            'stock_count': stocks.count(),
            'capital': capital
        }
        port['capital_per_stock'] = port['capital']//port['stock_count']
        self.port_params = port
        self.ratio_dict = {'cash': 0}
        self.ohlcv_inst_list = []

        # run initial methods
        self.initial_distribution()
        self.redistribute()

    def initial_distribution(self):
        port = self.port_params

        for stock in port['stocks']:
            code = stock.code.code
            ohlcv = OHLCV.objects.filter(code=code).order_by('-date')
            if ohlcv.exists():
                ohlcv_inst = ohlcv.first()
                ticker_inst = Ticker.objects.filter(code=ohlcv_inst.code).order_by('-date').first()

                self.ohlcv_inst_list.append(ohlcv_inst)

                name = ticker_inst.name
                date = ohlcv_inst.date
                close_price = int(ohlcv_inst.close_price)
                stock_data = {
                    'name': name,
                    'date': date,
                    'price': close_price
                }
                self.ratio_dict[code] = stock_data
                capital_per_stock = port['capital_per_stock']
                if close_price < capital_per_stock:
                    stock_num = capital_per_stock//close_price
                    invested = int(stock_num * close_price)
                    self.ratio_dict[code]['invested'] = invested
                    self.ratio_dict[code]['buy_num'] = stock_num
                    self.ratio_dict['cash'] += (capital_per_stock - invested)
                else:
                    self.ratio_dict[code]['invested'] = 0
                    self.ratio_dict[code]['buy_num'] = 0
            else:
                continue

    def redistribute(self):
        left_over_capital = self.ratio_dict['cash']
        ohlcv_inst_list = self.ohlcv_inst_list
        redistribute = left_over_capital > 0
        while redistribute:
            extra_buy = list(filter(lambda x: x.close_price < left_over_capital, ohlcv_inst_list))
            if len(extra_buy) == 0:
                redistribute = False
                continue
            extra_capital_per_stock = left_over_capital//len(extra_buy)
            extra_buy_num = list(map(lambda x: extra_capital_per_stock//x.close_price, extra_buy))
            if sum(extra_buy_num) == 0:
                redistribute = False
                continue
            close_price_list = [ohlcv.close_price for ohlcv in extra_buy]
            reset_left_over = int(left_over_capital - sum(map(lambda x, y: x*y, extra_buy_num, close_price_list)))
            extra_stocks = [ohlcv.code for ohlcv in extra_buy]
            for i in range(len(extra_stocks)):
                extra_invested = extra_buy_num[i]*close_price_list[i]
                self.ratio_dict[extra_stocks[i]]['invested'] += int(extra_invested)
                self.ratio_dict[extra_stocks[i]]['buy_num'] += int(extra_buy_num[i])
            self.ratio_dict['cash'] = reset_left_over
            ohlcv_inst_list = extra_buy
            left_over_capital = reset_left_over
        for key, val in self.ratio_dict.items():
            if key != 'cash':
                stock_ratio = val['invested']/self.port_params['capital']
                self.ratio_dict[key]['ratio'] = float(format(round(stock_ratio, 4), '.4f'))
        pd_inst = PortfolioDiagnosis(portfolio=self.port_params['portfolio'], ratio=self.ratio_dict)
        pd_inst.save()

    # def initial_distribution_2(self):
    #     port = self.port_params
    #
    #     for stock in port['stocks']:
    #         code = stock.code.code
    #         ohlcv = OHLCV.objects.filter(code=code).order_by('-date')
    #         if ohlcv.exists():
    #             ohlcv_inst = ohlcv.first()
    #             ticker_inst = Ticker.objects.filter(code=ohlcv_inst.code).order_by('-date').first()
    #
    #             self.ohlcv_inst_list.append(ohlcv_inst)
    #
    #             name = ticker_inst.name
    #             date = ohlcv_inst.date
    #             close_price = int(ohlcv_inst.close_price)
    #             stock_data = {
    #                 'name': name,
    #                 'date': date,
    #                 'price': close_price,
    #                 'portion_per_stock': close_price/port['capital']
    #             }
    #             self.ratio_dict[code] = stock_data
    #     self._distribute()
    #
    # def _distribute(self):
    #     stock_count = self.port_params['stock_count']
    #     ticker_list = [ticker for ticker in self.ratio_dict.keys() if ticker != 'cash']
    #     portion_list = [self.ratio_dict[ticker]['portion_per_stock'] for ticker in ticker_list]
    #
    #     distribute = True
    #     stock_num_init = [1] * len(portion_list)
    #     stock_num_list = [0] * len(portion_list)
    #     while distribute:
    #         if sum(stock_num_list) == 0:
    #             port_portion = list(map(lambda num, portion: num * portion, stock_num_init, portion_list))
    #         else:
    #             port_portion = list(map(lambda num, portion: num * portion, stock_num_list, portion_list))
    #         portion_sum = sum(port_portion)
    #         if portion_sum < 1:
    #             max_portion = max(portion_list)
    #             new_buy_num_list = []
    #             for i in range(len(port_portion)):
    #                 buy_num = max_portion//portion_list[i]
    #                 new_buy_num_list.append(buy_num)
    #                 stock_num_list = list(map(lambda num, new_num: num + new_num - num))
    #                 print(new_buy_num_list)
    #         break
