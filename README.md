# Sistema de Calificaciones (Backend)

Pequeña API en Django REST Framework para gestionar eventos y evaluaciones tipo 360.

Requisitos
- Windows 10/11 o similar
- Python 3.10+ (recomendado)
- MySQL disponible (opcional si quieres persistir datos)

Pasos rápidos (PowerShell)

1) Instalar Python (si no está instalado)

- Ve a https://www.python.org/downloads/windows/ y descarga el instalador de Python 3.10/3.11/3.12.
- Durante la instalación, marca "Add Python to PATH".

2) Crear entorno virtual e instalar dependencias

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

3) Variables de entorno

Crear un fichero `.env` en la raíz del proyecto con al menos:

```
SECRET_KEY=dev-secret
DB_NAME=evaluacion360
*** Begin README

# Sistema de Calificaciones (Backend)

Pequeña API en Django REST Framework para gestionar eventos y evaluaciones tipo 360.

Requisitos
- Windows 10/11 o similar (o Linux/macOS con Docker Desktop)
- Python 3.11 (recomendado para desarrollo local)
- Docker Desktop (opcional, recomendado para desarrollo con MySQL)

Contenido rápido
- Instrucciones de desarrollo local (virtualenv)
- Ejecución con Docker Compose (recomendado)
- CI (GitHub Actions) para ejecutar tests

Instalación local (virtualenv)

1) Crear entorno virtual e instalar dependencias

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2) Variables de entorno

Copia `.env.example` a `.env` y ajusta según tu entorno:

```powershell
cp .env.example .env
# editar .env si es necesario
```

3) Migraciones y arrancar (local sin Docker)

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ejecutar tests localmente

```powershell
# Ejecutar toda la suite (usa SQLite en memoria durante tests)
python manage.py test --verbosity 2

# O ejecutar tests unitarios con unittest discovery
python -m unittest discover -v
```

Endpoints principales

- POST `/api/events/`  -> Crear evento
- GET  `/api/events/`  -> Listar eventos
- POST `/api/evaluations/` -> Enviar evaluación
- GET `/api/evaluations/average/{user_id}/` -> Obtener promedio del usuario

Ejemplos de request/responses están en el código y en los tests (`tests/test_api_endpoints.py`).

Usar Docker Desktop (recomendado para desarrollo con MySQL)

1) Copia el archivo de ejemplo de entorno y ajusta si quieres:

```powershell
cp .env.example .env
# editar .env si es necesario
```

2) Levantar con Docker Compose:

```powershell
docker-compose up --build
```

Esto levantará dos servicios:
- `db`: MySQL 8.0 (base de datos `evaluacion360`, usuario `evaluacion_user` por defecto)
- `web`: la aplicación Django en `0.0.0.0:8000`

Para ejecución en background:

```powershell
docker-compose up -d --build
```

Ver logs del servicio web:

```powershell
docker-compose logs -f web
```

Parar y eliminar contenedores:

```powershell
docker-compose down
```

Notas sobre Docker
- Las credenciales por defecto están en `.env.example`. No comites tu `.env`.
- `web` monta el código (`.:/app`) para facilitar desarrollo (recarga de código). No usar así en producción.
- Si prefieres `gunicorn` en producción, indícamelo y actualizo `Dockerfile`.

CI — GitHub Actions

Se incluyó un workflow básico en `.github/workflows/ci.yml` que:
- Se ejecuta en `push` y `pull_request` a `main`, `master` y `develop`.
- Corre la suite de tests con Python 3.11 en `ubuntu-latest`, `windows-latest` y `macos-latest`.

El flujo principal del workflow:

- Checkout del repositorio
- Setup de Python
- Cache de pip
- Instalación de dependencias desde `requirements.txt`
- Ejecución de `python manage.py test --verbosity 2`

Si quieres la matriz más reducida (solo `ubuntu-latest`), dímelo y la simplifico para ejecuciones más rápidas.

Buenas prácticas
- Mantén `.env` fuera del repositorio. Solo comitea `.env.example`.
- Para entornos de CI, configura variables de entorno secretas en GitHub Actions (Settings → Secrets) y no uses credenciales en texto claro.

Contribuir

1. Crea una rama feature/fix
2. Haz pruebas localmente y/o con Docker Compose
3. Abre un PR; el CI ejecutará las pruebas automáticamente

Gracias — dime si quieres que añada instrucciones para despliegue en producción (Gunicorn + Nginx, Dockerfile optimizado), o que actualice el README con ejemplos curl para los endpoints.

*** End README
2. Crear la base de datos MySQL (ejemplo):
