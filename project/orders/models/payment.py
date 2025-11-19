from django.db import models
from orders.models.order import Order
from products.models.base import BaseModel

class Payment(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('init', 'Initialized'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    provider = models.CharField(max_length=50, default="paymob")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    paymob_order_id = models.CharField(max_length=100, null=True, blank=True)
    paymob_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_token = models.CharField(max_length=300, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} - {self.status}"
