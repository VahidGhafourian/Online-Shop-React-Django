from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('products/', views.GetProduts.as_view(), name="get_products"),
    path('category/<slug:category_slug>/', views.GetProduts.as_view(), name='category_filter'),
    path('order_check_add/', views.OrderAddView.as_view(), name="add_order"),
    path('payment/', views.DoPayment.as_view(), name="do_payment"),

    path('orders/', views.UserOrders.as_view(), name="user_orders"),

]
