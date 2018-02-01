from django.conf.urls import url

from marketsignal.views import MarketSignalView

urlpatterns = [
    url(r'^$', MarketSignalView.as_view(), name='home'),
]
