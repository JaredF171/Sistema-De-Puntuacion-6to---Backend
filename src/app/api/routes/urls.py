from django.urls import path
from src.app.api.controllers import EventController, EvaluationController, AverageController, RespondentsController

urlpatterns = [
    path('events/', EventController.as_view()),
    path('evaluations/', EvaluationController.as_view()),
    path('evaluations/average/<int:user_id>/', AverageController.as_view()),
    path('evaluations/respondents/', RespondentsController.as_view()),
]
