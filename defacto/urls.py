from django.conf.urls import url
from defacto.views import (
    SupplyDemandAPIView,
    DefactoAPIView,
    ScannerView,
    AgentDataAPIView,
    ScoreDataAPIView,
)

urlpatterns = [
    url(r'^supplydemand/$', SupplyDemandAPIView.as_view(), name='supply-demand'),
    url(r'^score/$', DefactoAPIView.as_view(), name='score'),

    url(r'^agent-data/$', AgentDataAPIView.as_view(), name='agent-data'),
    url(r'^score-data/$', ScoreDataAPIView.as_view(), name='score-data'),

    url(r'^$', ScannerView.as_view(), name='home'),
]
