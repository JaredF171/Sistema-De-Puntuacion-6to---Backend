from django.urls import path, include
from src.app.api.views import EvaluationLandingView

urlpatterns = [
    path('', EvaluationLandingView.as_view(), name='evaluation-form'),
    path('api/', include('src.app.api.routes.urls')),
]
