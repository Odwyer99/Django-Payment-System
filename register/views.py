from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect, HttpResponse
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from djmoney.money import Money

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, f'You have successfully registered.')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('users:dashboard')
        else:
            print("The form is not valid")
    else:
        form = SignUpForm()
    return render(request, 'webapps2023/register.html', {'form': form})

# def register_user(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.save()
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(username=user.username, password=raw_password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('users:login')
#         else:
#             messages.error(request, "Invalid Form.")
#             print("Invalid User")
#     form = SignUpForm()
#     return render(request, 'webapps2023/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            user.save()
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("users:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
                print("Invalid User")
        else:
            messages.error(request, "Invalid username or password.")
            print("Invalid User")
    form = AuthenticationForm()
    return render(request, 'webapps2023/login.html', context={"login_form": form})

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("users:login")
