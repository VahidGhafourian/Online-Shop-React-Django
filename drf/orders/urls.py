from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # path('order_check_add/', views.OrderAddView.as_view(), name="add_order"),
    path('orders/', views.UserOrders.as_view(), name="user_orders"),

]
