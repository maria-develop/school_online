from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    list_filter = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "payment_method", "payment_date")
    list_filter = ("user", "payment_method", "payment_date")
    search_fields = ("user__email",)
