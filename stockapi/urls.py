from django.conf.urls import url
from stockapi.views import (
    BMAPIView,
    CandleAPIView,
    TickerAPIView,
    TickerUpdatedAPIView,
    OHLCVAPIView,
    OHLCVNoPageAPIView,
    StockInfoAPIView,
    SpecsAPIView,
    InfoAPIView,
    FinancialAPIView,
    FinancialRatioAPIView,
    QuarterFinacialAPIView,
    BuySellAPIView,
)

urlpatterns = [
    url(r'^bm/$', BMAPIView.as_view(), name='bm'),
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
    url(r'^ticker-updated/$', TickerUpdatedAPIView.as_view(), name='ticker-updated'),
    url(r'^stockinfo/$', StockInfoAPIView.as_view(), name='stockinfo'),
    url(r'^specs/$', SpecsAPIView.as_view(), name='specs'),
    url(r'^ohlcv-data/$', OHLCVAPIView.as_view(), name='ohlcv-data'),
    url(r'^ohlcv/$', OHLCVNoPageAPIView.as_view(), name='ohlcv'),
    url(r'^candle/$', CandleAPIView.as_view(), name='candle'),
    url(r'^info/$', InfoAPIView.as_view(), name='info'),
    url(r'^financial/$', FinancialAPIView.as_view(), name='financial'),
    url(r'^financial-ratio/$', FinancialRatioAPIView.as_view(), name='financial-ratio'),
    url(r'^quarter-finacial/$', QuarterFinacialAPIView.as_view(), name='quarter-finacial'),
    url(r'^buysell/$', BuySellAPIView.as_view(), name='buysell'),
]
