from django.contrib import admin

from .models import Organization, Payment, BalanceLog

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("inn", "balance")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("operation_id", "payer_inn", "amount", "document_number", "document_date")

@admin.register(BalanceLog)
class BalanceLogAdmin(admin.ModelAdmin):
    list_display = ("organization", "change_amount", "description", "timestamp")