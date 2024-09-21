from django.urls import path
from .views import (
    CheckoutView,
    PaymentVerificationView
)

app_name = 'payments'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('verify-payment/', PaymentVerificationView.as_view(), name='verify_payment'),

]
