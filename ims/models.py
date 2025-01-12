from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from config import settings


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
    update_course = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        verbose_name="Обновление курса",
        help_text="Укажите обновление курса",
        related_name="course_update",
    )
    last_updated = models.DateTimeField(auto_now=True)  # дата обновления

    def was_updated_recently(self):  # проверка обновлений за последние 4 ч
        return now() - self.last_updated < timedelta(hours=4)

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


class Subscription(models.Model):
    name_subscription = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Наименование подписки",
        help_text="Укажите наименование подписки",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Владелец подписки",
        help_text="Укажите владельца подписки",
    )

    course = models.ForeignKey(
        "ims.Course",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Наименование курса",
        help_text="Выберите наименование курса",
    )

    def __str__(self):
        return self.name_subscription

    class Meta:
        verbose_name = ("Подписка",)
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
