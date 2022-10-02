# Generated by Django 4.1 on 2022-10-02 18:01

import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quizzes", "0003_alter_quiz_participants"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="attempts", to="quizzes.quiz"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attempts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Attempt",
                "verbose_name_plural": "Attempts",
            },
        ),
    ]
