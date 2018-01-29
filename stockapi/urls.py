from django.conf.urls import url
from stockapi.views import (
    TickerAPIView,
    OHLCVAPIView,
    StockInfoAPIView,
)

urlpatterns = [
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
    url(r'^stockinfo/$', StockInfoAPIView.as_view(), name='info'),
    url(r'^ohlcv/$', OHLCVAPIView.as_view(), name='ohlcv'),
]
