from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from acc.forms import AccountAuthenticationForm


# Create your views here.
def login_checkout(request):
    referer = request.META.get("HTTP_REFERER")
    if request.user.is_authenticated:
        return redirect("person:cart")
    if request.method == "POST":
        form = AccountAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user, backend='acc.backends.EmailBackend')
                return HttpResponseRedirect(referer)
            else:
                error = 'Username/password is incorrect'
                return render(request, "checkout/login.html", {"login_form": form, 'error': error})
        else:
            error = form.errors
    form = AccountAuthenticationForm()
    error = None
    return render(request, "checkout/login.html", {"login_form": form, 'error': error})


def checkout_main(request):
    pass
