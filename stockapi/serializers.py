from rest_framework import serializers
from stockapi.models import (
    Info,
    Ticker,
    StockInfo,
    OHLCV,
)

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


class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'market_type',
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
