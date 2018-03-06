from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from accounts.api.urls import accounts_api_urlpatterns
from portfolio.api.urls import portfolio_api_urlpatterns

urlpatterns = [
]

urlpatterns += accounts_api_urlpatterns
urlpatterns += portfolio_api_urlpatterns
urlpatterns = format_suffix_patterns(urlpatterns)
