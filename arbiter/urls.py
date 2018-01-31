from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .views import HomeView, login_view, logout_view

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('buzzzapi.urls', namespace='api')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^coin-api/', include('coinapi.urls', namespace='coinapi')),
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),
    url(r'^marketsignal/', include('marketsignal.urls', namespace='marketsignal')),
    url(r'^rms/', include('rms.urls', namespace='rms')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
