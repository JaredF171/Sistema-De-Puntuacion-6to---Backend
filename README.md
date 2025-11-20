# Sistema de Calificaciones (Backend)

API en Django REST Framework para gestionar eventos y evaluaciones tipo 360.

## Requisitos

- Windows 10/11 o similar (o Linux/macOS)
- Python 3.10+ (recomendado 3.11)
- MySQL (opcional, el proyecto usa SQLite por defecto)

## Instalación Local

### 1) Crear entorno virtual e instalar dependencias

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Variables de entorno (opcional)

El proyecto funciona con SQLite por defecto sin necesidad de configuración. Si deseas usar MySQL, crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=dev-secret
DB_ENGINE=mysql
DB_NAME=evaluacion360
DB_USER=root
DB_PASS=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

**Nota:** Si no creas el archivo `.env`, el proyecto usará SQLite automáticamente.

### 3) Migraciones y arrancar

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Opcional: crear usuario admin
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`

## Ejecutar Tests

```powershell
# Ejecutar toda la suite (usa SQLite en memoria durante tests)
python manage.py test --verbosity 2

# O ejecutar tests unitarios con unittest discovery
python -m unittest discover -v
```

## Endpoints Principales

- `POST /api/events/` → Crear evento
- `GET  /api/events/` → Listar eventos
- `POST /api/evaluations/` → Enviar evaluación
- `GET /api/evaluations/average/{user_id}/` → Obtener promedio del usuario

Ejemplos de request/responses están en el código y en los tests (`tests/test_api_endpoints.py`).

## Configuración de Base de Datos

### SQLite (por defecto)

No requiere configuración. El archivo `db.sqlite3` se crea automáticamente en la raíz del proyecto.

### MySQL (opcional)

1. Instala MySQL en tu sistema
2. Crea la base de datos:
   ```sql
   CREATE DATABASE evaluacion360;
   ```
3. Configura las variables de entorno en `.env` como se muestra arriba
4. Ejecuta las migraciones:
   ```powershell
   python manage.py migrate
   ```

## CI — GitHub Actions

Se incluyó un workflow básico en `.github/workflows/ci.yml` que:
- Se ejecuta en `push` y `pull_request` a `main`, `master` y `develop`.
- Corre la suite de tests con Python 3.11 en `ubuntu-latest`, `windows-latest` y `macos-latest`.

## Buenas Prácticas

- Mantén `.env` fuera del repositorio. Solo comitea `.env.example` si existe.
- Para entornos de CI, configura variables de entorno secretas en GitHub Actions (Settings → Secrets) y no uses credenciales en texto claro.

## Contribuir

1. Crea una rama feature/fix
2. Haz pruebas localmente
3. Abre un PR; el CI ejecutará las pruebas automáticamente
