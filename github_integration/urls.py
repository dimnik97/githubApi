from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import ApiUserData, ApiProjectsData, ApiLinkAuthorization, ApiUserAccessToken, Logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('get_user_data/', ApiUserData.as_view()),
    path('get_projects_data/', ApiProjectsData.as_view()),
    path('get_auth_link/', ApiLinkAuthorization.as_view()),
    path('get_auth_token/', ApiUserAccessToken.as_view()),
    url(r'^logout/', Logout.as_view()),
]
