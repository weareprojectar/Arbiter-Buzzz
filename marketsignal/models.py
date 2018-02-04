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
