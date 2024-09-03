from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Product,
                     Category,
                     ProductVariant,
                     ProductImage)
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          ProductVariantSerializer,
                          ProductImageSerializer)
from rest_framework import status
from utils import generate_transactio_id
import json
from rest_framework.permissions import IsAdminUser, AllowAny

class ProductListView(APIView):
    """
        Method: Get \n
            Get all list of products
        input: \n
            optional: category_slug
        return: \n
            list of products (for a category)
    """
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):

        category_id = request.query_params.get('category')
        search_query = request.query_params.get('search')

        products = Product.objects.all()

        if category_id:
            products = products.filter(category_id=int(category_id))

        # Searching by title
        # TODO: if you are using title to search. add index to it.
        if search_query:
            products = products.filter(title__icontains=search_query)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    """
        Method: Get \n

        input: \n

        return: \n
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryListView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_data(self, request):
        return request.data if type(request.data)!=str else json.loads(request.data)

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
