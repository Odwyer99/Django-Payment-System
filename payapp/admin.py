from django.contrib import admin
from .models import  Transactions, User_Account, Account_Data, PaymentRequest

class AccountAdmin(admin.ModelAdmin):
    list_filter = ['Accno','Balance']
    list_display = ['Accno', 'Balance']
    search_fields = ['Owner']
class Meta:
    model = Account_Data
    admin.site.register(Account_Data, AccountAdmin)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ['Trans_ID', 'Accno', 'Type']
    list_display = ['Trans_ID', 'Accno', 'Type']
    search_fields = ['Type']
class Meta:
    model = Transactions
admin.site.register(Transactions, TransactionAdmin)

class UserAdmin(admin.ModelAdmin):
    list_filter = ['Cust_ID', 'Name', 'email']
    list_display = ['Cust_ID', 'Name' ]
    search_fields = ['Name', ],
    readonly_fields = ['Name', ]
class Meta:
    model = User_Account
admin.site.register(User_Account, UserAdmin)

# class PaymentListAdmin(admin.ModelAdmin):
#     list_filter = ['user']
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user']
#
#     class Meta:
#         model = Paymentlist
# admin.site.register(Paymentlist, PaymentListAdmin)


class PaymentRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver', 'reason']
    list_display = ['sender', 'receiver', 'reason']
    search_fields = ['sender__username', 'receiver__username']
    class Meta:
        model = PaymentRequest
admin.site.register(PaymentRequest, PaymentRequestAdmin)