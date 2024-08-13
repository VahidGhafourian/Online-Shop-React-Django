from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'account'

urlpatterns = [
    # path('register/', views.UserRegisterView.as_view(), name="user_register"),
    # path('verify/', views.UserRegisterVerifyCodeView.as_view(), name="verify_code"),
    path('check-login-phone/', views.UserCheckLoginPhone.as_view(), name="check_login_phone"),
    path('send-otp/', views.GenerateSendOTP.as_view(), name='send-otp'),
    path('verify-otp/', views.VerifyOTP.as_view(), name='verify_otp'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', views.UserInfoView.as_view(), name='user-info'),
    path('add-address/', views.AddressView.as_view(), name='add-address'),
    path('user-addresses/', views.AddressView.as_view(), name='user-addresses'),
    # path('logout/', views.UserLogoutView.as_view(), name="user_logout"),
]
