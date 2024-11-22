from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'payment_date')
    list_filter = ('user', 'payment_method', 'payment_date')
    search_fields = ('user__email',)
