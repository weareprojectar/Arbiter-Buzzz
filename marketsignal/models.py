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
