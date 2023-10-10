from django import forms
from .models import Inventory,Orders
from django.core.exceptions import ValidationError

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name','cost','selling_price']

    def clean(self):
        cleaned_data = super().clean()
        cost = cleaned_data.get('cost')
        selling_price = cleaned_data.get('selling_price')
        print(f"Cost Price: {cost}, Selling Price: {selling_price}")

        if selling_price <= cost:
            raise ValidationError("Selling price must be greater than the cost price.")
        if cost < 0:
            raise ValidationError("Cost cannot be negative.")


class SellItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    
    # def clean_quantity(self):
    #     quantity = self.cleaned_data['quantity']
    #     if quantity < 0:
    #         raise ValidationError("Quantity cannot be negative.")
    #     return quantity

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['quantity']

    # def clean_quantity(self):
    #     quantity = self.cleaned_data['quantity']
    #     if quantity < 0:
    #         raise ValidationError("Quantity cannot be negative.")
    #     return quantity