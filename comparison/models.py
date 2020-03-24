from django.contrib.auth import get_user_model
from django.db import models

class PaymentSystem(models.Model):
    name = models.CharField(max_length=200)
    delivery_speed = models.CharField(max_length=200)
    transfer_fee = models.DecimalField(max_digits=15, decimal_places=2)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
