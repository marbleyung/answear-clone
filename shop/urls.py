from django.urls import path
from .views import *


app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('search/', SearchResultView.as_view(), name='search'),
    path('search/<slug:gender_slug>/', SearchGenderView.as_view(), name='search_gender'),
    path('search/<slug:gender_slug>/<slug:type_slug>/', SearchTypeView.as_view(), name='search_type'),
    path('search/<slug:gender_slug>/<slug:type_slug>/<slug:category_slug>/', SearchCategoryView.as_view(),
         name='search_category'),
    path('b/<slug:brand_slug>', BrandView.as_view(), name='brand'),
    path('c/<slug:gender_slug>/', gender_view, name='gender'),
    path('c/<slug:gender_slug>/<slug:type_slug>/', type_view, name='type'),
    path('c/<slug:gender_slug>/<slug:type_slug>/<slug:category_slug>/', category_view, name='category'),
    path('item/<slug:item_slug>/', item_view, name='item'),
    path('item/<slug:item_slug>/select-size/<slug:size_slug>', select_size, name='select_size'),
    path('item/<slug:item_slug>/select-size/<slug:size_slug>/add-to-cart', add_to_cart, name='add_to_cart'),
    path('item/<slug:item_slug>/select-size/<slug:size_slug>/delete-from-cart', delete_from_cart, name='delete_from_cart'),
    path('item/<slug:item_slug>/add-to-favorite', add_to_favorite, name='add_to_favorite'),
    path('item/<slug:item_slug>/delete-from-favorite', delete_from_favorite, name='delete_from_favorite'),
]
