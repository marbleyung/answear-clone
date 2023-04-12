from django.urls import path
from person.views import *

app_name = 'person'

urlpatterns = [
    path('me/', me, name='me'),
    path('edit-persondata/<int:pk>', edit_persondata, name='edit-persondata'),
    path('add-persondata/', add_persondata, name='add-persondata'),
    path('delete-persondata/<int:pk>', delete_persondata, name='delete-persondata'),
    path('favorite/', favorite, name='favorite'),
    path('cart/', cart, name='cart'),
]
