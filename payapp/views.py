from django.shortcuts import render, redirect
from .models import User_Account, Account_Data, Transactions, Money_Transfers, PaymentRequest,Notification
from payapp import Classes
from django.db import transaction
from .form import TransferForm, DepositForm, WithdrawForm, PaymentRequestForm
from register.forms import User
from django.contrib import messages
from django.db import connection
from djmoney.money import Money
from djmoney.contrib.exchange.models import convert_money
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .serializer import Money_TransfersSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

CURRENCY_CHOICES = [('USD', 'US Dollar $'), ('EUR', 'Euro €'),  ('GBP', 'British Pound £')]

def conversion(request):
    Money_TransfersSerializer
    if request.method == 'GET':
        currency1 = request.GET.get('USD')
        currency2 = request.GET.get('GBP')
        amount = request.GET.get('amount')
        conversion = Money_Transfers.objects.get(sender=currency1, receiver=currency2)
        converted_amount = Money(amount, currency1) * conversion.Amount
        return JsonResponse({'converted_amount': converted_amount.amount})


# def conversion(request, currency1, currency2, amount_of_currency1):
#     #converting currency1 to currency2
#     if request.method == 'POST':
#         currency = Money_TransfersSerializer()
#         if currency.is_valid():
#             currency1 = currency.serializer_choice_field.choices("sender")
#             currency2 = currency.serializer_choice_field.choices('receiver')
#             amount_of_currency1 = Money_Transfers.objects.get("Amount")
#     try:
#         convert_money(Money(amount_of_currency1, currency1), currency2)
#     except ValueError:
#         # invalid amount_of_currency1 value
#         return JsonResponse({'error': 'Invalid amount'}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)
#
# def conversion(request, currency1, currency2, amount_of_currency1):
#     #converting currency1 to currency2
#     if request.method == 'POST':
#         currency = Money_TransfersSerializer(request.POST)
#         if currency.is_valid():
#             currency1 = request.POST.get('GBP')
#             currency2 = request.POST.get('USD')
#             amount_of_currency1 = 1000
#             converted_amount = convert_money(amount_of_currency1, currency1, currency2)
#             return HttpResponse(converted_amount)
#         else:
#             return JsonResponse({'error': 'Invalid amount'}, status=400)
# class CurrencyExchangeService:
#     def get_rates_from_api(self, BASE_CURRENCY,  currency):
#         return self.get_rates_from_api(BASE_CURRENCY)[get_rate, currency]

def home(request):
    return render(request, "webapps2023/home.html")


cur_customer = None #Stores customer obj

payment_request = None

def display_menu(request):
    global cur_customer
    user_log_in = Classes.Login_Details(request.user.username, request.user.password)
    cust_details = User_Account.objects.filter(Name=user_log_in.Name)
    print("cust_details", cust_details)
    if(cust_details):
        print("Existing Customer")
        customer = Classes.Customer(user_log_in)
        print("customer obj", customer)
    else:
        print("Creating New Customer")
        customer = Classes.New_Customer(user_log_in, user_log_in.Name)
    print("Customer name:", customer.customer_data.Name)
    cur_customer = customer
    total = Transactions.objects.filter(Trans_ID=request.user.id).count()
    return render(request, 'webapps2023/user_account.html', {'customer': customer, 'total':total})

def account(request):
    accounts = cur_customer.accounts
    user_accnos = list(accounts.keys())
    print("user_accnos", user_accnos)
    return render(request, 'webapps2023/account.html', {'customer': cur_customer, 'accounts': accounts, 'can_close_accnos': user_accnos })

