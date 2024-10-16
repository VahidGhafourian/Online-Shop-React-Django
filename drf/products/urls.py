from django.urls import path

from .views import (
    CategoryDetailView,
    CategoryListView,
    InventoryView,
    ProductImageDetailView,
    ProductImageListView,
    ProductListView,
    ProductSearchFilterView,
    ProductVariantDetailView,
    ProductVariantListView,
    ReviewView,
    TagDetailView,
    TagListView,
)

app_name = "products"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductListView.as_view(), name="product-detail"),
    path(
        "product-variants/",
        ProductVariantListView.as_view(),
        name="product-variant-list",
    ),
    path(
        "product-variants/<int:pk>/",
        ProductVariantDetailView.as_view(),
        name="product-variant-detail",
    ),
    path("product-images/", ProductImageListView.as_view(), name="product-image-list"),
    path(
        "product-images/<int:pk>/",
        ProductImageDetailView.as_view(),
        name="product-image-detail",
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<str:slug>/", TagDetailView.as_view(), name="tag-detail"),
    path(
        "inventory/<int:product_variant_id>/",
        InventoryView.as_view(),
        name="inventory-detail",
    ),
    path("review/<int:product_id>/", ReviewView.as_view(), name="review-list"),
    path(
        "products/search/",
        ProductSearchFilterView.as_view(),
        name="product-search-filter",
    ),
]
