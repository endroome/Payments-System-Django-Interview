import json
from uuid import UUID
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import Payment, Organization, BalanceLog


@method_decorator(csrf_exempt, name="dispatch")
class BankWebhookView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))

            operation_id = UUID(data["operation_id"])
            amount = int(data["amount"])
            payer_inn = data["payer_inn"]
            document_number = data["document_number"]
            document_date = datetime.fromisoformat(
                data["document_date"].replace("Z", "+00:00")
            )

        except (KeyError, ValueError, TypeError) as e:
            return JsonResponse({"error": f"Invalid input: {e}"}, status=400)

        if Payment.objects.filter(operation_id=operation_id).exists():
            return HttpResponse(status=200, content="Already processed")

        try:
            with transaction.atomic():
                Payment.objects.create(
                    operation_id=operation_id,
                    amount=amount,
                    payer_inn=payer_inn,
                    document_number=document_number,
                    document_date=document_date,
                )

                org, _ = Organization.objects.get_or_create(inn=payer_inn)
                org.balance += amount
                org.save()

                BalanceLog.objects.create(
                    organization=org,
                    change_amount=amount,
                    description=f"Пополнение по документу {document_number}",
                )
        except Exception as e:
            return JsonResponse({"error": f"Database error: {e}"}, status=500)

        return HttpResponse(status=200, content="Success")


class BalanceView(View):
    def get(self, request, inn):
        try:
            org = Organization.objects.get(inn=inn)
            return JsonResponse({"inn": inn, "balance": org.balance})
        except Organization.DoesNotExist:
            return JsonResponse({"inn": inn, "balance": 0})
