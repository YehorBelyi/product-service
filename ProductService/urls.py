from django.contrib import admin
from django.urls import path
from ProductService import views
from ProductService.views import ListingUpdateView

urlpatterns = [
    path('listing/search', views.ListingSearchView.as_view(), name='listing-search'),
    path('listing/create', views.ListingCreateView.as_view(), name='listing-create'),
    path('listing/<int:pk>/details', views.ListingDetailView.as_view(), name='listing-details'),
    path('listing/<int:pk>/delete', views.ListingDeleteView.as_view(), name='listing-delete'),
    path('listing/<int:pk>/update', ListingUpdateView.as_view(), name='listing-update'),
]
