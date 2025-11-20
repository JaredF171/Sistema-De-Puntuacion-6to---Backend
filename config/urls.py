from django.urls import path, include

urlpatterns = [
    path('api/', include('src.app.api.routes.urls')),
]
