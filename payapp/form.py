from django.forms import ModelForm,forms
from .models import Money_Transfers, Deposits, Withdraws, PaymentRequest



class TransferForm(ModelForm):
    class Meta:
        model = Money_Transfers
        fields = '__all__'

class DepositForm(ModelForm):
    class Meta:
        model = Deposits
        fields = '__all__'

class WithdrawForm(ModelForm):
    class Meta:
        model = Withdraws
        fields = '__all__'

class PaymentRequestForm(ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ('receiver', 'reason', 'Amount')
