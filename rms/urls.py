from django.conf.urls import url

# from django.views.generic.base import RedirectView

from rms.views import (
    RMSDiagnosisView,
    RMSHomeView,
    RMSStartView,
    RMSOptimizationView,
    RMSTodayPortfolioView,
)

urlpatterns = [
    url(r'^$', RMSHomeView.as_view(), name='home'),
    url(r'^start/$', RMSStartView.as_view(), name='start'),
    url(r'^today-portfolio/$', RMSTodayPortfolioView.as_view(), name='today-portfolio'),
    url(r'^diagnosis/(?P<pk>\d+)/$', RMSDiagnosisView.as_view(), name='diagnosis'),
    url(r'^optimization/(?P<pk>\d+)/$', RMSOptimizationView.as_view(), name='optimization'),
]
