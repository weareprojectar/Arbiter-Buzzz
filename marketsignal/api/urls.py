from django.conf.urls import url
from marketsignal.api.views import IndexAPIView, TopIndustryAPIView

marketsignal_urlpatterns = [
    url(r'^index/$', IndexAPIView.as_view(), name='index'),
    url(r'^top-industry/$', TopIndustryAPIView.as_view(), name='index'),
]
