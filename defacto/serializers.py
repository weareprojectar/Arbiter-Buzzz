from rest_framework import serializers
from defacto.models import SupplyDemand


class SupplyDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyDemand
        fields = ('id',
                'date',
                'name',
                'code',
                'volume',
                'institution_possession',
                'foreigner_possesion',
                'institution_average_price',
                'foreigner_average_price',)
