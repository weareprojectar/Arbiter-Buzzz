from django.conf.urls import url
from defacto.views import SupplyDemandAPIView, DefactoAPIView, ScannerView

urlpatterns = [
    url(r'^supplydemand/$', SupplyDemandAPIView.as_view(), name='supply-demand'),
    url(r'^score/$', DefactoAPIView.as_view(), name='score'),

    url(r'^$', ScannerView.as_view(), name='home'),
]