def withdraw(request):
    accounts = cur_customer.accounts
    msg ="<br>Enter a valid account no. and also check for ur balance!</p><br>"
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            acc_num = form.cleaned_data.get('Accno')
            amount = form.cleaned_data.get('Amount')
            print('requestPOST=', acc_num, type(acc_num))
            if acc_num in accounts:
                acc_q= Account_Data.objects.get(Accno=acc_num)
                balance=acc_q.Balance
                print("balance:", balance)
                if(balance>=amount):
                    trans = Classes.Account(acc_q)
                    trans.create_transaction(amount, "withdraw")
                    balance -= amount
                    acc_q.Balance = balance
                    print("balance:", acc_q.Balance)
                    acc_q.save()
                    cur_customer.accounts[acc_num].account_details.Balance -= amount
                    msg="<td>Withdraw Successful! Check your account balance</td><br>"
        else:
            msg = "<td>Insufficient funds!</td><br>"
    form = WithdrawForm()
    return render(request, 'webapps2023/withdraw.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'form': form})

def deposit(request):
    accounts = cur_customer.accounts
    msg = "<br>Enter a valid account no. and also check for your balance!</p><br>"
    form = DepositForm(request.POST)
    if form.is_valid():
        acc_num = form.cleaned_data.get('Accno')
        amount = form.cleaned_data.get('Amount')
        print('requestPOST=', acc_num,type(acc_num))
        if acc_num in accounts:
            acc_q=Account_Data.objects.get(Accno=acc_num)
            balance = acc_q.Balance
            print("balance:", balance)
            trans=Classes.Account(acc_q)
            trans.create_transaction(amount, "deposit")
            balance += amount
            acc_q.Balance=balance
            print("balance:", acc_q.Balance)
            acc_q.save()
            cur_customer.accounts[acc_num].account_details.Balance += amount
            msg="<td>Deposit Successful! Check your account balance</td><br>"
        else:
            msg = "<p>Invalid account number</p><br>"
    form = DepositForm()
    return render(request, 'webapps2023/deposit.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'form': form})

def transfer(request):
    with transaction.atomic():
        accounts = cur_customer.accounts
        msg = "<br>Enter a valid account number for both Sender and Receiver, and also check for your balance!</p><br>"
        if request.method == 'POST':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender = form.cleaned_data.get('sender')
                receiver = form.cleaned_data.get('receiver')
                amount = form.cleaned_data.get('Amount')
                if sender in accounts:
                    acc_q = Account_Data.objects.get(Accno=sender)
                    sender_balance = acc_q.Balance
                    if sender_balance >= amount:
                        sender_new_balance = sender_balance - amount
                        acc_q.Balance=sender_new_balance
                        acc_q.save()
                        trans = Classes.Account(acc_q)
                        trans.create_transaction(amount, "transfer-debit")
                        acc_q=Account_Data.objects.get(Accno=receiver)
                        receiver_balance = acc_q.Balance
                        receiver_new_balance = receiver_balance + amount
                        acc_q.Balance=receiver_new_balance
                        acc_q.save()
                        trans = Classes.Account(acc_q)
                        trans.create_transaction(amount, "transfer-credit")
                    msg = "<td>Transfer Successful!</td><br>"
            else:
                msg = "<p>Invalid account number</p><br>"
        else:
            form = TransferForm()
        return render(request, 'webapps2023/transfer.html', {'customer': cur_customer, 'form': form, 'msg': msg})


@csrf_exempt
def request(request):
    with transaction.atomic():
        msg ="Receiver name must be a valid username."
    payment_request = None
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data.get('receiver')
            reason = form.cleaned_data.get('reason')
            amount = form.cleaned_data.get('Amount')
            sender = request.user
            receiver1 = User.objects.get(username=receiver)
            if payment_request is not None:
                payment_request = PaymentRequest.objects.get(sender=sender, receiver=receiver1, Amount=amount, reason= reason )
                payment_request.sender = str(sender)
                payment_request.receiver = str(receiver1)
                payment_request.save()
            else:
                payment_request = PaymentRequest.objects.create(sender=sender, receiver=receiver1, Amount=amount, reason=reason)
                payment_request.sender = str(sender)
                payment_request.receiver = str(receiver1)
                payment_request.save()
                # return redirect('users:payment', request_id=payment_request.id)
            msg = "<td>Payment request sent<br>"
        else:
            return HttpResponse('Invalid Request')
    else:
        form = PaymentRequestForm
    return render(request, 'webapps2023/paymentrequest.html', {'msg': msg, 'form': form})

# def request(request):
#     accounts = cur_customer.accounts
#     msg =""
#     payment_request = None
#     if request.method == 'POST':
#         form = PaymentRequestForm(request.POST)
#         if form.is_valid():
#             sender = form.cleaned_data.get('sender')
#             receiver = form.cleaned_data.get('receiver')
#             reason = form.cleaned_data.get('reason')
#             amount = form.cleaned_data.get('Amount')
#             if sender in accounts:
#                 sender1 = User_Account.objects.get(Name=sender)
#                 if receiver in accounts:
#                     recipient = User_Account.objects.get(Name=receiver)
#                     if payment_request is not None:
#                         payment_request = PaymentRequest.objects.get(sender=sender1, receiver=recipient, Amount=amount, reason= reason )
#                         payment_request.save()
#                     else:
#                         payment_request = PaymentRequest.objects.create(sender=sender1,  receiver=recipient, Amount=amount, reason=reason)
#                         payment_request.save()
#                         msg = "<td>Payment request sent<br>"
#                         return redirect('users:payment', request_id=payment_request.id)
#                 else:
#                     return HttpResponse('Invalid Receiver')
#             else:
#                 return HttpResponse('Invalid Sender')
#     else:
#         form = PaymentRequestForm
#     return render(request, 'webapps2023/paymentrequest.html', {'msg': msg, 'form': form})
def payment_confirm(request, request_id):
    payment_request = PaymentRequest.objects.get(id=request_id)
    return render(request, 'webapps2023/requeststatus.html', {'payment_request': payment_request})

def payment_request_detail(request, request_id):
    payment_request = PaymentRequest.objects.get(id=request_id)
    if payment_request.receiver == request.user:
        if request.method == 'POST':
            payment_request.status = request.POST.get('status')
            payment_request.save()
            messages.success(request, 'Payment request updated.')
            return redirect('users:dashboard')
        else:
            return render(request, 'webapps2023/paymentrequest.html', {'payment_request': payment_request})
    else:
        return redirect('users:dashboard')

def payment_accept(request, request_id):
    try:
        payment_request = PaymentRequest.objects.get(id=request_id)
        if payment_request.status == 'pending':
            # Code to process the payment goes here
            payment_request.status = 'accepted'
            payment_request.save()
            return redirect('users:payment', request_id=payment_request.id)
    except PaymentRequest.DoesNotExist:
        pass
    return HttpResponseBadRequest('Invalid Request')

def payment_decline(request, request_id):
    try:
        payment_request = PaymentRequest.objects.get(id=request_id)
        if payment_request.status == 'pending':
            payment_request.status = 'declined'
            payment_request.save()
            return redirect('users:payment', request_id=payment_request.id)
    except PaymentRequest.DoesNotExist:
        pass
    return HttpResponseBadRequest('Invalid Request')

def notification(request, request_id, payment_accept):
    recipient = User.objects.get(pk=request_id)
    sender = request.user
    message = f"You have a new notification from {sender.username}."
    notification = Notification(sender=sender, receiver=recipient, message=message)
    notification.save()
    return redirect('users:dashboard')

def view_notifications(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'webapps2023/notifications.html', {'notifications': notifications})

def stat_gen(request):
    accounts = cur_customer.accounts
    print(accounts)
    msg = ""
    all_transactions = {}
    for acc in accounts:
        print("acc_no:", acc)
        acc_q = Account_Data.objects.get(Accno=int(acc))
        trans = Classes.Account(acc_q)
        transaction = trans.get_transaction_log()
        trans_objs_list = list(transaction.values())
        all_transactions[acc] = all_transactions.get(acc, [])+trans_objs_list
        print("trans:", transaction)
    return render(request, 'webapps2023/stat_gen.html', {'customer': cur_customer, 'accounts': accounts, 'transaction': all_transactions,'msg': msg})

def get_transaction_action(request):
    accounts = cur_customer.accounts
    print("got:", request.GET)
    msg = "filter"
    button_action = request.GET['account_action']
    all_transactions = {}
    if(button_action == 'withdraw'):
        for acc in accounts:
            transaction=Transactions.objects.filter(Accno_id=int(acc), Type="withdraw")
            print("withdraw:", transaction)
            all_transactions[acc] = list(transaction)
    elif(button_action == 'deposit'):
        for acc in accounts:
            transaction=Transactions.objects.filter(Accno_id=int(acc),Type="deposit")
            all_transactions[acc] = list(transaction)
    elif(button_action == 'all'):
        return redirect('users:stat_gen')
    print("all_trans:", all_transactions)
    return render(request, 'webapps2023/stat_gen.html', {'customer': cur_customer, 'accounts': accounts, 'transaction': all_transactions,'msg': msg})

def get_function_chosen(request):
    print(request.GET)
    menu_chosen = request.GET['function_chosen']
    if( menu_chosen == 'account'):
        return redirect('users:account')
    elif(menu_chosen=='withdraw'):
        return redirect('users:withdraw')
    elif(menu_chosen=='deposit'):
        return redirect('users:deposit')
    elif(menu_chosen=='stat_gen'):
        return redirect('users:stat_gen')
    elif(menu_chosen=='transfer'):
        return redirect('users:transfer')
    elif(menu_chosen=='request'):
        return redirect('users:add-payment')

def get_account_action(request):
    print("got:", request.GET)
    account_action = request.GET['account_action']
    if(account_action == 'create'):
        cur_customer.create_account()
        request.session['create'] = True
    elif(account_action == 'close'):
        print(request.GET)
        print("account:", cur_customer.accounts)
        close_accno = int(request.GET['close_accno'])
        cur_customer.close_account(close_accno)
    else:
        print("Got neither create nor close")
    return redirect('users:account')

