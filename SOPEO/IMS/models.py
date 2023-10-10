from django.db import models
import uuid
from django.forms import ValidationError

# Create your models here.

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iin = models.UUIDField(default=uuid.uuid1, unique=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    quantity_sold = models.BigIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        profit_earned = (self.selling_price - self.cost) * self.quantity_sold
        revenue = self.selling_price * self.quantity_sold
        # if profit_earned < 0 or revenue < 0:
        #     raise ValidationError("Profit earned or revenue cannot be negative.")

        self.profit_earned = profit_earned
        self.revenue = revenue

        super().save(*args, **kwargs)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    orderdttm = models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.quantity} {self.item.name}"
    
   

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    transactiondttm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.quantity} {self.item.name}"