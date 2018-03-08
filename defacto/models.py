from django.db import models


class AgentData(models.Model):
    date = models.CharField(max_length=8)
    code = models.CharField(max_length=6)
    ind_possession = models.BigIntegerField(blank=True, null=True)
    for_possession = models.BigIntegerField(blank=True, null=True)
    ins_possession = models.BigIntegerField(blank=True, null=True)
    cor_possession = models.BigIntegerField(blank=True, null=True)
    ind_apps = models.FloatField(blank=True, null=True)
    for_apps = models.FloatField(blank=True, null=True)
    ins_apps = models.FloatField(blank=True, null=True)
    cor_apps = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)


class ScoreData(models.Model):
    date = models.CharField(max_length=8)
    code = models.CharField(max_length=6)
    absolute_score = models.FloatField(blank=True, null=True)
    relative_score = models.FloatField(blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    score_rank = models.IntegerField(blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    score_change = models.FloatField(blank=True, null=True)
    lead_agent = models.CharField(max_length=20,
                                  blank=True,
                                  null=True)

    def __str__(self):
        return '{}'.format(self.code)


class RankData(models.Model):
    date = models.CharField(max_length=8)
    code = models.CharField(max_length=6)
    lead_agent = models.CharField(max_length=20, blank=True, null=True)
    total_score = models.FloatField(blank=True, null=True)
    cartegory = models.CharField(max_length=40, blank=True, null=True)
    rank_change = models.IntegerField(blank=True, null=True)
    sign = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.code)
