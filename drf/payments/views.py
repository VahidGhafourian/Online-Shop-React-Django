from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment, Transaction
from .serializers import PaymentSerializer, TransactionSerializer
from .models import Discount, Coupon
from .serializers import DiscountSerializer, CouponSerializer, ApplyCouponSerializer
from cart.models import Cart
from cart.serializers import CartSerializer

class PaymentsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = PaymentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Payment.objects.get(id=id, user=user)
        except Payment.DoesNotExist:
            return None

    def get(self, request, id):
        payment = self.get_object(id, request.user)
        if payment is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    # def put(self, request, id):
    #     payment = self.get_object(request.user, id)
    #     if not payment:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = PaymentSerializer(payment, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(payment__user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    # def get(self, request):
    #     transactions = Transaction.objects.filter(user=request.user)
    #     serializer = TransactionSerializer(transactions, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = TransactionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Transaction.objects.get(id=id, payment__user=user)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, id):
        transaction = self.get_object(id, request.user)
        if transaction is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    # def put(self, request, id):
    #     transaction = self.get_object(request.user, id)
    #     if not transaction:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountList(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = DiscountSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscountDetail(APIView):
    def get_object(self, id):
        try:
            return Discount.objects.get(id=id)
        except Discount.DoesNotExist:
            return None

    def get(self, request, id):
        discount = self.get_object(id)
        if discount is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    # def put(self, request, id):
    #     discount = self.get_object(id)
    #     if not discount:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = DiscountSerializer(discount, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id):
    #     discount = self.get_object(id)
    #     if not discount:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     discount.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CouponList(APIView):
    def get(self, request):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = CouponSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CouponDetail(APIView):
    def get_object(self, id):
        try:
            return Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            return None

    def get(self, request, id):
        coupon = self.get_object(id)
        if coupon is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

class ApplyCoupon(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                coupon = Coupon.objects.get(code=code, is_active=True).first()
                cart = Cart.objects.get(user=request.user)

                if coupon and coupon.is_valid() and cart.total >= coupon.minimum_order_value:
                    for item in cart.items.all():
                        if item.product in coupon.applicable_to.all() or item.product.category in coupon.applicable_categories.all():
                            item.price -= coupon.calculate_discount(item.price)
                    coupon.usage_count += 1
                    coupon.save()
                    cart.save()
                    serializer = CartSerializer(cart)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            except Coupon.DoesNotExist:
                return Response({'error': 'Invalid or inactive coupon code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
