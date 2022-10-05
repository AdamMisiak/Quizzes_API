# Generated by Django 4.1 on 2022-10-05 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quizzes", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=255, null=True, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=255, null=True, verbose_name="last name")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.CreateModel(
            name="QuizInvitation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[(1, "sent"), (2, "accepted"), (3, "rejected")],
                        null=True,
                        verbose_name="status",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "invited",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="invited", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="invites", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="invites", to="quizzes.quiz"
                    ),
                ),
            ],
            options={
                "verbose_name": "Quiz Invitation",
                "verbose_name_plural": "Quiz Invitations",
            },
        ),
    ]
