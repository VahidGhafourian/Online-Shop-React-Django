from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payments/', views.PaymentsList.as_view(), name="payments_list"),
    path('payments/<int:id>/', views.PaymentDetail.as_view(), name="payment_detail"),
    path('payments/create/', views.CreatePayment.as_view(), name="create_payment"),
    path('transactions/', views.TransactionsList.as_view(), name="transactions_list"),
    path('transactions/<int:id>/', views.TransactionDetail.as_view(), name="transactions_detail"),
    path('discounts/', views.DiscountList.as_view(), name="discounts_list"),
    path('discounts/<int:id>/', views.DiscountDetail.as_view(), name="discounts_detail"),
    path('coupons/', views.CouponList.as_view(), name="coupon_list"),
    path('coupons/<int:id>/', views.CouponDetail.as_view(), name="coupon_detail"),
    path('coupons/apply/', views.ApplyCoupon.as_view(), name="apply_coupon"),

]
