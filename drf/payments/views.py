from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cart.models import Cart
from account.models import Address
from orders.serializers import OrderSerializer
from orders.models import Order, OrderItem
from zarinpal import views as zarinpal_views
from payments.models import Payment
from django.db import transaction
from .models import Discount, Coupon
from .serializers import DiscountSerializer, CouponSerializer
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=rest_status.HTTP_400_BAD_REQUEST)

    shipping_address_id = request.data.get('shipping_address')
    if not shipping_address_id:
        return Response({"error": "Shipping address is required"}, status=rest_status.HTTP_400_BAD_REQUEST)

    shipping_address = Address.objects.filter(id=shipping_address_id, user=request.user).first()
    if not shipping_address:
        return Response({"error": "Invalid shipping address"}, status=rest_status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.product_variant.price * item.quantity for item in cart.items.all())

    order = Order.objects.create(user=request.user, shipping_address=shipping_address)
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_variant=cart_item.product_variant,
            price=cart_item.product_variant.price,
            quantity=cart_item.quantity
        )
        # Update inventory
        inventory = cart_item.product_variant.inventory
        inventory.quantity -= cart_item.quantity
        inventory.save()

    cart.items.all().delete()
    cart.coupon = None
    cart.save()

    # Create a pending payment
    payment = Payment.objects.create(
        order=order,
        amount=total_amount,
        payment_method='Zarinpal',
        status=Payment.Status.PENDING  # Initially set to Pending
    )
    # Initiate Zarinpal payment
    payment_response = zarinpal_views.send_request(request, data={'amount': payment.amount})
    if payment_response['status']:
        # Store the payment authority in the order for later verification
        order.transaction_id = payment_response['authority']
        order.save()
        payment.transaction_id = payment_response['authority']
        payment.save()

        return Response({
            "order": OrderSerializer(order).data,
            "payment_url": payment_response['url']
        }, status=rest_status.HTTP_201_CREATED)
    else:
        # If payment initiation fails, mark the order and payment as failed
        order.status = Order.Status.FAILED
        order.save()
        return Response({"error": "Payment initiation failed"}, status=rest_status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def payment_verification_view(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    order = Order.objects.filter(transaction_id=authority).first()
    if order:
        payment = Payment.objects.filter(order=order, transaction_id=authority).first()
        if not payment:
            return Response({"error": "Payment not found"}, status=rest_status.HTTP_404_NOT_FOUND)

        if status == 'OK':
            verification_response = zarinpal_views.verify(authority, payment.amount)
            if verification_response['status']:
                # Payment was successful
                payment.status = Payment.Status.SUCCESSFUL
                payment.save()
                order.status = Order.Status.PAID
                order.save()
                return Response({
                    "message": "Payment was successful",
                    "order_id": order.id,
                    "payment_id": payment.id
                }, status=rest_status.HTTP_200_OK)
            else:
                # Payment failed
                payment.status = Payment.Status.FAILED
                payment.save()
                order.status = Order.Status.FAILED
                order.save()
                return Response({"error": "Payment verification failed"}, status=rest_status.HTTP_400_BAD_REQUEST)
        else:
            payment.status = Payment.Status.FAILED
            payment.save()
            order.status = Order.Status.FAILED
            order.save()
            return Response({"error": "Payment was not successful"}, status=rest_status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"error": "Order not found"}, status=rest_status.HTTP_404_NOT_FOUND)


class DiscountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class CouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.usage_count > 0:
            return Response({"error": "Cannot delete a coupon that has been used."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
