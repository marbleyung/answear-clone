from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.shortcuts import redirect
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", 'phone', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ('password1', 'password2',):
            if field_name == 'password1':
                self.fields[field_name].help_text = "Can't be entirely numeric, must have 8 or more symbols"
            else:
                self.fields[field_name].help_text = ''

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = None

    class Meta:
        model = CustomUser
        fields = ("email", 'phone', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            try:
                account = CustomUser.objects.exclude(pk=self.instance.pk).get(phone=phone)
            except CustomUser.DoesNotExist:
                return phone
            raise forms.ValidationError('Phone number "%s" is already in use.' % phone)

    def save(self, commit=True):
        account = super(CustomUserChangeForm, self).save(commit=False)
        account.email = self.cleaned_data['email']
        account.phone = self.cleaned_data['phone']
        account.first_name = self.cleaned_data['first_name']
        account.last_name = self.cleaned_data['last_name']
        if commit:
            account.save()
        return account


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Email or phone number')

    class Meta:
        model = CustomUser
        fields = ('username', 'password',)

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            print('line 48', username, password)
            if not authenticate(username=username, password=password):
                redirect('acc:login')
                # raise forms.ValidationError("Invalid login")
                return None