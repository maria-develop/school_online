from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.timezone import now

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_course_update_email(email):
    """Отправляет сообщение пользователю об обновлении курса."""
    send_mail(
        "Обновление курса",
        "В Вашем курсе появилось обновление",
        EMAIL_HOST_USER,
        [email],
    )


# @shared_task
# def deactivate_inactive_users():
#     one_month_ago = now().date() - timedelta(days=30)
#     inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
#
#     email_list = []
#     for user in inactive_users:
#         email_list.append(user.email)
#     if email_list:
#         send_mail(
#             "Блокировка пользователя",
#             "Ваш аккаунт не активен последние 30 дней, поэтому заблокирован.",
#             EMAIL_HOST_USER,
#             email_list,
#         )
#         inactive_users.update(is_active=False)


@shared_task
def deactivate_inactive_users():
    # Определяем дату для проверки (30 дней назад)
    one_month_ago = now() - timedelta(days=30)

    # Находим активных пользователей, которые не заходили в течение 30 дней
    inactive_users = User.objects.filter(
        Q(last_login__lt=one_month_ago)
        | Q(last_login__isnull=True),  # учитываем пользователей с `last_login=None`
        is_active=True,
        is_notified_about_blocking=False,
    )

    # Собираем email-адреса
    email_list = list(inactive_users.values_list("email", flat=True))

    # Если есть пользователи для блокировки, отправляем email
    if email_list:
        try:
            send_mail(
                subject="Блокировка пользователя",
                message=(
                    "Ваш аккаунт не был активен последние 30 дней. "
                    "В связи с этим он был заблокирован."
                ),
                from_email=EMAIL_HOST_USER,
                recipient_list=email_list,
            )
            # Деактивируем пользователей
            inactive_users.update(is_active=False, is_notified_about_blocking=True)
        except Exception as e:
            # Обрабатываем возможные ошибки при отправке email
            print(f"Ошибка при отправке email: {e}")
