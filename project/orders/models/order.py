from django.db import models
from accounts.models.user import User
from products.models.product import Product

from products.models.base import BaseModel


class Order(BaseModel):

    STATUS_CHOICES = (
        ('pending','pending'),
        ('processing','processing'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('cancelled','cancelled')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"

class OrderItem(BaseModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price and self.quantity:
            self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

