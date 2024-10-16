from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", RedirectView.as_view(url="/swagger-ui/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("products.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/order/", include("orders.urls")),
    path("api/payment/", include("payments.urls")),
    path("api/account/", include("account.urls")),
    path("api/", include("notifications.urls")),
    path("zarinpal/", include("zarinpal.urls")),
]
