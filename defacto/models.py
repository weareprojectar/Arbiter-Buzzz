from django.db import models

# Create your models here.
class SupplyDemand(models.Model):
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    # volume = models.IntegerField(blank=True, null=True)
    individual_possession = models.BigIntegerField(blank=True, null=True)
    institution_possession = models.BigIntegerField(blank=True, null=True)
    foreigner_possession = models.BigIntegerField(blank=True, null=True)
    individual_average_price = models.FloatField(blank=True, null=True)
    institution_average_price = models.FloatField(blank=True, null=True)
    foreigner_average_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)

class DefactoData(models.Model):
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    individual_coefficient = models.FloatField()
    institution_coefficient = models.FloatField()
    foreigner_coefficient = models.FloatField()
    individual_tvalue = models.FloatField()
    institution_tvalue = models.FloatField()
    foreigner_tvalue = models.FloatField()
    individual_rank = models.IntegerField(blank=True, null=True)
    institution_rank = models.IntegerField(blank=True, null=True)
    foreigner_rank = models.IntegerField(blank=True, null=True)
    total_rank = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)


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
    lead_agent = models.CharField(max_length=10,
                                  blank=True,
                                  null=True)

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

    def __str__(self):
        return '{}'.format(self.code)
