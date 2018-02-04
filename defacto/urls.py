from django.conf.urls import url
from defacto.views import SupplyDemandAPIView

urlpatterns = [
    url(r'^supplydemand/$', SupplyDemandAPIView.as_view(), name='supply-demand'),
]
