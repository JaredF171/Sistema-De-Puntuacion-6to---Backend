from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/', include('src.app.api.routes.urls')),
    path('api/auth/token/', obtain_auth_token),
]
