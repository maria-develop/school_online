# Generated by Django 5.1.3 on 2024-11-22 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ims", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "payment_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Дата и время совершения оплаты",
                        verbose_name="Дата оплаты",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Укажите сумму оплаты",
                        max_digits=10,
                        verbose_name="Сумма оплаты",
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("Наличные", "Наличные"),
                            ("Перевод на счет", "Перевод на счет"),
                        ],
                        help_text="Выберите способ оплаты",
                        max_length=50,
                        verbose_name="Способ оплаты",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        help_text="Выберите оплаченный курс",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="ims.course",
                        verbose_name="Оплаченный курс",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        blank=True,
                        help_text="Выберите оплаченный урок",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="ims.lesson",
                        verbose_name="Оплаченный урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Выберите пользователя, который совершил оплату",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
