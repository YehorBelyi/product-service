from django.contrib import admin
from django.urls import path
from ProductService import views

urlpatterns = [
    path('listing/search', views.ListingSearchView.as_view(), name='listing-search'),
    path('listing/create', views.ListingCreateView.as_view(), name='listing-create'),
    path('listing/<int:pk>/details', views.ListingDetailView.as_view(), name='listing-details')
]
