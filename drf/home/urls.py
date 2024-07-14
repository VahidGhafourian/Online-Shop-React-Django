from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('products/', views.GetProdutsView.as_view(), name="get_products"),
    path('category/<slug:category_slug>/', views.GetProdutsView.as_view(), name='category_filter'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),

    # path('order_check_add/', views.OrderAddView.as_view(), name="add_order"),
    # path('payment/', views.DoPayment.as_view(), name="do_payment"),

    # path('orders/', views.UserOrders.as_view(), name="user_orders"),

]
