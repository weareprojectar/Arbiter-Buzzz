# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-02 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.BigIntegerField()),
                ('ticker', models.CharField(max_length=10)),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.FloatField()),
                ('trade_price', models.IntegerField(blank=True)),
                ('mean_price', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('start', models.BigIntegerField()),
                ('end', models.BigIntegerField()),
                ('mm_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=20)),
                ('ticker', models.CharField(max_length=10)),
                ('price', models.FloatField()),
                ('volume', models.FloatField()),
                ('prev_price', models.IntegerField()),
                ('change', models.CharField(max_length=10)),
                ('ch_price', models.IntegerField()),
                ('AB', models.CharField(max_length=10)),
            ],
        ),
    ]
