from django.contrib import admin
from .models import EventModel, EvaluationModel, EvaluationAnswerModel


@admin.register(EventModel)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date", "admin_id")
    search_fields = ("name",)


@admin.register(EvaluationModel)
class EvaluationModelAdmin(admin.ModelAdmin):
    list_display = ("id", "event_id", "evaluated_user_id", "evaluator_user_id", "type", "created_at")
    list_filter = ("type",)


@admin.register(EvaluationAnswerModel)
class EvaluationAnswerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "evaluation", "criterion_id", "score")
