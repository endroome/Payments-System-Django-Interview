from django.db import models

class Organization(models.Model):
    inn = models.CharField(max_length=12, unique=True)
    balance = models.BigIntegerField(default=0)

class Payment(models.Model):
    operation_id = models.UUIDField(primary_key=True)
    amount = models.BigIntegerField()
    payer_inn = models.CharField(max_length=12)
    document_number = models.CharField(max_length=64)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class BalanceLog(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    change_amount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
