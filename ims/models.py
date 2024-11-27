from django.db import models

import users
from config import settings


# from users.models import User


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Наименование курса",
        help_text="Укажите наименование курса",
    )
    preview = models.ImageField(
        upload_to="ims/preview",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец курса",
        help_text="Укажите владельца курса",
    )

    def __str__(self):
        return self.name or "Без названия"

    class Meta:
        verbose_name = ("Курс",)
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name_lesson = models.CharField(
        max_length=100,
        # blank=True,
        # null=True,
        verbose_name="Наименование урока",
        help_text="Укажите наименование урока",
    )
    preview_lesson = models.ImageField(
        upload_to="ims/preview",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    description_lesson = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Наименование курса",
        help_text="Выберите наименование курса",
    )
    video_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец урока",
        help_text="Укажите владельца урока",
    )

    def __str__(self):
        return self.name_lesson

    class Meta:
        verbose_name = ("Урок",)
        verbose_name_plural = "Уроки"
