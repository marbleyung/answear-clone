from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from person.models import Favorites
from .models import *


def home(request):
    return redirect('shop:gender', gender_slug='male')


class SearchResultView(ListView):
    model = Item
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(Q(name__icontains=query) | Q(item_brand__brand__icontains=query))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        d = {item.item_gender: {} for item in object_list}
        context['d'] = d
        object_list = self.get_queryset()
        for item in object_list:
            d[item.item_gender][item.item_type] = list()
        print('views33')
        for item in object_list:
            if item.item_category not in d[item.item_gender][item.item_type]:
                d[item.item_gender][item.item_type].append(item.item_category)
        return context


class SearchGenderView(ListView):
    model = Item
    template_name = 'search_nested.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(item_gender__slug=self.kwargs['gender_slug']).\
            filter(Q(name__icontains=query) | Q(item_brand__brand__icontains=query))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchGenderView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['gender_slug'] = self.kwargs['gender_slug']
        object_list = Item.objects.filter(Q(name__icontains=query) |
                                          Q(item_brand__brand__icontains=query))
        d = {item.item_gender: {} for item in object_list}
        context['d'] = d
        for item in object_list:
            d[item.item_gender][item.item_type] = list()

        for item in object_list:
            if item.item_category not in d[item.item_gender][item.item_type]:
                d[item.item_gender][item.item_type].append(item.item_category)
        return context


class SearchTypeView(ListView):
    model = Item
    template_name = 'search_nested.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(item_gender__slug=self.kwargs['gender_slug']).\
            filter(item_type__slug=self.kwargs['type_slug'])\
            .filter(Q(name__icontains=query) | Q(item_brand__brand__icontains=query))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchTypeView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['gender_slug'] = self.kwargs['gender_slug']
        context['type_slug'] = self.kwargs['type_slug']
        object_list = Item.objects.filter(Q(name__icontains=query) |
                                          Q(item_brand__brand__icontains=query))
        d = {item.item_gender: {} for item in object_list}
        context['d'] = d
        for item in object_list:
            d[item.item_gender][item.item_type] = list()

        for item in object_list:
            if item.item_category not in d[item.item_gender][item.item_type]:
                d[item.item_gender][item.item_type].append(item.item_category)
        return context


class SearchCategoryView(ListView):
    model = Item
    template_name = 'search_nested.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(item_gender__slug=self.kwargs['gender_slug']).\
            filter(item_type__slug=self.kwargs['type_slug']).filter\
            (item_category__slug=self.kwargs['category_slug']).filter(Q(name__icontains=query)
            | Q(item_brand__brand__icontains=query))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchCategoryView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['gender_slug'] = self.kwargs['gender_slug']
        context['type_slug'] = self.kwargs['type_slug']
        context['category_slug'] = self.kwargs['category_slug']
        object_list = Item.objects.filter(Q(name__icontains=query) |
                                          Q(item_brand__brand__icontains=query))
        d = {item.item_gender: {} for item in object_list}
        context['d'] = d
        for item in object_list:
            d[item.item_gender][item.item_type] = list()

        for item in object_list:
            if item.item_category not in d[item.item_gender][item.item_type]:
                d[item.item_gender][item.item_type].append(item.item_category)
        return context


class BrandView(ListView):
    model = Item
    template_name = 'search_nested.html'

    def get_queryset(self):
        brand_slug = self.kwargs['brand_slug']
        brand = ItemBrand.objects.get(slug=brand_slug)
        object_list = Item.objects.filter(item_brand=brand)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BrandView, self).get_context_data(**kwargs)
        object_list = self.get_queryset()
        d = {item.item_gender: {} for item in object_list}
        context['d'] = d
        brand_slug = self.kwargs['brand_slug']
        brand = ItemBrand.objects.get(slug=brand_slug)
        context['brand'] = brand
        context['query'] = brand_slug
        for item in object_list:
            d[item.item_gender][item.item_type] = list()
        for item in object_list:
            if item.item_category not in d[item.item_gender][item.item_type]:
                d[item.item_gender][item.item_type].append(item.item_category)
        return context


def gender_view(request, gender_slug):
    items = Item.objects.filter(item_gender__slug=gender_slug)[:4][::-1]
    types = ItemType.objects.all()
    context = {'items': items, 'gender_slug': gender_slug,
               'types': types}
    return render(request, 'gender.html', context=context)


