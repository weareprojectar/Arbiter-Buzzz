from rest_framework import serializers
from defacto.models import SupplyDemand,Defacto


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

class DefactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defacto
        fields = ('id',
                'date',
                'name',
                'code',
                'institution_coefficient',
                'foreigner_coefficient',
                'institution_rank',
                'foreigner_rank',
                'score',)
