from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderItemListView,
    OrderItemDetailView
)

app_name = 'orders'

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('order-items/', OrderItemListView.as_view(), name='order-item-list'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='order-item-detail'),
    # path('orders/<int:id>/refound/', views.RefundRequestView.as_view(), name="refund-request"), #complete when refund model added to project

]
