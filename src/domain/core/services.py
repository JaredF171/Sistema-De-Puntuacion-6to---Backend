from typing import List
from datetime import datetime
from src.domain.core.entities import Event, Evaluation
from src.domain.ports.inbound.evaluacion_service_port import EvaluacionServicePort
from src.domain.ports.out.evaluacion_repository_port import EvaluacionRepositoryPort

class EvaluacionService(EvaluacionServicePort):
    def __init__(self, repo: EvaluacionRepositoryPort):
        self.repo = repo

    def crear_evento(self, event: Event) -> Event:
        if event.start_date > event.end_date:
            raise ValueError("La fecha de inicio no puede ser mayor a la de fin")
        return self.repo.guardar_evento(event)

    def listar_eventos(self) -> List[Event]:
        return self.repo.obtener_eventos()

    def enviar_evaluacion(self, evaluation: Evaluation) -> Evaluation:
        evaluation.created_at = datetime.now()
        return self.repo.guardar_evaluacion(evaluation)

    def obtener_promedio_usuario(self, user_id: int) -> float:
        evaluaciones = self.repo.obtener_evaluaciones_usuario(user_id)
        total, count = 0, 0
        for ev in evaluaciones:
            for ans in ev.answers:
                total += ans.score
                count += 1
        return total / count if count > 0 else 0.0
