from .models import User_Account, Account_Data, Transactions
import random
from datetime import date , datetime
from djmoney.money import Money
from register.models import User
from register.forms import SignUpForm

CURRENCY_CHOICES = [('USD', 'US Dollar $'), ('EUR', 'Euro €'),  ('GBP', 'British Pound £')]

cur_customer = User
def randomGen():
    # return a 10 digit random number as users account number
    return int(random.uniform(1000000000, 9999999999))

def accounttype():
    return Money(0, 'GBP')

# def accounttype(request):
#     accounts = cur_customer
#     form = SignUpForm()
#     if form.is_valid():
#         form.save()
#         Balance = request.POST.get("Balance")
#         if User.objects.filter(Balance=request.Balance).exists():
#             Balance = User.objects.get(Balance=request.Balance).Balance
#     else:
#         return Money(0, 'GBP')

class Account:
    def __init__(self, account_details):

        #Existing account
        self.account_no = account_details.Accno
        print("self.account_no:", self.account_no)
        self.account_details = account_details
        print("self.account_details:", self.account_details)
        self.transac = {}

        transaction_list = Transactions.objects.filter(Accno=account_details)
        print("trans list: ", transaction_list)
        for trans in transaction_list:
            self.transac[trans.Trans_ID] = Transaction(trans)

    def create_transaction(self, amt, type ):
        new_trans = New_Transaction(self, date.today(), datetime.now(), amt, type)


    def get_transaction_log(self):
        for tr in self.transac:
            self.transac[tr].display()
        return self.transac


class New_Account(Account):
    def __init__(self, customer_obj):
        new_acc = Account_Data()
        new_acc.Accno = randomGen()
        new_acc.Balance = accounttype()
        new_acc.Owner = customer_obj.customer_data
        new_acc.save()
        super().__init__(new_acc)  #Call to base class constrcutor

class Login_Details:
    def __init__(self, user, passwd):
        self.Name = user
        self.password = passwd

#For existing customer
class Customer:
    def __init__(self, log_in_obj):
        #self.customer_data = Customer_Data.objects.get(Name = log_in_obj.username)
        self.customer_data = User_Account.objects.get(Name= log_in_obj.Name)
        self.login_credentials = log_in_obj
        self.accounts = {}
        account_data_list = Account_Data.objects.filter(Owner=self.customer_data)
        print(account_data_list)
        for account_data in account_data_list:
            self.accounts[account_data.Accno] = Account(account_data)

    def create_account(self):
        new_account = New_Account(self)
        self.accounts[new_account.account_no] = new_account

    def close_account(self, accno):
        del_account = self.accounts[accno]
        del_account.account_details.delete()
        del self.accounts[accno]
    #
    def create_notification(self, receiver, reason, amount, is_active):
        new_not = New_Notification(self,  receiver, reason, amount, is_active)

        # def get_notification_log(self):
        #     for tr in self.transac:
        #         self.transac[tr].display()
        # return self.transac

class New_Customer(Customer):
    def __init__(self, log_in_obj, name):
        #Insert details to DB
        cust_user=User_Account()
        cust_user.Name = name
        cust_user.save()
        super().__init__(log_in_obj)
        #self.accounts = {}

class Notification:
    def __int__(self, Not_data):
        #Read existing Notification from DB
        self.Not_id=Not_data.Not_ID
        self.Not_details=Not_data

class New_Notification(Notification):
    def __init__(self, customer_obj, sender, receiver, amount, reason, is_active):
        Not_details=Notification()
        Not_details.Sender=sender
        Not_details.Receiver=receiver
        Not_details.Amount=amount
        Not_details.reason=reason
        Not_details.is_active=is_active
        Not_details.Name=customer_obj.customer_data
        Not_details.save()
        super().__init__(Not_details)


class Transaction:
    def __init__(self, trans_data):
        #Read existing transaction details from DB
        self.trans_id=trans_data.Trans_ID
        self.trans_details=trans_data
    def display(self):
        print("self.trans_id: ",self.trans_id)
        print("self.trans_details: ",self.trans_details.Type)


class New_Transaction(Transaction):
    def __init__(self, account_obj, date, time, amount, tran_type):
        #trans_id will be got by auto-increment
        trans_details=Transactions()
        trans_details.Amount=amount
        trans_details.Type=tran_type
        trans_details.Date= date
        trans_details.Time= time
        trans_details.Accno=account_obj.account_details
        trans_details.save()
        super().__init__(trans_details)
