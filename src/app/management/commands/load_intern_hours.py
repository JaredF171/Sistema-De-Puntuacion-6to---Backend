from django.core.management.base import BaseCommand

from src.app.data.intern_hours_seed import INTERN_HOURS
from src.app.db.mysql.models import InternHoursModel


class Command(BaseCommand):
    help = "Carga los registros históricos de horas de practicantes en la base de datos (MySQL o SQLite)."

    def handle(self, *args, **options):
        created, updated = 0, 0
        for row in INTERN_HOURS:
            payload = dict(
                name=row[0],
                horas=row[1],
                horas_jul_oct=row[2],
                horas_acumuladas=row[3],
                horas_necesarias=row[4],
                horas_restantes_2212=row[5],
                falta_sobra=row[6],
                faltaria_sobraria=row[7],
                total=row[8],
                cumplimiento_pct=row[9],
            )
            obj, was_created = InternHoursModel.objects.update_or_create(
                name=payload["name"],
                defaults=payload,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Datos de practicantes cargados. Nuevos: {created}, actualizados: {updated}."
            )
        )
