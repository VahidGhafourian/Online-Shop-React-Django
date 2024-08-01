from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('products/', views.GetProdutsView.as_view(), name="get_products"),

]
