# Generated by Django 5.1.3 on 2024-12-10 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ims", "0004_course_update_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
