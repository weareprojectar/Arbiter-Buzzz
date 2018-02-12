from rest_framework import serializers
from defacto.models import SupplyDemand,DefactoData


class SupplyDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyDemand
        fields = ('id',
                'date',
                'name',
                'code',
                # 'volume',
                'individual_possession',
                'institution_possession',
                'foreigner_possession',
                'individual_average_price',
                'institution_average_price',
                'foreigner_average_price',)

class DefactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefactoData
        fields = ('id',
                'date',
                'name',
                'code',
                'individual_coefficient',
                'institution_coefficient',
                'foreigner_coefficient',
                'individual_tvalue',
                'institution_tvalue',
                'foreigner_tvalue',
                'individual_rank',
                'institution_rank',
                'foreigner_rank',
                'total_rank',
                'score',)
