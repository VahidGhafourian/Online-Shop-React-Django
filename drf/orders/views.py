from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer, OrderAdminSerializer #, RefundSerializer


class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Method: GET
            Retrieve the orders list
        Input:
            - Authenticated request
        Return:
            - list of orders
        """
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderAdminSerializer(orders, many=True)
        return Response(serializer.data)

class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderAdminSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderAdminSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminRefundOrderView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status in [Order.Status.CANCELLED, Order.Status.FAILED, Order.Status.PENDING]:
            return Response({"error": f"Cannot refund a order with {order.status} status"}, status=status.HTTP_400_BAD_REQUEST)

        for item in order.items.all():
            inventory = item.product_variant.inventory
            inventory.quantity += item.quantity
            inventory.save()

        order.status = Order.Status.CANCELLED
        order.save()

        serializer = OrderAdminSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
