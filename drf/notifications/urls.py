from django.urls import include, path
from rest_framework.routers import DefaultRouter

from notifications.views import NotificationViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")

app_name = "notifications"

urlpatterns = [
    path("", include(router.urls)),
]
