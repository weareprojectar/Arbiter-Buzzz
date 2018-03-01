from django.conf.urls import url
from marketsignal.api.views import (
    IndexAPIView,
    TopIndustryAPIView,
    MarketScoreAPIView,
    MSHomeAPIView,
)

marketsignal_urlpatterns = [
    url(r'^index/$', IndexAPIView.as_view(), name='index'),
    url(r'^top-industry/$', TopIndustryAPIView.as_view(), name='index'),
    url(r'^score/$', MarketScoreAPIView.as_view(), name='score'),
    url(r'^ms-info/(?P<pk>\d+)/$', MSHomeAPIView.as_view(), name='ms-info'),
]
