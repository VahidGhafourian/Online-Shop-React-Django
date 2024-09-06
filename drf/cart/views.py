from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from payments.models import Discount

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        # print(created)
        return cart

    """
    Method: GET
        Retrieve the cart details.
    Input:
        - Authenticated request
    Return:
        - ['user', 'items']
    """
    def get(self, request):
        cart = self.get_cart(request)
        cart = self.apply_discounts(cart)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Method: POST
        Add an item to the cart.
    Input:
        - ['product_variant', 'items_count']
    Return:
        - ['product_variant', 'items_count']
    """
    def post(self, request):
        cart = self.get_cart(request)
        data = request.data
        # print(cart.items)
        data['cart'] = cart.id

        # Check if the item already exists and update quantity if necessary
        existing_item = CartItem.objects.filter(cart=cart, product_variant=data.get('product_variant')).first()
        if existing_item:
            data['items_count'] = existing_item.items_count + int(data.get('items_count', 1))
            serializer = CartItemSerializer(existing_item, data=data, partial=True)
        else:
            serializer = CartItemSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Method: DELETE
        Remove an item from the cart.
    Input:
        - item_id
    Return:
        - status 200 if its done. otherwise 404.
    """
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=item_id)
            cart_item.delete()
            return Response(status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    """
    Method: PUT
        Update an item in the cart.
    Input:
        - item_id, ['items_count']
    Return:
        - status 200 if its done. otherwise 404.
    """
    def put(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=item_id)
            serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CartItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def apply_discounts(self, cart):
        """Apply discounts to the cart items."""
        for item in cart.items.all():
            discounts = Discount.objects.filter(applicable_to=item.product_variant, is_active=True)
            for discount in discounts:
                item.price -= discount.calculate_discount(item.price)
        return cart
