from django.conf import settings
from djmoney.models.fields import MoneyField
from django.db import models
from register.models import User


CURRENCY_CHOICES = [('USD', 'US Dollar $'), ('EUR', 'Euro €'),  ('GBP', 'British Pound £')]
CURRENCY_1 = [('USD', 'US Dollar $')]
CURRENCY_2 = [('EUR', 'Euro €')]
CURRENCY_3 = [('GBP', 'British Pound £')]




class User_Account(models.Model):
    Cust_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    email = models.EmailField()
    class Meta:
        db_table = 'customer'

class Account_Data(models.Model):
    Accno = models.IntegerField(primary_key=True)
    Owner = models.ForeignKey(User_Account, on_delete=models.CASCADE)
    Balance = MoneyField(max_digits=14, decimal_places=2, null=True, currency_choices=CURRENCY_CHOICES)
    # Account = models.CharField('Account_Type', max_length=50,  choices=CURRENCY_CHOICES)
    class Meta:
        db_table = 'account'


class Deposits(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.IntegerField()
    Amount = MoneyField(max_digits=14, null=True, decimal_places=2)
    class Meta:
        db_table = 'deposits'

class Withdraws(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.IntegerField()
    Amount = MoneyField(max_digits=14, null=True, decimal_places=2)
    class Meta:
        db_table = 'withdraws'

class Transactions(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE)
    Amount = MoneyField(max_digits=14, null=True, default_currency='USD', choices=CURRENCY_CHOICES)
    Type = models.CharField(max_length=30)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField()
    class Meta:
        db_table = 'transactions'

class Notification(models.Model):
    Not_ID = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    reason = models.TextField()
    Amount = models.FloatField()
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateField(auto_now_add=True)

    # def accept(self):
    #     receiver_payment_request = User_Account.objects.get(Name=self.receiver)
    #     sender_payment_request = User_Account.objects.get(Name=self.sender)
    #     self.is_active = True
    #     self.save()
    #
    # def decline(self):
    #     self.is_active = False
    #     self.save()
    #
    # def cancel(self):
    #     self.is_active = False
    #     self.save()
    class Meta:
        db_table = 'Notification'

class Money_Transfers(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    sender = models.IntegerField()
    receiver = models.IntegerField()
    Amount = MoneyField(max_digits=14, null=True, decimal_places=2)
    class Meta:
        db_table = 'transfers'

class conversion(models.Model):
    currency1 = MoneyField(max_digits=14, decimal_places=2, null=True, currency_choices=CURRENCY_CHOICES)
    currency2 = MoneyField(max_digits=14, decimal_places=2, null=True, currency_choices=CURRENCY_CHOICES)
    rate = models.DecimalField(max_digits=14, decimal_places=2)


class PaymentRequest(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    reason = models.CharField(max_length=255)
    Amount = MoneyField(max_digits=14, null=True, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_request = models.ForeignKey(PaymentRequest, on_delete=models.CASCADE)
    Amount = MoneyField(max_digits=14, null=True, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



