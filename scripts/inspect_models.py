import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path para poder importar 'src' cuando
# ejecutamos este script directamente.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from src.app.db.mysql.models import EventModel, EvaluationModel, EvaluationAnswerModel

print('EventModel app_label=', EventModel._meta.app_label)
print('EventModel model_name=', EventModel._meta.model_name)
print('EventModel module=', EventModel.__module__)
print('EvaluationModel app_label=', EvaluationModel._meta.app_label)
print('EvaluationModel model_name=', EvaluationModel._meta.model_name)
print('EvaluationAnswerModel app_label=', EvaluationAnswerModel._meta.app_label)
print('EvaluationAnswerModel model_name=', EvaluationAnswerModel._meta.model_name)
