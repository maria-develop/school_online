from django.contrib.auth.models import AbstractUser
from django.db import models

from ims.models import Lesson, Course


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = ("Пользователь",)
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("Наличные", "Наличные"),
        ("Перевод на счет", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # on_delete=models.SET_NULL,  # в лекции
        verbose_name="Пользователь",
        help_text="Выберите пользователя, который совершил оплату",
    )
    # payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_date = models.DateTimeField(
        auto_now_add=True,
        # blank=True,
        # null=True,
        verbose_name="Дата оплаты",
        help_text="Дата и время совершения оплаты",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        help_text="Выберите оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        help_text="Выберите оплаченный урок",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    # amount = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     verbose_name="Сумма оплаты",
    #     help_text="Укажите сумму оплаты",
    # )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )

    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии для оплаты",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    # payment_status = models.CharField(
    #     max_length=50,
    #     verbose_name="Статус платежа",
    #     help_text="Укажите статус платежа",
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return self.amount
        # return f"Оплата от {self.user.email} на сумму {self.amount} руб. {self.payment_method}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
