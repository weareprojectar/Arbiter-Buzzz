from django.db import models

SIZE_TYPES = (
    ('L', 'Large Cap'), # 대형주
    ('M', 'Middle Cap'), # 중형주
    ('S', 'Small Cap'), # 소형주
)

STYLE_TYPES = (
    ('G', 'Growth'), # 성장주
    ('V', 'Value'), # 가치주
    ('D', 'Dividend'), # 배당주
)


# stock Ticker
class Ticker(models.Model):
    date = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    market_type = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


# on time stock price data(9-16)
class StockInfo(models.Model):
    date = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    market_type = models.CharField(max_length=10)
    price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.date, self.name)


# daily market OHLCV data(at 16 O`Clock)
class OHLCV(models.Model):
    date = models.CharField(max_length=16)
    code = models.CharField(max_length=6)
    open_price = models.IntegerField()
    high_price = models.IntegerField()
    low_price = models.IntegerField()
    close_price = models.IntegerField()
    volume = models.IntegerField()

    def __str__(self):
        return '{} {}'.format(self.code)


class Specs(models.Model):
    code = models.CharField(max_length=6)
    date = models.CharField(max_length=8)
    momentum = models.FloatField(blank=True, null=True)
    volatility = models.FloatField(blank=True, null=True)
    correlation = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    momentum_score = models.IntegerField(blank=True, null=True)
    volatility_score = models.IntegerField(blank=True, null=True)
    correlation_score = models.IntegerField(blank=True, null=True)
    volume_score = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.code


class Info(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    size_type = models.CharField(max_length=1,
                                 choices=SIZE_TYPES,
                                 blank=True,
                                 null=True) # 사이즈
    style_type = models.CharField(max_length=1,
                                  choices=STYLE_TYPES,
                                  blank=True,
                                  null=True) # 스타일
    market_type=models.CharField(max_length=10)
    face_val = models.CharField(max_length=10,
                                blank=True,
                                null=True) # 액면가
    stock_nums = models.BigIntegerField(blank=True, null=True) # 상장주식수
    price = models.IntegerField(blank=True)#당일 종가
    market_cap = models.BigIntegerField(blank=True, null=True) # 시가총액
    market_cap_rank = models.IntegerField(blank=True, null=True) # 시가총액 순위
    industry = models.CharField(max_length=50,
                                blank=True,
                                null=True) # 산업
    foreign_limit = models.BigIntegerField(blank=True, null=True)
    foreign_possession = models.BigIntegerField(blank=True, null=True)
    foreign_ratio = models.FloatField(blank=True, null=True)
    per = models.FloatField(blank=True, null=True) # PER로 성장주/가치주 구분
    eps = models.FloatField(blank=True, null=True)
    pbr = models.FloatField(blank=True, null=True)
    bps = models.FloatField(blank=True)
    industry_per = models.FloatField(blank=True)
    yield_ret = models.FloatField(blank=True, null=True) # 배당수익률

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class Financial(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    revenue = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    consolidate_profit = models.IntegerField(blank=True, null=True)
    asset = models.IntegerField(blank=True, null=True)
    debt = models.IntegerField(blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class FinancialRatio(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    debt_ratio = models.FloatField(blank=True, null=True)
    profit_ratio = models.FloatField(blank=True, null=True)
    net_profit_ratio = models.FloatField(blank=True, null=True)
    consolidate_profit_ratio = models.FloatField(blank=True, null=True)
    net_ROE = models.FloatField(blank=True, null=True)
    consolidate_ROE = models.FloatField(blank=True, null=True)
    revenue_growth = models.FloatField(blank=True, null=True)
    profit_growth = models.FloatField(blank=True, null=True)
    net_profit_growth = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class QuarterFinacial(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    revenue = models.IntegerField(blank=True, null=True)
    profit = models.IntegerField(blank=True, null=True)
    net_profit = models.IntegerField(blank=True, null=True)
    consolidate_profit = models.IntegerField(blank=True, null=True)
    profit_ratio = models.FloatField(blank=True, null=True)
    net_profit_ratio = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


class BuySell(models.Model):
    date = models.CharField(max_length=10)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    institution = models.IntegerField(blank=True, null=True)
    foreigner = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)
