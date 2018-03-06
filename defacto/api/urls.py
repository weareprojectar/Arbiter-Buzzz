from django.conf.urls import url

from defacto.api.views import AgentDataAPIView, ScoreDataAPIView

urlpatterns = [
    url(r'^agent-data/$', AgentDataAPIView.as_view(), name='agent-data'),
    url(r'^score-data/$', ScoreDataAPIView.as_view(), name='score-data'),
]
