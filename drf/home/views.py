from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Order, OrderItem, Payment
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer
from account.serializers import AddressSerializer
from account.models import Address
from rest_framework import status
from utils import generate_transactio_id
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
import requests
from django.http import JsonResponse

class GetProduts(APIView):
    """
        Method: Get \n
            Get all list of products (for a category)
        input: \n
            optional: category_slug
        return: \n
            list of products (for a category)

    """
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            categories = Category.objects.get(slug=category_slug)
            products = products.filter(category=categories)
        categories = CategorySerializer(instance=categories, many=True)
        products = ProductSerializer(instance=products, many=True)
        return Response(data={'products': products.data,
                              'category': categories.data,}, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    """
        Method: Get \n

        input: \n

        return: \n


    """
    def get(self, request, slug):
        product = Product.objects.get(Product, slug=slug)
        print(type(product))
        product = ProductSerializer(instance=product)
        return Response(data={'product': product.data}, status=status.HTTP_200_OK)

class OrderAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print('='*20)
        products={}
        data = request.data
        for item in data['items']:
            try:
                products[Product.objects.get(id=item['id'])] = item['quantity']
                address = Address.objects.get(user=request.user, id=data['shipping_address'])
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            except Address.DoesNotExist:
                return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(user=request.user, transaction_id=generate_transactio_id(),
                                     shipping_address=address)
        for product, quantity in products.items():
            OrderItem.objects.create(order=order, product=product, price=product.price,
                                     quantity=quantity)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DoPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print('||'*20)
        print(request.data)
        data = request.data
        order = Order.objects.get(user=request.user, transaction_id=data['transaction_id'])
        print(order)
        payment = Payment.objects.create(order=order)
        api_url = "https://api.zarinpal.com/pg/v4/payment/request.json"
        data = {
            "merchant_id": "5dcf4407-29f5-4a04-8177-5c2172d86db1",
            "amount": 20000,
            "description": "Payment description",
            "callback_url": "http://localhost:3000/payment_info/",
        }
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        # Send a POST request to ZarinPal API
        response = requests.post(api_url, json=data, headers=headers)
        print(response)
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()
            print(response_data)
            # Check if the payment request was successful
            if response_data.get("data", {}).get("code") == 100:
                # Payment request successful
                payment_url = response_data.get("data", {}).get("authority")
                return JsonResponse({"payment_url": payment_url})
            else:
                # Payment request failed
                error_message = response_data.get("errors", {}).get("message", "Unknown error")
                return JsonResponse({"error": error_message}, status=400)
        else:
            # Request to ZarinPal API failed
            return JsonResponse({"error": "Failed to connect to ZarinPal API"}, status=500)


class UserOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        orders = OrderSerializer(orders, many=True)
        return Response(orders.data, status=status.HTTP_200_OK)
