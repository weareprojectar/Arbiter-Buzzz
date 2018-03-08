from rest_framework import serializers
from defacto.models import AgentData, ScoreData


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
                  'cor_apps',)


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
                  'score_change',
                  'lead_agent',)
