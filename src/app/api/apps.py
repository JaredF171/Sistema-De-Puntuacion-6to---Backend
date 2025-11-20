from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.app.api'

    def ready(self):
        # Importar los modelos de la capa de datos para asegurar que
        # Django los detecte y los incluya en las migraciones.
        try:
            from src.app.db.mysql import models  # noqa: F401
        except Exception:
            # Evitar fallos en entornos donde Django aún no esté inicializado
            pass
