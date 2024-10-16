from django.urls import path

from .views import (
    AdminOrderDetailView,
    AdminOrderListView,
    AdminRefundOrderView,
    UserOrderListView,
)

app_name = "orders"

urlpatterns = [
    path("", UserOrderListView.as_view(), name="user-order-list"),
    path("admin/", AdminOrderListView.as_view(), name="all-order-list"),
    path("<int:pk>/", AdminOrderDetailView.as_view(), name="order-detail"),
    path(
        "order-refound/admin/<int:pk>/",
        AdminRefundOrderView.as_view(),
        name="refound-order",
    ),
]
