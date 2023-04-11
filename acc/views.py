from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from acc.forms import *
from person.models import *


def register_request(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Person.objects.create(user=user, fname=user.first_name, lname=user.last_name)
            login(request, user, backend='acc.backends.EmailBackend')
            return redirect("shop:home")
        else:
            error = form.errors
            form = CustomUserCreationForm()
            return render(request, 'acc/register.html', {'register_form': form, 'error': error})
    return render(request, "acc/register.html", {"register_form": form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = AccountAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password) #or authenticate(phone=email, password=password)
            if user:
                login(request, user, backend='acc.backends.EmailBackend')
                return redirect("shop:home")
            else:
                error = 'Username/password is incorrect'
                return render(request, "acc/login.html", {"login_form": form, 'error': error})
        else:
            error = form.errors
    form = AccountAuthenticationForm()
    error = None
    return render(request, "acc/login.html", {"login_form": form, 'error': error})


def logout_request(request):
    logout(request)
    return redirect("shop:home")


@login_required
def edit_userdata(request):
    user = CustomUser.objects.get(email=request.user)
    context = {}
    initial = {"id": user.pk, "email": user.email, "phone": user.phone,
               "first_name": user.first_name, "last_name": user.last_name,}
    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user, initial=initial)
        if form.is_valid():
            form.save()
            return redirect("person:me")
        else:
            form = CustomUserChangeForm(request.POST, instance=request.user,
                                     initial=initial)
            context['form'] = form
    form = CustomUserChangeForm(request.POST or None, initial=initial)
    context['form'] = form
    return render(request, "person/edit_userdata.html", context)
