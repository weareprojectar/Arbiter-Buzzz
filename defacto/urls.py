from django.conf.urls import url
from defacto.views import SupplyDemandAPIView, DefactoAPIView

urlpatterns = [
    url(r'^supplydemand/$', SupplyDemandAPIView.as_view(), name='supply-demand'),
    url(r'^score/$', DefactoAPIView.as_view(), name='score'),
]
