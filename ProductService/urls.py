from django.contrib import admin
from django.urls import path
from ProductService import views

urlpatterns = [
    path('listing/search', views.ListingSearchView.as_view(), name='listing-search')
]
