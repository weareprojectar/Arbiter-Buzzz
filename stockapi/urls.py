from django.conf.urls import url
from stockapi.views import (
    InfoAPIView,
    TickerAPIView,
    OHLCVAPIView,
    StockInfoAPIView,
)

urlpatterns = [
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
    url(r'^stockinfo/$', StockInfoAPIView.as_view(), name='stockinfo'),
    url(r'^ohlcv/$', OHLCVAPIView.as_view(), name='ohlcv'),
    url(r'^info/$', InfoAPIView.as_view(), name='info'),
]
