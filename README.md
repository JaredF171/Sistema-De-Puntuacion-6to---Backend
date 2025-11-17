# Sistema de Calificaciones - Backend (Django + DRF)

Proyecto generado con arquitectura hexagonal: dominio (core), puertos (interfaces) y adaptadores (entradas HTTP y salida MySQL).

Instrucciones rápidas:

1. Crear y activar un virtualenv

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Crear la base de datos MySQL (ejemplo):

```sql
CREATE DATABASE evaluacion360 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Configurar `.env` si es necesario y ejecutar migraciones:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Endpoints:
- POST /api/events/  -> crear evento
- GET  /api/events/  -> listar eventos
- POST /api/evaluations/ -> enviar evaluación
- GET /api/evaluations/average/{user_id}/ -> promedio usuario
