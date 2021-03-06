from rest_framework import serializers
from stockapi.models import (
    Ticker,
    StockInfo,
    Specs,
    OHLCV,
    KospiOHLCV,
    KosdaqOHLCV,
    Info,
    Financial,
    FinancialRatio,
    QuarterFinancial,
    DailyBuySell,
    WeeklyBuySell,

    KospiWeeklyBuy,
    KosdaqWeeklyBuy,
    ETFWeeklyBuy,
    KospiWeeklySell,
    KosdaqWeeklySell,
    ETFWeeklySell,
    KospiWeeklyNet,
    KosdaqWeeklyNet,
    ETFWeeklyNet,
)


class BMSerializer(serializers.ModelSerializer):
    class Meta:
        from stockapi.models import BM
        model = BM
        fields = ('date',
                  'name',
                  'index',
                  'volume',
                  'individual',
                  'foreigner',
                  'institution',)


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = ('code',)


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'market_type',)


class StockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'market_type',
                  'price',
                  'volume',)


class SpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specs
        fields = ('code',
                  'date',
                  'momentum',
                  'volatility',
                  'correlation',
                  'volume',
                  'momentum_score',
                  'volatility_score',
                  'correlation_score',
                  'volume_score',
                  'total_score',)


class RankSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Specs
        fields = ('code',
                  'name',
                  'momentum_score',
                  'volatility_score',
                  'volume_score',
                  'total_score',)

    def get_name(self, obj):
        return Ticker.objects.filter(code=obj.code).first().name


class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = ('date',
                  # 'name',
                  'code',
                  # 'market_type',
                  'open_price',
                  'close_price',
                  'high_price',
                  'low_price',
                  'volume',)


class KospiOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'close_price',
                  'high_price',
                  'low_price',
                  'volume',)


class KosdaqOHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqOHLCV
        fields = ('date',
                  'code',
                  'open_price',
                  'close_price',
                  'high_price',
                  'low_price',
                  'volume',)


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'market_type',
                  'industry',
                  'market_cap',
                  'market_cap_rank',
                  'face_val',
                  'stock_nums',
                  'price',
                  'foreign_limit',
                  'foreign_ratio',
                  'foreign_possession',
                  'per',
                  'eps',
                  'pbr',
                  'bps',
                  'yield_ret',
                  'industry_per',
                  'size_type',
                  'style_type',)


class FinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financial
        fields = ('id',
                  'date',
                  'code',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'asset',
                  'debt',
                  'capital',)


class FinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRatio
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'debt_ratio',
                  'profit_ratio',
                  'net_profit_ratio',
                  'consolidate_profit_ratio',
                  'net_ROE',
                  'consolidate_ROE',
                  'revenue_growth',
                  'profit_growth',
                  'net_profit_growth',)


class QuarterFinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterFinancial
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'revenue',
                  'profit',
                  'net_profit',
                  'consolidate_profit',
                  'profit_ratio',
                  'net_profit_ratio',)


class DailyBuySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBuySell
        fields = ('id',
                  'date',
                  'name',
                  'code',
                  'close_price',
                  'institution',
                  'foreigner',)


class WeeklyBuySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBuySell
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


##### Kiwoom Buy & Sell data
class KospiWeeklyBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiWeeklyBuy
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqWeeklyBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqWeeklyBuy
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFWeeklyBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFWeeklyBuy
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KospiWeeklySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiWeeklySell
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqWeeklySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqWeeklySell
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFWeeklySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFWeeklySell
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KospiWeeklyNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KospiWeeklyNet
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class KosdaqWeeklyNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = KosdaqWeeklyNet
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)


class ETFWeeklyNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETFWeeklyNet
        fields = ('id',
                  'date',
                  'code',
                  'name',
                  'short',
                  'individual',
                  'foreign_retail',
                  'institution',
                  'financial',
                  'insurance',
                  'trust',
                  'etc_finance',
                  'bank',
                  'pension',
                  'private',
                  'nation',
                  'etc_corporate',
                  'foreign',)
