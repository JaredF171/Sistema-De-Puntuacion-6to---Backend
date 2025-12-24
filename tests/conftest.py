import os

# Forzamos SQLite en pruebas para evitar dependencias de MySQL y Docker.
os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
from django.core.management import call_command


django.setup()


def pytest_configure():
    """Ensure database schema is ready before tests run."""
    # run_syncdb permite crear las tablas si aún no hay migraciones aplicadas
    call_command("migrate", run_syncdb=True, verbosity=0)
