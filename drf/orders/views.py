# orders/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem #, Refund
from .serializers import OrderSerializer, OrderItemSerializer #, RefundSerializer

class OrdersList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user, id):
        try:
            return Order.objects.get(user=user, id=id)
        except Order.DoesNotExist:
            return None

    def get(self, request, id):
        order = self.get_object(request.user, id)
        if not order:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id):
        order = self.get_object(request.user, id)
        if not order:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        order = self.get_object(request.user, id)
        if not order:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderCancel(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        order = Order.objects.filter(id=id, user=request.user).first()
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.status = 'Cancelled'
        order.save()
        return Response(status=status.HTTP_200_OK)

# class RefundRequestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, order_id):
#         serializer = RefundSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(order_id=order_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
