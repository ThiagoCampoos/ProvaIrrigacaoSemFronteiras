from django.contrib import admin
from django.urls import path, include

from people.views import UserCreate, CustomObtainAuthToken, UserRetrieve, DashboardView
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/v1/', include('people.urls')),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/', UserRetrieve.as_view(), name='user_retrieve'),
    path("login/", CustomObtainAuthToken.as_view(), name="login"),
    path('api-token-auth/', obtain_auth_token, name='api_token_path'),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),
]
