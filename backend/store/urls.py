from django.urls import path 
from . import views

urlpatterns = [
    path('products/', views.getproducts),
    path('products/<int:pk>/', views.getproduct),
    path('categories/', views.getcategory),
    path('cart/', views.getcart),
    path('cart/add/', views.addtocart),
    path('cart/remove/', views.removefromcart),
    path('cart/update/', views.updatecart),
  ]
