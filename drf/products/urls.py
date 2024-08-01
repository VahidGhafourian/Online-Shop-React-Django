from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.GetProdutsView.as_view(), name="get_products"),
    path('category/<slug:category_slug>/', views.GetProdutsView.as_view(), name='category_filter'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),
]
