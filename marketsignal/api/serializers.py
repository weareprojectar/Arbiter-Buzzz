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


class MSHomeSerializer(serializers.ModelSerializer):
    bm_info = serializers.SerializerMethodField()
    size_info = serializers.SerializerMethodField()
    style_info = serializers.SerializerMethodField()
    industry_info = serializers.SerializerMethodField()

    class Meta:
        model = MarketScore
        fields = ('bm_info',
                  'size_info',
                  'style_info',
                  'industry_info',)

    def get_bm_info(self, obj):
        from stockapi.models import BM
        index_list = BM.objects.order_by('-date')[:4]
        kospi_index = []
        kosdaq_index = []
        for index_inst in index_list:
            index_name = index_inst.name
            if index_name == 'KOSPI':
                kospi_index.append(index_inst.index)
            elif index_name == 'KOSDAQ':
                kosdaq_index.append(index_inst.index)
        kospi_change = (kospi_index[0] - kospi_index[1])/kospi_index[1]
        kosdaq_change = (kosdaq_index[0] - kosdaq_index[1])/kosdaq_index[1]
        return {
            'kospi_index': kospi_index[0],
            'kospi_change': kospi_change,
            'kosdaq_index': kosdaq_index[0],
            'kosdaq_change': kosdaq_change
        }

    def get_size_info(self, obj):
        size_list = Index.objects.filter(category='S').order_by('-date')[:6]
        l_index = []
        m_index = []
        s_index = []
        for size_inst in size_list:
            index_name = size_inst.name
            if index_name == 'L':
                l_index.append(size_inst.index)
            elif index_name == 'M':
                m_index.append(size_inst.index)
            elif index_name == 'S':
                s_index.append(size_inst.index)
        l_change = (l_index[0] - l_index[1])/l_index[1]
        m_change = (m_index[0] - m_index[1])/m_index[1]
        s_change = (s_index[0] - s_index[1])/s_index[1]
        return {
            'l_index': l_index[0],
            'l_change': l_change,
            'm_index': m_index[0],
            'm_change': m_change,
            's_index': s_index[0],
            's_change': s_change
        }

    def get_style_info(self, obj):
        pass

    def get_industry_info(self, obj):
        pass
