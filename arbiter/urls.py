from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import (
    HomeView,
    login_view,
    logout_view,
)

urlpatterns = [
    ### common ###
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', admin.site.urls),

    ### restapi ###
    url(r'^api/', include('buzzzapi.urls', namespace='api')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    ### cryptocurrency restapi
    url(r'^coin-api/', include('coinapi.urls', namespace='coinapi')),

    ### stock data restapi ###
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),

    ### buzzz tool specific ###
    url(r'^marketsignal/', include('marketsignal.urls', namespace='marketsignal')), # general views
    url(r'^ms-api/', include('marketsignal.api.urls', namespace='ms-api')), # api views
    url(r'^defacto/', include('defacto.urls', namespace='defacto')), # general views
    url(r'^sd-api/', include('defacto.api.urls', namespace='sd-api')), # api views
    url(r'^rms/', include('rms.urls', namespace='rms')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
