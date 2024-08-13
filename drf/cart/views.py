from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from payments.models import Discount

class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart = self.apply_discounts(cart)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def apply_discounts(self, cart):
        for item in cart.items.all():
            discounts = Discount.objects.filter(applicable_to=item.product, is_active=True)
            for discount in discounts:
                item.price -= discount.calculate_discount(item.price)
        return cart

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        data = request.data
        data['cart'] = cart.id
        #TODO: if user added one product variant two times add ++ to previous item_count
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveItemFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
