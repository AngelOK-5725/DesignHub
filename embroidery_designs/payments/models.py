from django.db import models

# Create your models here.
# embroidery_designs/payments/models.py

from django.db import models
from django.contrib.auth.models import User
from designs.models import Design

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='payment_purchases')
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} — {self.design} — {self.amount}'

