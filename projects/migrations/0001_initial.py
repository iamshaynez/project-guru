# Generated by Django 5.0.3 on 2024-03-16 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("project_number", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "budget_man_months",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("budget_amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("comment", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("name_cn", models.CharField(max_length=100)),
                ("vendor", models.CharField(max_length=100)),
                ("onboard_date", models.DateField()),
                ("rank", models.CharField(max_length=50)),
                ("hourly_rate", models.DecimalField(decimal_places=2, max_digits=10)),
                ("comment", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="WorkRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("hours", models.IntegerField()),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="projects.staff"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="workrecord",
            constraint=models.UniqueConstraint(
                fields=("staff", "date", "project"), name="unique_work_record"
            ),
        ),
    ]
