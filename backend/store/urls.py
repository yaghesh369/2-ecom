from django.urls import path 
from . import views

urlpatterns = [
    path('products/', views.getproducts),
    path('products/<int:pk>/', views.getproduct),
    path('categories/', views.getcategory),
  ]
