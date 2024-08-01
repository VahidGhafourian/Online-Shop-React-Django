from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category # Order, OrderItem, Payment
from .serializers import ProductSerializer, CategorySerializer # OrderSerializer
from account.serializers import AddressSerializer
from account.models import Address
from rest_framework import status
from utils import generate_transactio_id
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
import requests
from django.http import JsonResponse

class ProductsList(APIView):
    """
        Method: Get \n
            Get all list of products (for a category)
        input: \n
            optional: category_slug
        return: \n
            list of products (for a category)

    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, category_slug=None):
    #     products = Product.objects.filter(available=True)
    #     categories = Category.objects.all()
    #     if category_slug:
    #         categories = Category.objects.get(slug=category_slug)
    #         products = products.filter(category=categories)
    #     categories = CategorySerializer(instance=categories, many=True)
    #     products = ProductSerializer(instance=products, many=True)
    #     return Response(data={'products': products.data,
    #                           'category': categories.data,}, status=status.HTTP_200_OK)

class ProductDetail(APIView):
    """
        Method: Get \n

        input: \n

        return: \n
    """
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
# class OrderAddView(APIView):
    # permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     print('='*20)
    #     products={}
    #     data = request.data
    #     for item in data['items']:
    #         try:
    #             products[Product.objects.get(id=item['id'])] = item['quantity']
    #             address = Address.objects.get(user=request.user, id=data['shipping_address'])
    #         except Product.DoesNotExist:
    #             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    #         except Address.DoesNotExist:
    #             return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
    #     order = Order.objects.create(user=request.user, transaction_id=generate_transactio_id(),
    #                                  shipping_address=address)
    #     for product, quantity in products.items():
    #         OrderItem.objects.create(order=order, product=product, price=product.price,
    #                                  quantity=quantity)
    #     serializer = OrderSerializer(instance=order)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

# class DoPayment(APIView):
    # permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     print('||'*20)
    #     print(request.data)
    #     data = request.data
    #     order = Order.objects.get(user=request.user, transaction_id=data['transaction_id'])
    #     print(order)
    #     payment = Payment.objects.create(order=order)
    #     api_url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    #     data = {
    #         "merchant_id": "5dcf4407-29f5-4a04-8177-5c2172d86db1",
    #         "amount": 20000,
    #         "description": "Payment description",
    #         "callback_url": "http://localhost:3000/payment_info/",
    #     }
    #     headers = {
    #         'accept': 'application/json',
    #         'content-type': 'application/json',
    #     }
    #     # Send a POST request to ZarinPal API
    #     response = requests.post(api_url, json=data, headers=headers)
    #     print(response)
    #     if response.status_code == 200:
    #         # Parse the JSON response
    #         response_data = response.json()
    #         print(response_data)
    #         # Check if the payment request was successful
    #         if response_data.get("data", {}).get("code") == 100:
    #             # Payment request successful
    #             payment_url = response_data.get("data", {}).get("authority")
    #             return JsonResponse({"payment_url": payment_url})
    #         else:
    #             # Payment request failed
    #             error_message = response_data.get("errors", {}).get("message", "Unknown error")
    #             return JsonResponse({"error": error_message}, status=400)
    #     else:
    #         # Request to ZarinPal API failed
    #         return JsonResponse({"error": "Failed to connect to ZarinPal API"}, status=500)


# class UserOrders(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     orders = Order.objects.filter(user=request.user)
    #     orders = OrderSerializer(orders, many=True)
    #     return Response(orders.data, status=status.HTTP_200_OK)
"""
