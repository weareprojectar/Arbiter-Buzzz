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
            name='BM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=10)),
                ('index', models.FloatField()),
                ('volume', models.IntegerField()),
                ('individual', models.IntegerField()),
                ('foreigner', models.IntegerField()),
                ('institution', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyBuySell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=50)),
                ('close_price', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('foreigner', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ETFWeeklyBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ETFWeeklyNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ETFWeeklySell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Financial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=10)),
                ('revenue', models.IntegerField(blank=True, null=True)),
                ('profit', models.IntegerField(blank=True, null=True)),
                ('net_profit', models.IntegerField(blank=True, null=True)),
                ('consolidate_profit', models.IntegerField(blank=True, null=True)),
                ('asset', models.IntegerField(blank=True, null=True)),
                ('debt', models.IntegerField(blank=True, null=True)),
                ('capital', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=50)),
                ('debt_ratio', models.FloatField(blank=True, null=True)),
                ('profit_ratio', models.FloatField(blank=True, null=True)),
                ('net_profit_ratio', models.FloatField(blank=True, null=True)),
                ('consolidate_profit_ratio', models.FloatField(blank=True, null=True)),
                ('net_roe', models.FloatField(blank=True, null=True)),
                ('consolidate_roe', models.FloatField(blank=True, null=True)),
                ('revenue_growth', models.FloatField(blank=True, null=True)),
                ('profit_growth', models.FloatField(blank=True, null=True)),
                ('net_profit_growth', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=50)),
                ('date', models.CharField(max_length=10)),
                ('size_type', models.CharField(blank=True, choices=[('L', 'Large Cap'), ('M', 'Middle Cap'), ('S', 'Small Cap')], max_length=1, null=True)),
                ('style_type', models.CharField(blank=True, choices=[('G', 'Growth'), ('V', 'Value'), ('D', 'Dividend')], max_length=1, null=True)),
                ('market_type', models.CharField(max_length=10)),
                ('face_val', models.CharField(blank=True, max_length=10, null=True)),
                ('stock_nums', models.BigIntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True)),
                ('market_cap', models.BigIntegerField(blank=True, null=True)),
                ('market_cap_rank', models.IntegerField(blank=True, null=True)),
                ('industry', models.CharField(blank=True, max_length=50, null=True)),
                ('foreign_limit', models.BigIntegerField(blank=True, null=True)),
                ('foreign_possession', models.BigIntegerField(blank=True, null=True)),
                ('foreign_ratio', models.FloatField(blank=True, null=True)),
                ('per', models.FloatField(blank=True, null=True)),
                ('eps', models.FloatField(blank=True, null=True)),
                ('pbr', models.FloatField(blank=True, null=True)),
                ('bps', models.FloatField(blank=True)),
                ('industry_per', models.FloatField(blank=True)),
                ('yield_ret', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KosdaqOHLCV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=16)),
                ('code', models.CharField(max_length=6)),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KosdaqWeeklyBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KosdaqWeeklyNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KosdaqWeeklySell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KospiOHLCV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=16)),
                ('code', models.CharField(max_length=6)),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='KospiWeeklyBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KospiWeeklyNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KospiWeeklySell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OHLCV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=16)),
                ('code', models.CharField(max_length=6)),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuarterFinancial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=50)),
                ('revenue', models.IntegerField(blank=True, null=True)),
                ('profit', models.IntegerField(blank=True, null=True)),
                ('net_profit', models.IntegerField(blank=True, null=True)),
                ('consolidate_profit', models.IntegerField(blank=True, null=True)),
                ('profit_ratio', models.FloatField(blank=True, null=True)),
                ('net_profit_ratio', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('date', models.CharField(max_length=8)),
                ('momentum', models.FloatField(blank=True, null=True)),
                ('volatility', models.FloatField(blank=True, null=True)),
                ('correlation', models.FloatField(blank=True, null=True)),
                ('volume', models.BigIntegerField(blank=True, null=True)),
                ('momentum_score', models.IntegerField(blank=True, null=True)),
                ('volatility_score', models.IntegerField(blank=True, null=True)),
                ('correlation_score', models.IntegerField(blank=True, null=True)),
                ('volume_score', models.IntegerField(blank=True, null=True)),
                ('total_score', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=6)),
                ('market_type', models.CharField(max_length=10)),
                ('price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=6)),
                ('market_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyBuySell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short', models.IntegerField(blank=True, null=True)),
                ('individual', models.IntegerField(blank=True, null=True)),
                ('foreign_retail', models.IntegerField(blank=True, null=True)),
                ('institution', models.IntegerField(blank=True, null=True)),
                ('financial', models.IntegerField(blank=True, null=True)),
                ('insurance', models.IntegerField(blank=True, null=True)),
                ('trust', models.IntegerField(blank=True, null=True)),
                ('etc_finance', models.IntegerField(blank=True, null=True)),
                ('bank', models.IntegerField(blank=True, null=True)),
                ('pension', models.IntegerField(blank=True, null=True)),
                ('private', models.IntegerField(blank=True, null=True)),
                ('nation', models.IntegerField(blank=True, null=True)),
                ('etc_corporate', models.IntegerField(blank=True, null=True)),
                ('foreign', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
