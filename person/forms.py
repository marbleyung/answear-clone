from django import forms
from person.models import *


class PersonForm(forms.ModelForm):
    fname = forms.CharField(max_length=30, required=True)
    lname = forms.CharField(max_length=30, required=True)
    region = forms.CharField(max_length=50, required=True)
    city = forms.CharField(max_length=50, required=True)
    street = forms.CharField(max_length=50, required=True)
    house_number = forms.CharField(max_length=10, required=True)
    appartments_number = forms.CharField(max_length=10, required=False)
    zipcode = forms.CharField(max_length=10, required=True)

    class Meta:
        model = Person
        fields = ('fname', 'lname',
                  'region', 'city', "street",
                  'house_number', 'appartments_number', 'zipcode',)


class NewPersonForm(forms.Form):
    fname = forms.CharField(max_length=30, required=True)
    lname = forms.CharField(max_length=30, required=True)
    region = forms.CharField(max_length=50, required=True)
    city = forms.CharField(max_length=50, required=True)
    street = forms.CharField(max_length=50, required=True)
    house_number = forms.CharField(max_length=10, required=True)
    appartments_number = forms.CharField(max_length=10, required=False)
    zipcode = forms.CharField(max_length=10, required=True)

    class Meta:
        model = Person
        fields = ('fname', 'lname',
                  'region', 'city', "street",
                  'house_number', 'appartments_number', 'zipcode',)