def type_view(request, gender_slug, type_slug):
    context = {'gender_slug': gender_slug, 'type_slug': type_slug}
    gender = ItemGender.objects.get(slug=gender_slug)
    categories = ItemCategory.objects.filter(type__slug=type_slug)
    types = ItemType.objects.all()
    items = Item.objects.filter(item_gender__slug=gender_slug,
                                item_type__slug=type_slug)
    context['categories'] = categories
    context['items'] = items
    context['types'] = types
    context['gender'] = gender
    return render(request, 'type.html', context=context)


def category_view(request, gender_slug, type_slug, category_slug):
    context = {'gender_slug': gender_slug, 'type_slug': type_slug, 'category_slug': category_slug}
    gender = ItemGender.objects.get(slug=gender_slug)
    types = ItemType.objects.all()
    categories = ItemCategory.objects.filter(type__slug=type_slug)
    items = Item.objects.filter(item_gender__slug=gender_slug,
                                item_type__slug=type_slug,
                                item_category__slug=category_slug,
                                quantity__gt=0)
    context['categories'] = categories
    context['items'] = items
    context['types'] = types
    context['gender'] = gender
    return render(request, 'category.html', context=context)


def item_view(request, item_slug):

    types = ItemType.objects.all()
    item = Item.objects.get(slug=item_slug)
    sizes = ItemStock.objects.filter(item=item)
    gender_slug = item.item_gender.slug
    context = {'item_slug': item_slug, 'item': item,
               'types': types, 'gender_slug': gender_slug,
               'sizes': sizes,}

    if request.user.is_authenticated:
        favorite = Favorites.objects.filter(user=request.user)
        favorite = [fav.fav_item for fav in favorite]
        context['favorite'] = favorite
    return render(request, 'item.html', context=context)


def select_size(request, item_slug, size_slug):
    item = Item.objects.get(slug=item_slug)
    sizes = ItemStock.objects.filter(item=item)
    itemstock = ItemStock.objects.get(item__slug=item_slug, size__slug=size_slug)
    context = {'itemstock': itemstock, 'item': item, 'sizes': sizes, 'size_slug': size_slug}
    return render(request, 'item.html', context=context)


def add_to_cart(request, item_slug, size_slug):
    size = ItemSize.objects.get(slug=size_slug)
    itemstock = ItemStock.objects.get(item__slug=item_slug, size=size)
    referer = request.META.get("HTTP_REFERER")

    if itemstock.quantity <= 0:
        return redirect('shop:item', item_slug)
    if not request.session.session_key:
        request.session.create()
    session = request.session.session_key
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)
        else:
            cart = Cart.objects.get_or_create(session=session)
        item_in_cart = ItemInCart.objects.get_or_create(cart=cart[0], item=itemstock)
        if item_in_cart[0].quantity >= itemstock.quantity:
            messages.error(request=request, message=f"You can't buy more than {itemstock.quantity} pieces of this item")
            return HttpResponseRedirect(referer)
        cart[0].items.add(itemstock)
        cart[0].save()
        item_in_cart[0].quantity += 1
        item_in_cart[0].save()
    except Exception as e:
        print('views215', e)
        return redirect('/')
    return HttpResponseRedirect(referer)


def delete_from_cart(request, item_slug, size_slug):
    size = ItemSize.objects.get(slug=size_slug)
    itemstock = ItemStock.objects.get(item__slug=item_slug, size=size)
    if not request.session.session_key:
        request.session.create()
    session = request.session.session_key
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.get(session=session)
        item_in_cart = ItemInCart.objects.get(cart=cart, item=itemstock)
        if item_in_cart.quantity > 1:
            item_in_cart.quantity -= 1
            item_in_cart.save()
        else:
            item_in_cart.delete()
            print(cart.items.all())
    except Exception as e:
        print('line235', e)
        return redirect('/')
    referer = request.META.get("HTTP_REFERER")
    return HttpResponseRedirect(referer)


@login_required
def add_to_favorite(request, item_slug):
    item = Item.objects.get(slug=item_slug)
    favorites = Favorites.objects.filter(user=request.user)
    favorites = [fav.fav_item for fav in favorites]
    referer = request.META.get("HTTP_REFERER")

    if item in favorites:
        return HttpResponseRedirect(referer)
    object = Favorites.objects.create(fav_item=item)
    return HttpResponseRedirect(referer)


@login_required
def delete_from_favorite(request, item_slug):
    item = Item.objects.get(slug=item_slug)
    Favorites.objects.get(fav_item=item, user=request.user).delete()
    referer = request.META.get("HTTP_REFERER")
    return HttpResponseRedirect(referer)

