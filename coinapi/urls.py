from django.conf.urls import include, url
from coinapi.views import (
    CandleAPIView,
    PriceAPIView,
    PriceDetailAPIView,
    CandleDetailAPIView,
    MMAPIView,
)

urlpatterns = [
    url(r'^upbitchart/$', CandleAPIView.as_view(), name = 'upbit-chart'),
    url(r'^upbitprice/$', PriceAPIView.as_view(), name='upbit-price'),
    url(r'^upbitmm/$',MMAPIView.as_view(), name = 'upbit-mm'),
    url(r'^upbitchart/(?P<pk>\d+)/$', CandleDetailAPIView.as_view(), name = 'upbit-chart-detail'),
    url(r'^upbitprice/(?P<pk>\d+)/$', PriceDetailAPIView.as_view(), name='upbit-price-detail'),
]
