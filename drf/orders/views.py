from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Order, OrderItem #, Refund
from .serializers import OrderSerializer, OrderItemSerializer #, RefundSerializer

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Method: GET
        Retrieve the orders list
    Input:
        - Authenticated request
    Return:
        - list of orders
    """
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # """
    # Method: POST

    # Input:
    #     - Authenticated request
    # Return:
    #     -
    # """
    # def post(self, request):
    #     serializer = OrderSerializer(data={**request.data , 'user': request.user.id})
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return Order.objects.get(user=user, id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    """
    Method: GET
        Retrieve the User Order
    Input:
        - Authenticated request
    Return:
        - ['user', 'total_price', 'items', 'completed_at']
    """
    def get(self, request, pk):
        order = self.get_object(request.user, pk)
        if not order:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # """
    # Method:

    # Input:
    #     -
    # Return:
    #     -
    # """
    # def put(self, request, pk):
    #     order = self.get_object(request.user, pk)
    #     serializer = OrderSerializer(order, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # """
    # Method:

    # Input:
    #     -
    # Return:
    #     -
    # """
    # def delete(self, request, pk):
    #     order = self.get_object(request.user, pk)
    #     if not order:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     order.delete()
    #     return Response(status=status.HTTP_200_OK)


class OrderItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_items(self, user, id):
        if OrderItem.objects.filter(order=id).exists():
            return OrderItem.objects.filter(order__user=user, order=id)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    """
    Method:
        Retrieve the order's items list
    Input:
        - order_id
    Return:
        - list of items
    """
    def get(self, request):
        order_id = request.query_params.get('order')
        items = self.get_items(request.user, order_id)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # """
    # Method:

    # Input:
    #     -
    # Return:
    #     -
    # """
    # def post(self, request):
    #     serializer = OrderItemSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return OrderItem.objects.get(order__user=user, pk=pk)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    """
    Method:
        Retrieve the Item detail
    Input:
        - item_id
    Return:
        - ['id', 'order', 'product_variant', 'quantity', 'price']
    """
    def get(self, request, pk):
        item = self.get_object(request.user, pk)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    # """
    # Method:

    # Input:
    #     -
    # Return:
    #     -
    # """
    # def put(self, request, pk):
    #     item = self.get_object(request.user, pk)
    #     serializer = OrderItemSerializer(item, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # """
    # Method:

    # Input:
    #     -
    # Return:
    #     -
    # """
    # def delete(self, request, pk):
    #     item = self.get_object(request.user, pk)
    #     item.delete()
    #     return Response(status=status.HTTP_200_OK)

# class OrderCancel(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, id):
#         order = Order.objects.filter(id=id, user=request.user).first()
#         if not order:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         order.status = 'Cancelled'
#         order.save()
#         return Response(status=status.HTTP_200_OK)

# class RefundRequestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, order_id):
#         serializer = RefundSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(order_id=order_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
