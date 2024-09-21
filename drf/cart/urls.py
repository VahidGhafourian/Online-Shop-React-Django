from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart-add-get'),  # For GET and POST requests
    path('review/', views.CartView.as_view(), name='cart-review'),
    path('<int:item_id>/', views.CartView.as_view(), name='cart-item-edit'),  # For DELETE and PUT requests
    path('clear/', views.ClearCartView.as_view(), name='cart-clear'),
    path('apply-coupon/', views.ApplyCouponView.as_view(), name='apply-coupon'),

]
