from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listings_page, name='listings_page'), # Main listings
    path('create/', views.create_listing, name='create_listing'),
    path('<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('<slug:slug>/edit/', views.edit_listing, name='edit_listing'),
    path('<slug:slug>/delete/', views.delete_listing, name='delete_listing'),
    path('<slug:slug>/inquire/', views.inquiry_view, name='inquiry'), 
    path('<slug:slug>/book/', views.booking_view, name='booking'),

]


