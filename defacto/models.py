from django.db import models

# Create your models here.
class SupplyDemand(models.Model):
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    volume = models.IntegerField(blank=True, null=True)
    institution_possession = models.IntegerField(blank=True, null=True)
    foreigner_possesion = models.IntegerField(blank=True, null=True)
    institution_average_price = models.FloatField(blank=True, null=True)
    foreigner_average_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)

class DefactoData(models.Model):
    date = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    institution_coefficient = models.FloatField()
    foreigner_coefficient = models.FloatField()
    institution_rank = models.IntegerField(blank=True, null=True)
    foreigner_rank = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)
