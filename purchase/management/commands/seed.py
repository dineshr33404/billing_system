from django.core.management.base import BaseCommand
from purchase.models import Product, Denomination
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        for num in range(10):
            Product.objects.create(
                name=fake.word(),
                product_token = str(num),
                available_stock = 100,
                price=random.randint(10, 1000),
                tax_percentage = random.randint(0, 10),
            )
        denominationList = [500, 100, 50, 20, 10, 5, 2, 1]
        for amount in denominationList:
            Denomination.objects.create(
                name = str(amount),
                available_quantity = 100
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
