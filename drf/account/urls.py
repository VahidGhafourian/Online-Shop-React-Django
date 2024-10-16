from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = "account"

urlpatterns = [
    path(
        "check-login-phone/",
        views.UserCheckLoginPhone.as_view(),
        name="check_login_phone",
    ),
    path("send-otp/", views.GenerateSendOTP.as_view(), name="send-otp"),
    path("verify-otp/", views.VerifyOTP.as_view(), name="verify_otp"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "user-info/", views.UserInfoView.as_view(), name="user-info"
    ),  # also use for setting password in post method
    path("add-address/", views.AddressView.as_view(), name="add-address"),
    path("user-addresses/", views.AddressView.as_view(), name="user-addresses"),
    # path('logout/', views.UserLogoutView.as_view(), name="user_logout"),
]
