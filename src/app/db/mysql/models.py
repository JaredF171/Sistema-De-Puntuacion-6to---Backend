from django.db import models

class EventModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    admin_id = models.IntegerField()

class EvaluationModel(models.Model):
    event = models.ForeignKey(
        EventModel,
        related_name="evaluations",
        on_delete=models.CASCADE,
        db_column="event_id",
        null=True,
        blank=True,
    )
    evaluated_user_id = models.IntegerField()
    evaluator_user_id = models.IntegerField()
    type = models.CharField(max_length=20, default="360")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "evaluated_user_id", "evaluator_user_id")

class EvaluationAnswerModel(models.Model):
    evaluation = models.ForeignKey(EvaluationModel, related_name="answers", on_delete=models.CASCADE)
    criterion_id = models.IntegerField()
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)


class InternHoursModel(models.Model):
    """Horas trabajadas por practicantes (datos históricos)."""

    name = models.CharField(max_length=255, unique=True)
    horas = models.IntegerField()
    horas_jul_oct = models.IntegerField()
    horas_acumuladas = models.IntegerField()
    horas_necesarias = models.IntegerField()
    horas_restantes_2212 = models.IntegerField()
    falta_sobra = models.IntegerField()
    faltaria_sobraria = models.IntegerField()
    total = models.IntegerField()
    cumplimiento_pct = models.IntegerField(help_text="Porcentaje entero de cumplimiento (ej. 79 = 79%)")

    class Meta:
        db_table = "intern_hours"
        ordering = ["name"]
