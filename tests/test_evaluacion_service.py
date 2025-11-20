import unittest
from datetime import datetime, timedelta

from src.domain.core.entities import Event, Evaluation, EvaluationAnswer
from src.domain.core.services import EvaluacionService


class MockRepo:
    def __init__(self):
        self.events = []
        self.evaluations = []
        self._next_event_id = 1
        self._next_eval_id = 1

    def guardar_evento(self, event: Event) -> Event:
        event.id = self._next_event_id
        self._next_event_id += 1
        self.events.append(event)
        return event

    def obtener_eventos(self):
        return list(self.events)

    def guardar_evaluacion(self, evaluation: Evaluation) -> Evaluation:
        evaluation.id = self._next_eval_id
        self._next_eval_id += 1
        # ensure created_at is present
        if not hasattr(evaluation, 'created_at') or evaluation.created_at is None:
            evaluation.created_at = datetime.now()
        self.evaluations.append(evaluation)
        return evaluation

    def obtener_evaluaciones_usuario(self, user_id: int):
        return [e for e in self.evaluations if e.evaluated_user_id == user_id]


class EvaluacionServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = MockRepo()
        self.service = EvaluacionService(self.repo)

    def test_crear_evento_valido(self):
        start = datetime.now()
        end = start + timedelta(days=1)
        event = Event(id=None, name="Evento 1", description="", start_date=start, end_date=end, admin_id=1)
        saved = self.service.crear_evento(event)
        self.assertIsNotNone(saved.id)
        self.assertEqual(len(self.repo.events), 1)

    def test_crear_evento_fechas_invalidas(self):
        start = datetime.now()
        end = start - timedelta(days=1)
        event = Event(id=None, name="Evento 2", description="", start_date=start, end_date=end, admin_id=1)
        with self.assertRaises(ValueError):
            self.service.crear_evento(event)

    def test_enviar_evaluacion_y_promedio(self):
        # crear evaluacion con 3 respuestas
        answers = [EvaluationAnswer(criterion_id=1, score=4), EvaluationAnswer(criterion_id=2, score=6), EvaluationAnswer(criterion_id=3, score=5)]
        evaluation = Evaluation(id=None, event_id=1, evaluated_user_id=42, evaluator_user_id=99, type="360", created_at=datetime.now(), answers=answers)
        saved = self.service.enviar_evaluacion(evaluation)
        self.assertIsNotNone(saved.id)

        avg = self.service.obtener_promedio_usuario(42)
        self.assertAlmostEqual(avg, (4 + 6 + 5) / 3)


if __name__ == '__main__':
    unittest.main()
