# Cuando Django importe el paquete `src.app.api`, importamos los modelos para registrarlos
try:
    # Importar modelos para que Django los detecte en las migraciones
    from src.app.db.mysql import models  # noqa: F401
except Exception:
    # En tiempo de análisis o si las dependencias no están instaladas, ignorar
    pass
