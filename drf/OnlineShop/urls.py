from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/order/', include('orders.urls')),
    path('api/payment/', include('payments.urls')),
    path('api/account/', include('account.urls')),
    path('api/', include('notifications.urls')),
    path('zarinpal/', include('zarinpal.urls')),
]
