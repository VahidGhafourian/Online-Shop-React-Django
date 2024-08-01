from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('orders/', views.OrdersList.as_view(), name="orders_list"),
    path('orders/create/', views.OrdersList.as_view(), name="order_create"),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name="order_detail"),
    path('orders/<int:id>/update/', views.OrderDetail.as_view(), name="order_update"),
    path('orders/<int:id>/cancel/', views.OrderCancel.as_view(), name="order_cancel"),
    # path('orders/<int:id>/refound/', views.RefundRequestView.as_view(), name="refund-request"), #complete when refund model added to project

]
