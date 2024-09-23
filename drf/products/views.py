from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Product,
                     Category,
                     ProductVariant,
                     ProductImage,
                     Tag,
                     Inventory,
                     Review,)
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          ProductVariantSerializer,
                          ProductImageSerializer,
                          TagSerializer,
                          InventorySerializer,
                          ReviewSerializer)
from rest_framework import status
from utils import generate_transactio_id
import json
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import get_object_or_404


class ProductListView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk=None):
        """
          Method: GET for `api/products/` \n
            - Get all list of products \n
          input: \n
            - optional: category_slug, search \n
          return: \n
            - list of products (for a category) \n

          Method: GET for `api/products/{id}/` \n
            - Retrieves a single product by its primary key (pk).\n
          input: \n
            - pk: The primary key of the product to retrieve.\n
          return: \n
          - A Response object containing the serialized data of the product.\n
          - Status code: 200 OK if the product is found.\n
        """
        if pk:
            return self.get_detail(request, pk)
        return self.get_list(request)

    def get_list(self, request):
        category_id = request.query_params.get('category')
        search_query = request.query_params.get('search')
        page = request.query_params.get('page', 1)

        cache_key = f"products_list_{category_id}_{search_query}_{page}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        products = Product.objects.select_related('category').prefetch_related('variants', 'images')

        if category_id:
            products = products.filter(category_id=int(category_id))

        # Searching by title
        # TODO: if you are using title to search. add index to it.
        if search_query:
            products = products.filter(title__icontains=search_query)

        paginator = Paginator(products, 10)
        products_page = paginator.get_page(page)

        serializer = ProductSerializer(products_page, many=True)

        data = {
            'results': serializer.data,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': int(page)
        }

        cache.set(cache_key, data, timeout=300)  # Cache for 5 minutes

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
              Insert one product to db \n
          input: \n
              ['category', 'title', 'slug','description', 'available','attributes'] \n
          return: \n
              If successful returns Created product data otherwise return errors. \n
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_detail(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
          Method: PUT \n
            - Partially updates an existing product.\n
          input: \n
          - pk: The primary key of the product to update.\n
          - data: ['category', 'title', 'description', 'available', 'attributes']\n
          return: \n
            - A Response object containing the serialized data of the updated product.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
          Method: DELETE \n
            - Deletes a product by its primary key (pk).\n
          input: \n
            - pk: The primary key of the product to delete.\n
          return:
            - Status code: 204 NO CONTENT if the deletion is successful.\n
        """
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductVariantListView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, ):
        """
          Method: GET \n
            - Retrieves a list of product variants. Optionally filters by product ID.\n
          input: \n
            - product (optional query parameter): The ID of the product to filter variants by.\n
          return: \n
            - A Response object containing a list of serialized product variant data.\n
            - Status code: 200 OK.\n
        """
        product_id = request.query_params.get('product')

        if product_id:
            variants = ProductVariant.objects.filter(product_id=product_id)
        else:
            variants = ProductVariant.objects.all()

        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
            - Creates a new product variant.\n
          input: \n
            - data: A dictionary containing the data for the new product variant.\n
          return: \n
            - A Response object containing the serialized data of the newly created product variant. [
                'product', 'price',
                'quantity', 'attributes'
          ] \n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductVariantDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        try:
            return ProductVariant.objects.get(pk=pk)
        except ProductVariant.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
          Method: GET \n
            - Retrieves a single product variant by its primary key (pk).\n
          Input:\n
            - pk: The primary key of the product variant to retrieve.\n
          Return:\n
            - A Response object containing the serialized data of the product variant.\n
        """
        variant = self.get_object(pk)
        serializer = ProductVariantSerializer(variant)
        return Response(serializer.data)

    def put(self, request, pk):
        """
          Method: PUT \n
            - Partially updates an existing product variant.\n
          input: \n
            - pk: The primary key of the product variant to update.\n
            - request.data: A dictionary containing the data to update the product variant with.\n
          return: \n
            - A Response object containing the updated product variant's serialized data.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        variant = self.get_object(pk)
        serializer = ProductVariantSerializer(variant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
          Method: DELETE \n
            - Deletes a product variant by its primary key (pk).\n
          input: \n
            - pk: The primary key of the product variant to delete.\n
          return: \n
            - Status code: 204 NO CONTENT if the deletion is successful.\n
        """
        variant = self.get_object(pk)
        variant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_data(self, request):
        return request.data if type(request.data)!=str else json.loads(request.data)

    def get(self, request):
        """
          Method: GET \n
            - Description: Retrieves a list of all categories.\n
          input: \n
            - None\n
          return: \n
            - A Response object containing a list of serialized category data.\n
            - Status code: 200 OK.\n
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
            - Description: Creates a new category.\n
          input: \n
            - data: A dictionary containing the data for the new category.\n
          return: \n
            - A Response object containing the serialized data of the newly created category.\n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        """
          Method: GET \n
            - Description: Retrieves a single category by its primary key (pk).\n
          input: \n
            - pk: The primary key of the category to retrieve.\n
          return: \n
            - A Response object containing the serialized data of the category.\n
            - Status code: 200 OK.\n
        """
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
          Method: PUT \n
            - Description: Partially updates an existing category.\n
          input: \n
            - pk: The primary key of the category to update.\n
            - request.data: A dictionary containing the data to update the category with.\n
          return: \n
            - A Response object containing the updated category's serialized data.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid\n
        """
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
          Method: DELETE \n
            - Description: Deletes a category by its primary key (pk).\n
          input: \n
            - pk: The primary key of the category to delete.\n
          return: \n
            - Status code: 204 NO CONTENT if the deletion is successful.\n
        """
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageListView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        """
          Method: GET \n
            - Description: Retrieves a list of product images. Optionally filters by product ID.\n
          input: \n
            - product (optional query parameter): The ID of the product to filter images by.\n
          return: \n
            - A Response object containing a list of serialized product image data.\n
            - Status code: 200 OK.\n
        """
        product_id = request.query_params.get('product')

        if product_id:
            images = ProductImage.objects.filter(product_id=product_id)
        else:
            images = ProductImage.objects.all()

        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
            - Description: Creates a new product image.\n
          input: \n
            - data: A dictionary containing the data for the new product image.\n
          return: \n
            - A Response object containing the serialized data of the newly created product image.\n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        try:
            return ProductImage.objects.get(pk=pk)
        except ProductImage.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
          Method: GET \n
            - Description: Retrieves a single product image by its primary key (pk).\n
          input: \n
            - pk: The primary key of the product image to retrieve.\n
          return: \n
            - A Response object containing the serialized data of the product image.\n
            - Status code: 200 OK.\n
        """
        image = self.get_object(pk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
          Method: PUT \n
            - Description: Partially updates an existing product image.\n
          input: \n
            - pk: The primary key of the product image to update.\n
            - request.data: A dictionary containing the data to update the product image with.\n
          return: \n
            - A Response object containing the updated product image's serialized data.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        image = self.get_object(pk)
        serializer = ProductImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
          Method: DELETE \n
            - Description: Deletes a product image by its primary key (pk).\n
          input: \n
            - pk: The primary key of the product image to delete.\n
          return: \n
            - Status code: 204 NO CONTENT if the deletion is successful.\n
        """
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagListView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        """
          Method: GET \n
            - Description: Retrieves a list of all tags.\n
          input: \n
            - None\n
          return: \n
            - A Response object containing a list of serialized tag data.\n
            - Status code: 200 OK.\n
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
          Method: POST \n
            - Description: Creates a new tag.\n
          input: \n
            - data: A dictionary containing the data for the new tag.\n
          return: \n
            - A Response object containing the serialized data of the newly created tag.\n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
          Method: GET \n
            - Description: Retrieves a single tag by its primary key (pk).\n
          input: \n
            - pk: The primary key of the tag to retrieve.\n
          return: \n
            - A Response object containing the serialized data of the retrieved tag.\n
            - Status code: 200 OK.\n
        """
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
          Method: PUT \n
            - Description: Updates an existing tag by its primary key (pk).\n
          input: \n
            - pk: The primary key of the tag to update.\n
            - request.data: A dictionary containing the updated data for the tag.\n
          return: \n
            - A Response object containing the serialized data of the updated tag.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
          Method: DELETE \n
            - Description: Deletes a tag by its primary key (pk).\n
          input: \n
            - pk: The primary key of the tag to delete.\n
          return: \n
            - A Response object with no content.\n
            - Status code: 204 NO CONTENT.\n
        """
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InventoryView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, product_variant_id):
        try:
            return ProductVariant.objects.get(pk=product_variant_id).inventory
        except Tag.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, product_variant_id):
        """
          Method: GET \n
            - Description: Retrieves the inventory record for a specific product variant.\n
          input: \n
            - product_variant_id: The primary key of the product variant.\n
          return: \n
            - A Response object containing the serialized data of the retrieved inventory record.
            - Status code: 200 OK.
        """
        inventory = self.get_object(product_variant_id)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_variant_id):
        """
          Method: POST \n
            - Description: Creates a new inventory record for a specific product variant.\n
          input: \n
            - product_variant_id: The primary key of the product variant.\n
            - request.data: A dictionary containing the data for the new inventory record.\n
          return: \n
            - A Response object containing the serialized data of the newly created inventory record.\n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_variant_id):
        """
          Method: PUT \n
            - Description: Updates the inventory record for a specific product variant.\n
          input: \n
            - product_variant_id: The primary key of the product variant.\n
            - request.data: A dictionary containing the updated data for the inventory record.\n
          return: \n
            - A Response object containing the serialized data of the updated inventory record.\n
            - Status code: 200 OK if the update is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        inventory = self.get_object(product_variant_id)
        serializer = InventorySerializer(inventory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_variant_id):
        """
          Method: DELETE \n
            - Description: Deletes the inventory record for a specific product variant.\n
          input: \n
            - product_variant_id: The primary key of the product variant.\n
          return: \n
            - A Response object with no content.\n
            - Status code: 204 NO CONTENT.\n
        """
        inventory = self.get_object(product_variant_id)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_object(self, product_id):
        try:
            return Review.objects.filter(product = product_id)
        except Review.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, product_id):
        """
          Method: GET \n
            - Description: Retrieves a list of reviews for a specific product.\n
          input: \n
            - product_id: The primary key of the product.\n
          return: \n
            - A Response object containing a list of serialized review data for the specified product.\n
            - Status code: 200 OK.\n
        """
        review = self.get_object(product_id)
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        """
          Method: POST \n
            - Description: Creates a new review for a specific product.\n
          input: \n
            - product_id: The primary key of the product.\n
            - request.data: A dictionary containing the data for the new review.\n
          return: \n
            - A Response object containing the serialized data of the newly created review.\n
            - Status code: 201 CREATED if the creation is successful.\n
            - Status code: 400 BAD REQUEST if the data is invalid.\n
        """
        serializer = ReviewSerializer(data={**request.data, 'product': product_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
