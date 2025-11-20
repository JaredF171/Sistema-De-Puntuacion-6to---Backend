from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class EvaluationAnswer:
    criterion_id: int
    score: int
    comment: Optional[str] = None

@dataclass
class Evaluation:
    id: Optional[int]
    event_id: int
    evaluated_user_id: int
    evaluator_user_id: int
    type: str
    created_at: datetime
    answers: List[EvaluationAnswer]

@dataclass
class Event:
    id: Optional[int]
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    admin_id: int
