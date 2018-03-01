from rest_framework import serializers
from marketsignal.models import Index, MarketScore


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('id',
                  'date',
                  'name',
                  'index',
                  'volume',
                  'category',)

class MarketScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketScore
        fields = ('date',
                  'name',
                  'momentum',
                  'volatility',
                  'correlation',
                  'volume',
                  'momentum_score',
                  'volatility_score',
                  'correlation_score',
                  'volume_score',
                  'total_score',
                  'score_rating',)
