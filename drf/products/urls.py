from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.ProductsList.as_view(), name="products_list"),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('category/', views.CategoryList.as_view(), name='categories_list'),
]
