from rest_framework import serializers
from stockapi.models import (
    Ticker,
    StockInfo,
    Specs,
    OHLCV,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinacial,
    BuySell,
)

class BMSerializer(serializers.ModelSerializer):
    class Meta:
        from stockapi.models import BM
        model = BM
        fields = ('date',
                  'name',
                  'index',
                  'volume',
                  'individual',
                  'foreigner',
                  'institution',)


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'market_type',)


class StockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'market_type',
                  'price',
                  'volume',)


class SpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specs
        fields = ('code',
                  'date',
                  'momentum',
                  'volatility',
                  'correlation',
                  'volume',
                  'momentum_score',
                  'volatility_score',
                  'correlation_score',
                  'volume_score',
                  'total_score',)


class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = ('date',
                  # 'name',
                  'code',
                  # 'market_type',
                  'open_price',
                  'close_price',
                  'high_price',
                  'low_price',
                  'volume',)


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'market_type',
                  'industry',
                  'market_cap',
                  'market_cap_rank',
                  'face_val',
                  'stock_nums',
                  'price',
                  'foreign_limit',
                  'foreign_ratio',
                  'foreign_possession',
                  'per',
                  'eps',
                  'pbr',
                  'bps',
                  'yield_ret',
                  'industry_per',
                  'size_type',
                  'style_type',)


class FinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financial
        fields = ('id',
                  'date',
                  'code',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'asset',
                  'debt',
                  'capital',)


class FinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRatio
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'debt_ratio',
                  'profit_ratio',
                  'net_profit_ratio',
                  'consolidate_profit_ratio',
                  'net_ROE',
                  'consolidate_ROE',
                  'revenue_growth',
                  'profit_growth',
                  'net_profit_growth',)


class QuarterFinacialSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterFinacial
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'profit_ratio',
                  'net_profit_ratio',)


class BuySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuySell
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'institution',
                  'foreigner',)
