from rest_framework import serializers
from defacto.models import (
    SupplyDemand,
    DefactoData,
    AgentData,
    ScoreData,
)


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


class AgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentData
        fields = ('date',
                  'code',
                  'ind_possession',
                  'for_possession',
                  'ins_possession',
                  'cor_possession',
                  'ind_apps',
                  'for_apps',
                  'ins_apps',
                  'cor_apps',
                  'lead_agent',)


class ScoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreData
        fields = ('date',
                  'code',
                  'absolute_score',
                  'relative_score',
                  'total_score',
                  'score_rank',
                  'rank_change',
                  'score_change',)
