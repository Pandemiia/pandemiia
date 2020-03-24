import django_tables2 as tables
from .models import PaymentSystem

class PaymentSystemTable(tables.Table):
    class Meta:
        model = PaymentSystem