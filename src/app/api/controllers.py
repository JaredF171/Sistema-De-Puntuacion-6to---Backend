from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from src.domain.core.entities import Event, Evaluation, EvaluationAnswer
from src.domain.core.services import EvaluacionService
from src.app.db.mysql.repositories import EvaluacionMySQLRepository
from src.app.api.serializers import EventSerializer, EvaluationSerializer, InternHoursSerializer
from src.app.db.mysql.models import InternHoursModel

repo = EvaluacionMySQLRepository()
service = EvaluacionService(repo)


class EventController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            events = service.listar_eventos()
            serializer = EventSerializer(events, many=True)
            return Response({"status": "success", "data": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": "Error al obtener eventos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            event = Event(
                id=None,
                name=data["name"],
                description=data.get("description", ""),
                start_date=data["start_date"],
                end_date=data["end_date"],
                admin_id=data["admin_id"]
            )
            saved = service.crear_evento(event)
            return Response({"status": "success", "data": EventSerializer(saved).data}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"status": "error", "message": ve.detail, "details": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"status": "error", "message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": "Error al crear evento."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EvaluationController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {
            "event_id": request.query_params.get("event_id"),
            "evaluated_user_id": request.query_params.get("evaluated_user_id"),
            "evaluator_user_id": request.query_params.get("evaluator_user_id"),
        }
        parsed_filters = {k: int(v) for k, v in filters.items() if v is not None}
        evals = service.listar_evaluaciones(**parsed_filters)
        serializer = EvaluationSerializer(evals, many=True)
        return Response({"status": "success", "data": serializer.data})

    def post(self, request):
        try:
            serializer = EvaluationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            answers = [EvaluationAnswer(**a) for a in data["answers"]]
            evaluation = Evaluation(
                id=None,
                event_id=data["event_id"],
                evaluated_user_id=data["evaluated_user_id"],
                evaluator_user_id=data["evaluator_user_id"],
                type=data.get("type", "360"),
                created_at=data.get("created_at", datetime.now()),
                answers=answers
            )
            saved = service.enviar_evaluacion(evaluation)
            return Response({"status": "success", "data": EvaluationSerializer(saved).data}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"status": "error", "message": ve.detail, "details": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"status": "error", "message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": "Error al enviar evaluación."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AverageController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            avg = service.obtener_promedio_usuario(user_id)
            return Response({"status": "success", "data": {"evaluated_user_id": user_id, "average_score": avg}})
        except Exception:
            return Response({"status": "error", "message": "Error al calcular promedio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InternHoursController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = InternHoursModel.objects.all()
        serializer = InternHoursSerializer(records, many=True)
        return Response({"status": "success", "data": serializer.data})
