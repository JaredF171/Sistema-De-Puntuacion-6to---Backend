from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from src.domain.core.entities import Event, Evaluation, EvaluationAnswer
from src.domain.core.services import EvaluacionService
from src.app.db.mysql.repositories import EvaluacionMySQLRepository

repo = EvaluacionMySQLRepository()
service = EvaluacionService(repo)

class EventController(APIView):
    def get(self, request):
        events = service.listar_eventos()
        return Response([e.__dict__ for e in events])

    def post(self, request):
        data = request.data
        event = Event(
            id=None,
            name=data["name"],
            description=data.get("description", ""),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            admin_id=data["admin_id"]
        )
        saved = service.crear_evento(event)
        return Response(saved.__dict__, status=status.HTTP_201_CREATED)

class EvaluationController(APIView):
    def post(self, request):
        data = request.data
        answers = [EvaluationAnswer(**a) for a in data["answers"]]
        evaluation = Evaluation(
            id=None,
            event_id=data["event_id"],
            evaluated_user_id=data["evaluated_user_id"],
            evaluator_user_id=data["evaluator_user_id"],
            type="360",
            created_at=datetime.now(),
            answers=answers
        )
        saved = service.enviar_evaluacion(evaluation)
        return Response(saved.__dict__, status=status.HTTP_201_CREATED)

class AverageController(APIView):
    def get(self, request, user_id):
        avg = service.obtener_promedio_usuario(user_id)
        return Response({"evaluated_user_id": user_id, "average_score": avg})
