from django.urls import path
from .views import (
  CategoryListView,
  CategoryDetailView,
  ProductListView,
  ProductDetailView,
  ProductVariantListView,
  ProductVariantDetailView,
  ProductImageListView,
  ProductImageDetailView,
  )

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),
         name='product-detail'),

    path('product-variants/', ProductVariantListView.as_view(),
         name='product-variant-list'),
    path('product-variants/<int:pk>/', ProductVariantDetailView.as_view(),
         name='product-variant-detail'),

    path('product-images/', ProductImageListView.as_view(),
         name='product-image-list'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(),
         name='product-image-detail'),

    path('categories/', CategoryListView.as_view(), 
         name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),
]
