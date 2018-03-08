from django.conf.urls import url

from defacto.api.views import AgentDataAPIView, ScoreDataAPIView, RankDataAPIView

urlpatterns = [
    url(r'^agent-data/$', AgentDataAPIView.as_view(), name='agent-data'),
    url(r'^score-data/$', ScoreDataAPIView.as_view(), name='score-data'),
    url(r'^rank-data/$', RankDataAPIView.as_view(), name='rank-data'),
]
