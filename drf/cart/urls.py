from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart-list'),  # For GET and POST requests
    path('cart/<int:item_id>/', views.CartView.as_view(), name='cart-item'),  # For DELETE and PUT requests
]
