from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('orders/', views.UserOrdersList.as_view(), name="user_orders"),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name="order_detail"),
    path('orders/create/', views.OrderAddView.as_view(), name="add_order"),
    path('orders/<int:id>/update/', views.OrderUpdate.as_view(), name="order_update"),
    path('orders/<int:id>/cancel/', views.OrderCancel.as_view(), name="order_cancel"),
    # path('orders/<int:id>/refound/', views.OrderRefund.as_view(), name="order_refund"), #complete when refund model added to project

]
