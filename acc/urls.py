from django.urls import path
from .views import *
app_name = 'acc'

urlpatterns = [
    path('register/', register_request, name='register'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('edit-userdata/', edit_userdata, name='edit-userdata'),
]
