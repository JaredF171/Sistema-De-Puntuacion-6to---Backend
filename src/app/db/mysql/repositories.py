from django.db import IntegrityError

from src.domain.core.entities import Event, Evaluation, EvaluationAnswer
from src.domain.ports.out.evaluacion_repository_port import EvaluacionRepositoryPort
from src.app.db.mysql.models import EventModel, EvaluationModel, EvaluationAnswerModel

class EvaluacionMySQLRepository(EvaluacionRepositoryPort):

    def guardar_evento(self, event: Event) -> Event:
        obj = EventModel.objects.create(
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            admin_id=event.admin_id
        )
        event.id = obj.id
        return event

    def obtener_eventos(self):
        return [
            Event(
                id=e.id, name=e.name, description=e.description,
                start_date=e.start_date, end_date=e.end_date, admin_id=e.admin_id
            )
            for e in EventModel.objects.all()
        ]

    def guardar_evaluacion(self, evaluation: Evaluation) -> Evaluation:
        try:
            event = EventModel.objects.get(id=evaluation.event_id)
        except EventModel.DoesNotExist as exc:
            raise ValueError("El evento especificado no existe.") from exc

        try:
            ev = EvaluationModel.objects.create(
                event=event,
                evaluated_user_id=evaluation.evaluated_user_id,
                evaluator_user_id=evaluation.evaluator_user_id,
                type=evaluation.type
            )
        except IntegrityError as exc:
            raise ValueError("Ya existe una evaluación para este evaluador y evaluado en este evento.") from exc

        for ans in evaluation.answers:
            EvaluationAnswerModel.objects.create(
                evaluation=ev, criterion_id=ans.criterion_id,
                score=ans.score, comment=ans.comment
            )
        evaluation.id = ev.id
        evaluation.created_at = ev.created_at
        return evaluation

    def obtener_evaluaciones(self, *, event_id: int | None = None, evaluated_user_id: int | None = None, evaluator_user_id: int | None = None):
        qs = EvaluationModel.objects.prefetch_related("answers")
        if event_id is not None:
            qs = qs.filter(event_id=event_id)
        if evaluated_user_id is not None:
            qs = qs.filter(evaluated_user_id=evaluated_user_id)
        if evaluator_user_id is not None:
            qs = qs.filter(evaluator_user_id=evaluator_user_id)
        return self._map_evaluations(qs)

    def obtener_evaluaciones_usuario(self, user_id: int):
        evals = EvaluationModel.objects.filter(evaluated_user_id=user_id).prefetch_related("answers")
        return self._map_evaluations(evals)

    def _map_evaluations(self, queryset):
        result = []
        for e in queryset:
            answers = [
                EvaluationAnswer(criterion_id=a.criterion_id, score=a.score, comment=a.comment)
                for a in e.answers.all()
            ]
            result.append(Evaluation(
                id=e.id, event_id=e.event_id, evaluated_user_id=e.evaluated_user_id,
                evaluator_user_id=e.evaluator_user_id, type=e.type,
                created_at=e.created_at, answers=answers
            ))
        return result
