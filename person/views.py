from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect
from acc.models import *
from .models import *
from .forms import *


@login_required
def me(request):
    userdata = CustomUser.objects.get(email=request.user)
    persondata = Person.objects.filter(user=userdata)
    data = serializers.serialize("python", Person.objects.filter(user=userdata))
    print(len(list(persondata)))
    print(persondata)
    context = {'user': {},
               'persons': data,
               'editable': len(list(persondata)),
               'user_object': userdata,
               'persondata': persondata}
    if userdata.first_name and userdata.last_name:
        context['user']['name'] = f"{userdata.first_name} {userdata.last_name}"
    if userdata.phone:
        context['user']['phone'] = userdata.phone
    context['user']['email'] = userdata.email
    return render(request, 'person/profile.html', context=context)


@login_required
def edit_persondata(request, pk):
    person = Person.objects.get(pk=pk)
    context = {'person': person}
    initial = {"fname": person.fname, "lname": person.lname,
               'region': person.region, 'city': person.city, 'street': person.street,
               'house_number': person.house_number, 'appartments_number': person.appartments_number,
               'zipcode': person.zipcode}
    form = PersonForm(request.POST or None, initial=initial, instance=person)
    if form.is_valid():
        form.save()
        return redirect("person:me")
    else:
        form = PersonForm(request.POST, initial=initial, instance=person)
        context['form'] = form
    form = PersonForm(request.POST or None, initial=initial, instance=person)
    context['form'] = form
    return render(request, "person/edit_persondata.html", context=context)


@login_required
def add_persondata(request):
    if len(list(Person.objects.filter(user=request.user))) > 2:
        error = "You can't have more than 3 persons now"
        messages.error(message=error, request=request)
        return redirect('person:me')
    form = NewPersonForm(request.POST or None)
    if request.method == 'POST':
        form = NewPersonForm(data=request.POST)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            region = form.cleaned_data['region']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house_number = form.cleaned_data['house_number']
            appartments_number = form.cleaned_data['appartments_number']
            zipcode = form.cleaned_data['zipcode']
            Person.objects.create(user=request.user, fname=fname, lname=lname,
                                  region=region, city=city, street=street,
                                  house_number=house_number,
                                  appartments_number=appartments_number,
                                  zipcode=zipcode)
            return redirect('person:me')
        else:
            error = form.errors
            form = NewPersonForm()
            return render(request, 'person/edit_persondata.html', {'form': form, 'error': error})
    return render(request, "person/edit_persondata.html", {"form": form})


@login_required
def delete_persondata(request, pk):
    Person.objects.get(pk=pk).delete()
    return redirect('person:me')


@login_required
def favorite(request):
    favorite = Favorites.objects.filter(user=request.user)
    print(favorite)
    return render(request, 'person/favorite.html', {'favorite': favorite})


def cart(request):
    return render(request, 'person/cart.html')
