from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from payments.models import Coupon

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def get(self, request):
        """
          Method: GET \n
            - Retrieve the cart details. \n
          Input: \n
            - Authenticated request \n
          Return: \n
            - ['user', 'items'] \n
        """
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
            - Add an item to the cart. \n
          Input: \n
            - ['product_variant', 'quantity'] \n
          Return: \n
            - ['product_variant', 'quantity'] \n
        """
        cart = self.get_cart(request)
        product_variant_id = request.data.get('product_variant')
        quantity = int(request.data.get('quantity', 1))

        if not product_variant_id:
            return Response({"error": "Product variant ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the item is already in the cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product_variant_id=product_variant_id)
            cart_item.quantity += quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            # Item is not in the cart, create a new one
            data = request.data.copy()
            data['cart'] = cart.id
            serializer = CartItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, item_id):
        """
          Method: PUT \n
            - Update an item's quantity in the cart. \n
          Input: \n
            - [item_id, 'quantity'] \n
          Return: \n
            - status 200 if its done. otherwise 404. \n
        """
        cart_item = get_object_or_404(CartItem, cart__user=request.user, id=item_id)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        """
          Method: DELETE \n
            - Remove an item from the cart. \n"""
        cart_item = get_object_or_404(CartItem, cart__user=request.user, id=item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """
          Method: DELETE \n
            - Clear all items from the cart or remove the applied coupon. \n
          Input: \n
            action: "clear_items" or "remove_coupon". Default: "clear_items" \n
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        action = request.query_params.get('action', 'clear_items')
        if action == 'clear_items':
            cart.items.all().delete()
            message = "Cart cleared successfully"
        elif action == 'remove_coupon':
            cart.coupon = None
            cart.save()
            message = "Coupon removed successfully"
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": message}, status=status.HTTP_200_OK)

class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Method: POST \n
          - Applying coupons to the cart \n
        Input: \n
          - coupon_code \n
        """
        coupon_code = request.data.get('coupon_code')
        if not coupon_code:
            return Response({"error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(user=request.user)
        # Check if a coupon is already applied
        if cart.coupon:
            return Response({"error": "A coupon is already applied to this cart"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon code"}, status=status.HTTP_400_BAD_REQUEST)

        if not coupon.is_valid():
            return Response({"error": "Coupon is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the coupon is applicable to the items in the cart
        if not any(item.product_variant in coupon.applicable_to.all() or
                   item.product_variant.product.category in coupon.applicable_categories.all()
                   for item in cart.items.all()):
            return Response({"error": "Coupon is not applicable to any items in your cart"}, status=status.HTTP_400_BAD_REQUEST)

        cart.coupon = coupon
        cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
