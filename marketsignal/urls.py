from django.conf.urls import url

from marketsignal.views import MarketSignalView, SnapshotView

urlpatterns = [
    url(r'^$', MarketSignalView.as_view(), name='home'),
    url(r'^snapshot/(?P<code>[\w.@+-]+)/$', SnapshotView.as_view(), name='snapshot'),
]
