from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api.views import (
    UserAPIView,
    UserDetailsAPIView,
    UserLoginAPIView,
    ProfileAPIView,
    ProfileDetailsAPIView,
)

accounts_api_urlpatterns = [
    # token maker
    url(r'^get-token/', obtain_auth_token),

    # basic user login, info urls
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^user/$', UserAPIView.as_view(), name="user"),
    url(r'^user/(?P<username>[\w.@+-]+)/$',
        UserDetailsAPIView.as_view(), name="user-details"),

    # user profile related urls
    url(r'^profile/$', ProfileAPIView.as_view(), name="profile"),
    url(r'^profile/(?P<pk>[\w.@+-]+)/$',
        ProfileDetailsAPIView.as_view(), name="profile-details"),
]
