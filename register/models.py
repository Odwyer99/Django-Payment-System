from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser,User
from djmoney.models.fields import MoneyField


CURRENCY_CHOICES = [('USD', 'US Dollar $'), ('EUR', 'Euro €'),  ('GBP', 'British Pound £')]
CURRENCY_1 = [('USD', 'US Dollar $')]
CURRENCY_2 = [('EUR', 'Euro €')]
CURRENCY_3 = [('GBP', 'British Pound £')]

class User(AbstractUser):
    Balance = models.CharField("Account_Type", null=True, max_length=20, choices=CURRENCY_CHOICES)
    #  Balance = MoneyField("Account_Type",  max_digits=14, decimal_places=2, null=True, blank=True, currency_choices=CURRENCY_CHOICES)
