from django.conf.urls import url
from marketsignal.api.views import IndexAPIView

marketsignal_urlpatterns = [
    url(r'^index/$', IndexAPIView.as_view(), name='index'),
]
