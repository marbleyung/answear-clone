from django.contrib import admin
from .forms import *


class PersonAdmin(admin.ModelAdmin):
    add_form = PersonForm
    model = Person
    list_display = ("fname", 'lname', 'region', 'city', "street", "house_number", 'zipcode')
    list_filter = ("fname", 'lname', "region", 'city', 'zipcode')
    search_fields = ("fname", 'lname', "region", 'city', 'zipcode')
    ordering = ("lname", 'city',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Favorites)
