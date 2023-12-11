import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analytics.settings")  # Замените 'myproject' на имя вашего Django-проекта
import django
django.setup()

import random
from faker import Faker
from datetime import timedelta
from django.utils import timezone
from finance.models import Bill

fake = Faker()
coffee_names = ["Espresso", "Latte", "Cappuccino", "Americano", "Macchiato"]

# Фиксированные цены для каждого типа кофе
coffee_prices = {
    "Espresso": 400,
    "Latte": 700,
    "Cappuccino": 650,
    "Americano": 500,
    "Macchiato": 700,
}

# Генерация данных для таблицы
def generate_data():
    for day in range(1, 1001):  # 10 дней
        date = timezone.now() - timedelta(days=day)
        for _ in range(10):  # примерно 10 товаров
            position = random.choice(coffee_names)
            price = coffee_prices[position]  # Используем фиксированную цену
            quantity = random.randint(1, 5)
            sum_amount = round(price * quantity, 2)

            Bill.objects.create(
                date=date,
                position=position,
                price=price,
                quantity=quantity,
                sum=sum_amount,
            )

if __name__ == "__main__":
    generate_data()
