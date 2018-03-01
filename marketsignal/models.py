from django.db import models

INDEX_TYPES = (
    ('S', 'Size'),
    ('ST', 'Style'),
    ('I', 'Industry'),
)


class Index(models.Model):
    date = models.CharField(max_length=8)
    name = models.CharField(max_length=15)
    index = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=2,
                                choices=INDEX_TYPES,
                                blank=True,
                                null=True)

    def __str__(self):
        return self.name


class MarketScore(models.Model):
    date = models.CharField(max_length=8)
    name = models.CharField(max_length=15)
    momentum = models.FloatField(blank=True, null=True)
    volatility = models.FloatField(blank=True, null=True)
    correlation = models.FloatField(blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)
    momentum_score = models.IntegerField(blank=True, null=True)
    volatility_score = models.IntegerField(blank=True, null=True)
    correlation_score = models.IntegerField(blank=True, null=True)
    volume_score = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    score_rating = models.CharField(max_length=10,
                                    blank=True,
                                    null=True)

    def __str__(self):
        return self.name


class MSHome(models.Model):
    date = models.CharField(max_length=8)

    kospi_index = models.FloatField(blank=True, null=True)
    kospi_change = models.FloatField(blank=True, null=True)
    kospi_rate = models.FloatField(blank=True, null=True)
    kosdaq_index = models.FloatField(blank=True, null=True)
    kosdaq_change = models.FloatField(blank=True, null=True)
    kosdaq_rate = models.FloatField(blank=True, null=True)

    l_index = models.FloatField(blank=True, null=True)
    l_score = models.IntegerField(blank=True, null=True)
    l_change = models.IntegerField(blank=True, null=True)
    l_state = models.CharField(max_length=20, blank=True, null=True)
    m_index = models.FloatField(blank=True, null=True)
    m_score = models.IntegerField(blank=True, null=True)
    m_change = models.IntegerField(blank=True, null=True)
    m_state = models.CharField(max_length=20, blank=True, null=True)
    s_index = models.FloatField(blank=True, null=True)
    s_score = models.IntegerField(blank=True, null=True)
    s_change = models.IntegerField(blank=True, null=True)
    s_state = models.CharField(max_length=20, blank=True, null=True)

    g_index = models.FloatField(blank=True, null=True)
    g_score = models.IntegerField(blank=True, null=True)
    g_change = models.IntegerField(blank=True, null=True)
    g_state = models.CharField(max_length=20, blank=True, null=True)
    v_index = models.FloatField(blank=True, null=True)
    v_score = models.IntegerField(blank=True, null=True)
    v_change = models.IntegerField(blank=True, null=True)
    v_state = models.CharField(max_length=20, blank=True, null=True)

    ind_1_index = models.CharField(max_length=20, blank=True, null=True)
    ind_1_score = models.IntegerField(blank=True, null=True)
    ind_1_change = models.IntegerField(blank=True, null=True)
    ind_1_state = models.CharField(max_length=20, blank=True, null=True)
    ind_2_index = models.CharField(max_length=20, blank=True, null=True)
    ind_2_score = models.IntegerField(blank=True, null=True)
    ind_2_change = models.IntegerField(blank=True, null=True)
    ind_2_state = models.CharField(max_length=20, blank=True, null=True)
    ind_3_index = models.CharField(max_length=20, blank=True, null=True)
    ind_3_score = models.IntegerField(blank=True, null=True)
    ind_3_change = models.IntegerField(blank=True, null=True)
    ind_3_state = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.date


class MSHome2(models.Model):
    date = models.CharField(max_length=8)

    kospi_index = models.FloatField(blank=True, null=True)
    kospi_change = models.FloatField(blank=True, null=True)
    kospi_rate = models.FloatField(blank=True, null=True)
    kosdaq_index = models.FloatField(blank=True, null=True)
    kosdaq_change = models.FloatField(blank=True, null=True)
    kosdaq_rate = models.FloatField(blank=True, null=True)

    l_index = models.FloatField(blank=True, null=True)
    l_score = models.IntegerField(blank=True, null=True)
    l_change = models.IntegerField(blank=True, null=True)
    l_state = models.CharField(max_length=20, blank=True, null=True)
    m_index = models.FloatField(blank=True, null=True)
    m_score = models.IntegerField(blank=True, null=True)
    m_change = models.IntegerField(blank=True, null=True)
    m_state = models.CharField(max_length=20, blank=True, null=True)
    s_index = models.FloatField(blank=True, null=True)
    s_score = models.IntegerField(blank=True, null=True)
    s_change = models.IntegerField(blank=True, null=True)
    s_state = models.CharField(max_length=20, blank=True, null=True)

    g_index = models.FloatField(blank=True, null=True)
    g_score = models.IntegerField(blank=True, null=True)
    g_change = models.IntegerField(blank=True, null=True)
    g_state = models.CharField(max_length=20, blank=True, null=True)
    v_index = models.FloatField(blank=True, null=True)
    v_score = models.IntegerField(blank=True, null=True)
    v_change = models.IntegerField(blank=True, null=True)
    v_state = models.CharField(max_length=20, blank=True, null=True)

    ind_1_index = models.CharField(max_length=20, blank=True, null=True)
    ind_1_score = models.IntegerField(blank=True, null=True)
    ind_1_change = models.IntegerField(blank=True, null=True)
    ind_1_state = models.CharField(max_length=20, blank=True, null=True)
    ind_2_index = models.CharField(max_length=20, blank=True, null=True)
    ind_2_score = models.IntegerField(blank=True, null=True)
    ind_2_change = models.IntegerField(blank=True, null=True)
    ind_2_state = models.CharField(max_length=20, blank=True, null=True)
    ind_3_index = models.CharField(max_length=20, blank=True, null=True)
    ind_3_score = models.IntegerField(blank=True, null=True)
    ind_3_change = models.IntegerField(blank=True, null=True)
    ind_3_state = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.date


class RankData(models.Model):
    filter_by = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    num = models.IntegerField()
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    momentum_score = models.IntegerField(blank=True, null=True)
    volatility_score = models.IntegerField(blank=True, null=True)
    volume_score = models.IntegerField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.code
