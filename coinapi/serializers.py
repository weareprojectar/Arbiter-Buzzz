from rest_framework import serializers
from coinapi.models import Candle , Price, MM


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = ('id',
                  'date',
                  'ticker',
                  'high_price',
                  'low_price',
                  'open_price',
                  'close_price',
                  'volume',
                  'trade_price',
                  'mean_price',)


class CandleMMSerializer(serializers.ModelSerializer):
    ticker = serializers.CharField()
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    mm_num = serializers.IntegerField()

    class Meta:
        model = MM
        fields = ('ticker',
                  'start',
                  'end',
                  'mm_num',)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id',
                  'date',
                  'ticker',
                  'price',
                  'vol',
                  'prev_price',
                  'change',
                  'ch_price',
                  'AB',)
