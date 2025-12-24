from django.db import migrations, models

from src.app.data.intern_hours_seed import INTERN_HOURS


def seed_intern_hours(apps, schema_editor):
    InternHours = apps.get_model("app", "InternHoursModel")
    if InternHours.objects.exists():
        return

    objects = [
        InternHours(
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
        for row in INTERN_HOURS
    ]
    InternHours.objects.bulk_create(objects, ignore_conflicts=True)


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_internhoursmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="internhoursmodel",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.RunPython(seed_intern_hours, migrations.RunPython.noop),
    ]
