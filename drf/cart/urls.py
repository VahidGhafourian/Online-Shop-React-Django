from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.GetProdutsView.as_view(), name="get_products"),

]
