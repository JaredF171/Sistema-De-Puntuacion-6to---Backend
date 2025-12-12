from django.db import models

class EventModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    admin_id = models.IntegerField()

class EvaluationModel(models.Model):
    event_id = models.IntegerField()
    evaluated_user_id = models.IntegerField()
    evaluator_user_id = models.IntegerField()
    evaluator_email = models.EmailField(blank=True, null=True)
    type = models.CharField(max_length=20, default="360")
    created_at = models.DateTimeField(auto_now_add=True)

class EvaluationAnswerModel(models.Model):
    evaluation = models.ForeignKey(EvaluationModel, related_name="answers", on_delete=models.CASCADE)
    criterion_id = models.IntegerField()
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
