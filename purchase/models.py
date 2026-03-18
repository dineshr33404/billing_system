from django.db import models
from decimal import Decimal
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_token = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    name = models.CharField(
        max_length=255
    )
    available_stock = models.PositiveIntegerField(
        default=0
    )
    price = models.FloatField(default=1)
    tax_percentage = models.FloatField(
        default = 0,
        help_text="Tax percentage for the product"
    )
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        #ordering = ['name']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.product_id})"

    @property
    def price_with_tax(self):
        tax_amount = (self.price * self.tax_percentage) / 100
        return self.price + tax_amount
    @property
    def get_tax_amount(self):
        tax_amount = (self.price * self.tax_percentage) / 100
        return tax_amount


class Purchase (models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length = 255)
    total_price = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class purchase_product(models.Model):
    id = models.AutoField(primary_key = True)
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        to_field='product_token', 
        on_delete=models.CASCADE,
        db_column='product_id'  # optional: makes DB column name cleaner
    )
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Denomination(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 4)
    available_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

