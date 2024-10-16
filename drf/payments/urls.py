from django.urls import path

from .views import checkout_view, payment_verification_view

app_name = "payments"

urlpatterns = [
    path("checkout/", checkout_view, name="checkout"),
    path("verify-payment/", payment_verification_view, name="verify_payment"),
]
