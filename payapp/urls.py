from django.urls import path
from . import views
from register import views as register_views

app_name = "users"

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", register_views.register_user, name="register"),
    path("login/", register_views.login_user, name="login"),
    path("logout", register_views.logout_user, name="logout"),
    path("dashboard/", views.display_menu, name="dashboard"),
    path("redirect/", views.get_function_chosen, name="get_function_chosen"),
    path("account/", views.account, name='account'),
    path("process_account_action/", views.get_account_action, name='get_account_action'),
    path("withdraw/", views.withdraw, name='withdraw'),
    path("deposit/", views.deposit, name='deposit'),
    path("transfer/", views.transfer, name='transfer'),
    path("request/", views.request, name='add-payment'),
    path("payment-request/<int:request_id>/", views.payment_confirm, name='payment'),
    path("payment_accept/<int:request_id>/", views.payment_accept, name='accept-payment'),
    path("payment_decline/<int:request_id>/", views.payment_decline, name='decline-payment'),
    path("conversion/<str:currency1>/<str:currency2>/<str:amount_of_currency1>/", views.conversion, name='conversion'),
    # path("notification/", views.payment_confirm, name='payments'),
    path("stat_gen/", views.stat_gen, name='stat_gen'),
    path("get_stat_gen/", views.get_transaction_action, name='get_transaction_action'),
]





