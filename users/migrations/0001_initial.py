# Generated by Django 4.2.1 on 2023-10-10 00:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "user_id",
                    models.CharField(max_length=32, unique=True, verbose_name="Телеграм ID"),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        verbose_name="Телеграм Username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=256, null=True, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=256, null=True, verbose_name="Фамилия"),
                ),
                (
                    "language_code",
                    models.CharField(
                        blank=True,
                        default="ru",
                        max_length=8,
                        null=True,
                        verbose_name="Язык",
                    ),
                ),
                (
                    "deep_link",
                    models.CharField(blank=True, max_length=64, null=True, verbose_name="Deep Link"),
                ),
                (
                    "is_blocked_bot",
                    models.BooleanField(default=False, verbose_name="Заблокировал бота?"),
                ),
                ("is_admin", models.BooleanField(default=False, verbose_name="Админ?")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен?"),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
