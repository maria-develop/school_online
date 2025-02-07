# Generated by Django 5.1.3 on 2024-12-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_payment_link_payment_session_id_alter_payment_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_notified_about_blocking",
            field=models.BooleanField(
                default=False,
                help_text="Флаг для предотвращения повторной отправки уведомления",
                verbose_name="Уведомлен о блокировке",
            ),
        ),
    ]
