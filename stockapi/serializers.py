from rest_framework import serializers
from stockapi.models import (
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
