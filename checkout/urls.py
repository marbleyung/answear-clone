from django.urls import path
from checkout.views import *

app_name = 'checkout'

urlpatterns = [
    path('login', login_checkout, name='login'),
    path('main', checkout_main, name='main'),
]
