from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.CartDetail.as_view(), name="cart_detail"),
    path('cart/add/', views.AddToCart.as_view(), name="add_to_cart"),
    path('cart/remove/<int:item_id>/', views.RemoveItem.as_view(), name="remove_from_cart"),
    path('cart/update/<int:item_id>/', views.UpdateItem.as_view(), name="update_item"),

]
