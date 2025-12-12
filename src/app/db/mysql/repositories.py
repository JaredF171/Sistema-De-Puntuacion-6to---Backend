from src.domain.core.entities import Event, Evaluation, EvaluationAnswer, Respondent
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
        ev = EvaluationModel.objects.create(
            event_id=evaluation.event_id,
            evaluated_user_id=evaluation.evaluated_user_id,
            evaluator_user_id=evaluation.evaluator_user_id,
            evaluator_email=evaluation.evaluator_email,
            type=evaluation.type
        )
        for ans in evaluation.answers:
            EvaluationAnswerModel.objects.create(
                evaluation=ev, criterion_id=ans.criterion_id,
                score=ans.score, comment=ans.comment
            )
        evaluation.id = ev.id
        return evaluation

    def obtener_evaluaciones_usuario(self, user_id: int):
        evals = EvaluationModel.objects.filter(evaluated_user_id=user_id).prefetch_related("answers")
        result = []
        for e in evals:
            answers = [
                EvaluationAnswer(criterion_id=a.criterion_id, score=a.score, comment=a.comment)
                for a in e.answers.all()
            ]
            result.append(Evaluation(
                id=e.id, event_id=e.event_id, evaluated_user_id=e.evaluated_user_id,
                evaluator_user_id=e.evaluator_user_id, evaluator_email=e.evaluator_email, type=e.type,
                created_at=e.created_at, answers=answers
            ))
        return result

    def obtener_personas_encuestadas(self):
        evaluaciones = EvaluationModel.objects.all().order_by("-created_at")
        return [
            Respondent(
                evaluation_id=e.id,
                event_id=e.event_id,
                evaluated_user_id=e.evaluated_user_id,
                evaluator_user_id=e.evaluator_user_id,
                evaluator_email=e.evaluator_email,
                created_at=e.created_at,
            )
            for e in evaluaciones
        ]
