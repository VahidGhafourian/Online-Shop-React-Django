from django.urls import path
from .views import (
  CategoryListView,
  CategoryDetailView,
  ProductListView,
  ProductDetailView,
  )

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
