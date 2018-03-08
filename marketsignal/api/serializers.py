from rest_framework import serializers
from marketsignal.models import (
    Index,
    MarketScore,
    MSHome,
    RankData,
)

def format_decimal(data):
    return float(format(round(data, 2), '.2f'))

def change_to_pct(data):
    return float(format(round(data, 4), '.4f')) * 100


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


# class MSHomeSerializer(serializers.ModelSerializer):
#     bm_info = serializers.SerializerMethodField()
#     size_info = serializers.SerializerMethodField()
#     style_info = serializers.SerializerMethodField()
#     industry_info = serializers.SerializerMethodField()
#
#     class Meta:
#         model = MarketScore
#         fields = ('bm_info',
#                   'size_info',
#                   'style_info',
#                   'industry_info',)
#
#     def get_bm_info(self, obj):
#         from stockapi.models import BM
#         index_list = BM.objects.order_by('-date')[:4]
#         kospi_index = []
#         kosdaq_index = []
#         for index_inst in index_list:
#             index_name = index_inst.name
#             if index_name == 'KOSPI':
#                 kospi_index.append(index_inst.index)
#             elif index_name == 'KOSDAQ':
#                 kosdaq_index.append(index_inst.index)
#         kospi_change = kospi_index[0] - kospi_index[1]
#         kospi_rate = kospi_change/kospi_index[1]
#         kosdaq_change = kosdaq_index[0] - kosdaq_index[1]
#         kosdaq_rate = kosdaq_change/kosdaq_index[1]
#         return {
#             'kospi_index': format_decimal(kospi_index[0]),
#             'kospi_change': format_decimal(kospi_change),
#             'kospi_rate': change_to_pct(kospi_rate),
#             'kosdaq_index': format_decimal(kosdaq_index[0]),
#             'kosdaq_change': format_decimal(kosdaq_change),
#             'kosdaq_rate': change_to_pct(kosdaq_rate)
#         }
#
#     def get_size_info(self, obj):
#         size_list = Index.objects.filter(category='S').order_by('-date')[:3]
#         score_list = MarketScore.objects.filter(name__in=['L', 'M', 'S']).order_by('-date')[:6]
#
#         for size_inst in size_list:
#             index_name = size_inst.name
#             if index_name == 'L':
#                 l_index = size_inst.index
#             elif index_name == 'M':
#                 m_index = size_inst.index
#             elif index_name == 'S':
#                 s_index = size_inst.index
#
#         l_scores, m_scores, s_scores = [], [], []
#         for score_inst in score_list:
#             index_name = score_inst.name
#             if index_name == 'L':
#                 l_scores.append(score_inst.total_score)
#             elif index_name == 'M':
#                 m_scores.append(score_inst.total_score)
#             elif index_name == 'S':
#                 s_scores.append(score_inst.total_score)
#
#         return {
#             'l_index': format_decimal(l_index),
#             'l_score': l_scores[0],
#             'l_change': l_scores[0] - l_scores[1],
#             'm_index': format_decimal(m_index),
#             'm_score': m_scores[0],
#             'm_change': m_scores[0] - m_scores[1],
#             's_index': format_decimal(s_index),
#             's_score': s_scores[0],
#             's_change': s_scores[0] - s_scores[1]
#         }
#
#     def get_style_info(self, obj):
#         style_list = Index.objects.filter(category='ST').order_by('-date')[:4]
#         score_list = MarketScore.objects.filter(name__in=['G', 'V']).order_by('-date')[:4]
#
#         for style_inst in style_list:
#             index_name = style_inst.name
#             if index_name == 'G':
#                 g_index = style_inst.index
#             elif index_name == 'V':
#                 v_index = style_inst.index
#
#         g_scores, v_scores = [], []
#         for score_inst in score_list:
#             index_name = score_inst.name
#             if index_name == 'G':
#                 g_scores.append(score_inst.total_score)
#             elif index_name == 'V':
#                 v_scores.append(score_inst.total_score)
#
#         return {
#             'g_index': format_decimal(g_index),
#             'g_score': g_scores[0],
#             'g_change': g_scores[0] - g_scores[1],
#             'v_index': format_decimal(v_index),
#             'v_score': v_scores[0],
#             'v_change': v_scores[0] - v_scores[1]
#         }
#
#     def get_industry_info(self, obj):
#         industry_qs = Index.objects.filter(category='I')
#         last_date = industry_qs.order_by('-date').first().date
#         ranked_index = [data.name for data in industry_qs.filter(date=last_date).order_by('-index')[:3]]
#
#         industry_list = industry_qs.filter(name__in=ranked_index).order_by('-date')[:3]
#         score_list = MarketScore.objects.filter(name__in=ranked_index).order_by('-date')[:6]
#
#         for industry_inst in industry_list:
#             index_name = industry_inst.name
#             if index_name == ranked_index[0]:
#                 ind_1_index = industry_inst.index
#             elif index_name == ranked_index[1]:
#                 ind_2_index = industry_inst.index
#             elif index_name == ranked_index[2]:
#                 ind_3_index = industry_inst.index
#
#         ind_1_scores, ind_2_scores, ind_3_scores = [], [], []
#         for score_inst in score_list:
#             index_name = score_inst.name
#             if index_name == ranked_index[0]:
#                 ind_1_scores.append(score_inst.total_score)
#             elif index_name == ranked_index[1]:
#                 ind_2_scores.append(score_inst.total_score)
#             elif index_name == ranked_index[2]:
#                 ind_3_scores.append(score_inst.total_score)
#
#         return {
#             'ind_1_index': format_decimal(ind_1_index),
#             'ind_1_score': ind_1_scores[0],
#             'ind_1_change': ind_1_scores[0] - ind_1_scores[1],
#             'ind_2_index': format_decimal(ind_2_index),
#             'ind_2_score': ind_2_scores[0],
#             'ind_2_change': ind_2_scores[0] - ind_2_scores[1],
#             'ind_3_index': format_decimal(ind_3_index),
#             'ind_3_score': ind_3_scores[0],
#             'ind_3_change': ind_3_scores[0] - ind_3_scores[1]
#         }


class MSHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MSHome
        fields = ('date',
                  'kospi_index',
                  'kospi_change',
                  'kospi_rate',
                  'kosdaq_index',
                  'kosdaq_change',
                  'kosdaq_rate',
                  'l_index',
                  'l_score',
                  'l_change',
                  'l_state',
                  'm_index',
                  'm_score',
                  'm_change',
                  'm_state',
                  's_index',
                  's_score',
                  's_change',
                  's_state',
                  'g_index',
                  'g_score',
                  'g_change',
                  'g_state',
                  'v_index',
                  'v_score',
                  'v_change',
                  'v_state',
                  'ind_1_index',
                  'ind_1_score',
                  'ind_1_change',
                  'ind_1_state',
                  'ind_2_index',
                  'ind_2_score',
                  'ind_2_change',
                  'ind_2_state',
                  'ind_3_index',
                  'ind_3_score',
                  'ind_3_change',
                  'ind_3_state',)


class RankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankData
        fields = ('filter_by',
                  'date',
                  'num',
                  'code',
                  'name',
                  'momentum_score',
                  'volatility_score',
                  'volume_score',
                  'total_score',)
