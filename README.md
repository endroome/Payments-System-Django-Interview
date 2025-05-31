# 💳 Payments System — Django Interview

Тестовое задание для Backend Django Developer.

## 📌 Задача

Реализовать сервис, который:

- Принимает webhook от банка (`POST /api/webhook/bank/`)
- Обрабатывает транзакцию:
  - Защита от дублей по `operation_id`
  - Начисление суммы на баланс организации по `payer_inn`
  - Логирование изменения баланса
- Отдаёт текущий баланс по ИНН (`GET /api/organizations/<inn>/balance/`)

## 🛠️ Стек

- Python 3.9  
- Django 4.2.17  
- MySQL

## 📤 Пример запроса (POST /api/webhook/bank/)

```json
{
  "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
  "amount": 145000,
  "payer_inn": "1234567890",
  "document_number": "PAY-328",
  "document_date": "2024-04-27T21:00:00Z"
}
```
## 📥 Пример ответа (GET /api/organizations/1234567890/balance/)
```json
{
  "inn": "1234567890",
  "balance": 145000
}
```