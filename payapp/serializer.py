from rest_framework import serializers
from .models import Money_Transfers
from django.db import models
from djmoney.models.fields import MoneyField

CURRENCY_CHOICES = [('USD', 'US Dollar $'), ('EUR', 'Euro €'),  ('GBP', 'British Pound £')]

class Money_TransfersSerializer(serializers.ModelSerializer):
    currency1 = MoneyField(max_digits=14, decimal_places=2, null=True, currency_choices=CURRENCY_CHOICES)
    currency2 = MoneyField(max_digits=14, decimal_places=2, null=True, currency_choices=CURRENCY_CHOICES)
    rate = models.DecimalField(max_digits=14, decimal_places=2)
    class Meta:
        model = Money_Transfers