from django.conf.urls import url
from defacto.views import ScannerView

urlpatterns = [
    url(r'^$', ScannerView.as_view(), name='home'),
]
