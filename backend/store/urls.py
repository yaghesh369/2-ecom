from django.urls import path 
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.register),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', views.getproducts),
    path('products/<int:pk>/', views.getproduct),
    path('categories/', views.getcategory),
    path('cart/', views.getcart),
    path('cart/add/', views.addtocart),
    path('cart/remove/', views.removefromcart),
    path('cart/update/', views.updatecart),
    path('orders/create/', views.createorder),
  ]
