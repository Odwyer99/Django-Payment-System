from django.contrib import admin
from django.urls import include, path

# from django.contrib import admin
# from django.urls import path,include
# from django.conf.urls import url
# from accounts import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', include('payapp.urls')),
    path('home/', include('payapp.urls')),
    path('register/', include('payapp.urls')),
    path('login/', include('payapp.urls')),
    path('logout/', include('payapp.urls')),
    path('dashboard/', include('payapp.urls')),
    path('redirect/', include('payapp.urls')),
    path('account/', include('payapp.urls')),
    path('withdraw/', include('payapp.urls')),
    path('deposit/', include('payapp.urls')),
    path('transfer', include('payapp.urls')),
    path("stat_gen/", include('payapp.urls')),
    path("request/", include('payapp.urls')),
    path("payment-request/<int:request_id>/", include('payapp.urls')),
    path("payment_accept/<int:request_id>/", include('payapp.urls')),
    path("payment_decline/<int:request_id>/",include('payapp.urls')),
    path("payment-request/", include("payapp.urls")),
    path("conversion/<str:currency1>/<str:currency2>/<str:amount_of_currency1>/", include('payapp.urls')),
    # path("add-payment/<int:id>/", include('payapp.urls')),
    # path("accept/<int:id>/", include('payapp.urls')),
    path('admin/', admin.site.urls),

]