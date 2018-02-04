from rest_framework import serializers
from marketsignal.models import Index


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('id',
                  'name',
                  'index',
                  'volume',
                  'category',)
