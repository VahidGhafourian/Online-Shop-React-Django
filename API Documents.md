# E-commerce Platform API Documentation

## Overview

This API provides endpoints for an e-commerce platform built with Django REST Framework. It supports product browsing, cart management, checkout, order processing, and inventory management through JSON APIs.

Base URL: `http://pirnking.info/api/`

## Authentication

Most API endpoints require authentication. Use JWT (JSON Web Token) authentication by including an `Authorization` header with a valid token.


Example:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```


## API Schema and Documentation

- API Schema: `/api/schema/`
- Swagger UI: `/swagger-ui/`
- ReDoc: `/redoc/`

## Standard Headers

For all API requests, the following headers must be included:

```
headers: {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': 'Bearer YOUR_JWT_TOKEN_HERE' # (if neaded)
}
```

Note: Replace `YOUR_JWT_TOKEN_HERE` with the actual JWT token obtained during authentication.

## Application to Endpoints

The headers specified above should be used for all API endpoints documented in this API, unless explicitly stated otherwise for a specific endpoint.

## Endpoints

### User Registration and Authentication

#### Check Login Phone

- **URL**: `/api/account/check-login-phone/`
- **Method**: `POST`
- **Description**: Check if a phone number is registered before
- **Data Params**:
  ```json
  {
    "phone_number": "09121234567",
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "new_user": False,
      "have_pass": False,
    }
    ```
---

#### Send OTP

- **URL**: `/api/account/send-otp/`
- **Method**: `POST`
- **Description**: Send a one-time password to the user's phone
- **Data Params**:
  ```json
  {
    "phone_number": "09121234567",
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "success": True,
      "message": 'OTP sent successfully',
    }
    ```
---

#### Verify OTP

- **URL**: `/api/account/verify-otp/`
- **Method**: `POST`
- **Description**: Verify the OTP entered by the user
- **Data Params**:
  ```json
  {
    "phone_number": "09121234567",
    "otp": "12345"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "success": True,
      "message": 'OTP verified successfully',
      "access": 'abadfafjgjukluy...',
      "refresh": 'ladjflmiosbndv...'
    }
    ```
---

#### Refresh Token

- **URL**: `/api/account/login/refresh/`
- **Method**: `POST`
- **Description**: Refresh JWT token
- **Data Params**:
  ```json
  {
    "refresh": 'kmbldnonanfadf...' ,
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "access": 'abadfafjgjukluy...',
    }
    ```
---

#### Get User Info

- **URL**: `/api/account/user-info/`
- **Method**: `GET`
- **Description**: Get user information 
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "last_login": "2024-09-29T19:58:02.088725+03:30",
      "first_name": "vahid",
      "last_name": "ghafourian",
      "is_active": "True",
      "is_admin": "False",
      "email_confirmd": "False",
      "date_joined": "2024-09-29T19:58:02.088725+03:30",
      "date_updated": "2024-09-29T19:58:02.088725+03:30",
      "email": "vahid@example.com",
      "phone_number": "09121234567",
    }
    ```
---

#### Update User Information

- **URL**: `/api/account/user-info/`
- **Method**: `POST`
- **Description**: Update User information like password
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "first_name": "ali",
    "last_name": "abbasi",
    "email": "vahid@example.com",
    "password": "123456",
    "confirm_password": "123456"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "success": "True",
      "message": "Password updated successfully"
    }
    ```
---

#### Add Address

- **URL**: `/api/account/add-address/`
- **Method**: `POST`
- **Description**: Add a new address for the user
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "is_default": "True",
    "country": "Iran",
    "state": "Tehran",
    "city": "tehran",
    "street": "vanak",
    "postal_code": "1234567890"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": "1",
      "is_default": "True" ,
      "country": "Iran" ,
      "state": "Tehran" ,
      "city": "tehran" ,
      "street": "vanak" ,
      "postal_code": "1234567890",
      "user": "1"
    }
    ```
---

#### User Addresses

- **URL**: `/api/account/user-addresses/`
- **Method**: `GET`
- **Description**: Get all addresses for the user
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [{
      "id": "1",
      "is_default": "True" ,
      "country": "Iran" ,
      "state": "Tehran" ,
      "city": "tehran" ,
      "street": "vanak" ,
      "postal_code": "1234567890",
      "user": "1"
    },
    ...]
    ```

---

### Product Management

#### Get Product List

- **URL**: `/api/products/`
- **Method**: `GET`
- **Description**: Retrieve a paginated list of products. Supports optional filtering by category and search query.
- **Data Params**:
    - category: (optional) Filter products by category ID
    - search: (optional) Search products by title
    - page: (optional) Paginate results (default: 1)
- **Success Response**:
  - **Code**: 200
  - **Content**: 
  ```json
    {
      "results": [
        {
          "id": 1,
          "category": 2,
          "title": "Sample Product",
          "slug": "sample-product",
          "description": "This is a sample product",
          "available": true,
          "attributes": { /* product attributes */ },
          "images": [ /* product images */ ],
          "default_image": { /* default image data */ },
          "variants": [ /* product variants */ ],
          "lowest_price": 19.99,
          "average_rating": 4.5,
          "created_at": "2023-09-29T12:34:56+0000",
          "updated_at": "2023-09-29T12:34:56+0000"
        },
        ...
      ],
      "count": 100,
      "num_pages": 10,
      "current_page": 1
    }
  ```

---

#### Get Product Detail

- **URL**: `/api/products/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieve the details of a single product by its ID.
  
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "category": 2,
      "title": "Sample Product",
      "slug": "sample-product",
      "description": "This is a sample product",
      "available": true,
      "attributes": { /* product attributes */ },
      "images": [ /* product images */ ],
      "default_image": { /* default image data */ },
      "variants": [ /* product variants */ ],
      "lowest_price": 19.99,
      "average_rating": 4.5,
      "created_at": "2023-09-29T12:34:56+0000",
      "updated_at": "2023-09-29T12:34:56+0000"
    }
    ```

---

#### Create Product

- **URL**: `/api/products/`
- **Method**: `POST`
- **Description**: Create a new product.
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "category": 2,
    "title": "New Product",
    "description": "This is a new product",
    "available": true,
    "attributes": { /* product attributes */ }
  }
  ```

- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 1,
      "category": 2,
      "title": "New Product",
      "slug": "new-product",
      "description": "This is a new product",
      "available": true,
      "attributes": { /* product attributes */ },
      "images": [],
      "default_image": null,
      "variants": [],
      "lowest_price": null,
      "average_rating": null,
      "created_at": "2023-09-29T12:34:56+0000",
      "updated_at": "2023-09-29T12:34:56+0000"
    }
    ```

- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "errors": {
        "field": ["error message"]
      }
    }
    ```

---

#### Update Product

- **URL**: `/api/products/<int:pk>/`
- **Method**: `PUT`
- **Description**: Update an existing product by its ID.
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "title": "Updated Product",
    "description": "This is an updated product",
    "available": false,
    "attributes": { /* updated attributes */ }
  }
  ```

- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "category": 2,
      "title": "Updated Product",
      "slug": "updated-product",
      "description": "This is an updated product",
      "available": false,
      "attributes": { /* updated attributes */ },
      "images": [],
      "default_image": null,
      "variants": [],
      "lowest_price": null,
      "average_rating": null,
      "created_at": "2023-09-29T12:34:56+0000",
      "updated_at": "2023-09-29T12:34:56+0000"
    }
    ```
---

#### Delete Product

- **URL**: `/api/products/<int:pk>/`
- **Method**: `DELETE`
- **Description**: Delete a product by its ID.
- **Authentication**: Admin only
- **Success Response**:
  - **Code**: 204
  - **Content**: `{}`
---

#### Product Search and Filter

- **URL**: `/api/products/search/`
- **Method**: `GET`
- **Description**: Search and filter products based on various criteria
- **Query Parameters**:
  - `search`: Search query for product title or description
  - `category`: Filter by category slug
  - `tags`: Filter by tag slugs (can be multiple)
  - `min_price`: Minimum price for filtering
  - `max_price`: Maximum price for filtering
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "title": "Product Title",
        "description": "Product Description",
        "price": 99.99,
        "category": "category-slug",
        "tags": ["tag1", "tag2"]
      },
      ...
    ]
    ```

---
#### List Product Variants

- **URL**: `/api/product-variants/`
- **Method**: `GET`
- **Description**: Get a list of all product variants or filter by product
- **Query Parameters**:
  - `product`: (Optional) Filter variants by product ID
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "product": 1,
        "price": 99.99,
        "quantity": 10,
        "attributes": {}
      },
      ...
    ]
    ```

---
#### Create Product Variant

- **URL**: `/api/product-variants/`
- **Method**: `POST`
- **Description**: Create a new product variant
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "product": 1,
    "price": 99.99,
    "attributes": {}
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 1,
      "product": 1,
      "price": 99.99,
      "quantity": null,
      "attributes": {}
    }
    ```

---
#### Get Product Variant Details

- **URL**: `/api/product-variants/<int:pk>/`
- **Method**: `GET`
- **Description**: Get details of a specific product variant
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "product": 1,
      "price": 99.99,
      "quantity": 10,
      "attributes": {}
    }
    ```

---
#### Update Product Variant

- **URL**: `/api/product-variants/<int:pk>/`
- **Method**: `PUT`
- **Description**: Update a product variant
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "price": 89.99,
    "attributes": {"color": "red"}
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "product": 1,
      "price": 89.99,
      "quantity": 10,
      "attributes": {"color": "red"}
    }
    ```

---
#### Delete Product Variant

- **URL**: `/api/product-variants/<int:pk>/`
- **Method**: `DELETE`
- **Description**: Delete a product variant
- **Authentication**: Admin only
- **Success Response**:
  - **Code**: 204
  - **Content**: No content

---


### Category Management

#### List Categories

- **URL**: `/api/categories/`
- **Method**: `GET`
- **Description**: Get a list of all categories
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "parent": null,
        "title": "Category Title",
        "slug": "category-slug",
        "created_at": "2024-09-29T12:00:00Z",
        "updated_at": "2024-09-29T12:00:00Z",
        "product_attributes_schema": {},
        "variant_attributes_schema": {}
      },
      ...
    ]
    ```

---
#### Create Category

- **URL**: `/api/categories/`
- **Method**: `POST`
- **Description**: Create a new category
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "title": "New Category",
    "parent": 1,
    "product_attributes_schema": {},
    "variant_attributes_schema": {}
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 2,
      "parent": 1,
      "title": "New Category",
      "slug": "new-category",
      "created_at": "2024-09-29T12:00:00Z",
      "updated_at": "2024-09-29T12:00:00Z",
      "product_attributes_schema": {},
      "variant_attributes_schema": {}
    }
    ```

---
#### Get Category Details

- **URL**: `/api/categories/<int:pk>/`
- **Method**: `GET`
- **Description**: Get details of a specific category
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "parent": null,
      "title": "Category Title",
      "slug": "category-slug",
      "created_at": "2024-09-29T12:00:00Z",
      "updated_at": "2024-09-29T12:00:00Z",
      "product_attributes_schema": {},
      "variant_attributes_schema": {}
    }
    ```

---
#### Update Category

- **URL**: `/api/categories/<int:pk>/`
- **Method**: `PUT`
- **Description**: Update a category
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "title": "Updated Category",
    "product_attributes_schema": {"color": "string"}
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "parent": null,
      "title": "Updated Category",
      "slug": "updated-category",
      "created_at": "2024-09-29T12:00:00Z",
      "updated_at": "2024-09-29T13:00:00Z",
      "product_attributes_schema": {"color": "string"},
      "variant_attributes_schema": {}
    }
    ```

---
#### Delete Category

- **URL**: `/api/categories/<int:pk>/`
- **Method**: `DELETE`
- **Description**: Delete a category
- **Authentication**: Admin only
- **Success Response**:
  - **Code**: 204
  - **Content**: No content
---

### Inventory Management

#### Get Inventory

- **URL**: `/api/inventory/<int:product_variant_id>/`
- **Method**: `GET`
- **Description**: Get inventory details for a specific product variant
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "product_variant": "Product Variant Name",
      "quantity": 100
    }
    ```
---

#### Create Inventory

- **URL**: `/api/inventory/<int:product_variant_id>/`
- **Method**: `POST`
- **Description**: Create inventory for a product variant
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "quantity": 100
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 1,
      "product_variant": "Product Variant Name",
      "quantity": 100
    }
    ```
---

#### Update Inventory

- **URL**: `/api/inventory/<int:product_variant_id>/`
- **Method**: `PUT`
- **Description**: Update inventory for a product variant 
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "quantity": 150
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "product_variant": "Product Variant Name",
      "quantity": 150
    }
    ```
---

#### Delete Inventory

- **URL**: `/api/inventory/<int:product_variant_id>/`
- **Method**: `DELETE`
- **Description**: Delete inventory for a product variant 
- **Authentication**: Admin only
- **Success Response**:
  - **Code**: 204
  - **Content**: No content
---

### Product Review Management
#### Get Product Reviews

- **URL**: `/api/review/<int:product_id>/`
- **Method**: `GET`
- **Description**: Get all reviews for a specific product
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "product": 1,
        "user": "username",
        "rating": 5,
        "comment": "Great product!",
        "created_at": "2024-09-29T12:00:00Z"
      },
      ...
    ]
    ```
---

#### Create Product Review

- **URL**: `/api/review/<int:product_id>/`
- **Method**: `POST`
- **Description**: Create a new review for a product 
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "rating": 5,
    "comment": "Excellent product, highly recommended!"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 2,
      "product": 1,
      "user": "admin_username",
      "rating": 5,
      "comment": "Excellent product, highly recommended!",
      "created_at": "2024-09-29T13:00:00Z"
    }
    ```
---

### Cart Management

#### Get Cart

- **URL**: `/api/cart/`
- **Method**: `GET`
- **Description**: Retrieve the current user's cart
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "items": [
        {
          "id": 1,
          "product_variant": 1,
          "quantity": 2,
          "price": 1000,
          "discounted_price": 900,
          "subtotal": 1800
        }
      ],
      "total_price": 2000,
      "total_discounted_price": 1800,
      "coupon": null,
      "final_price": 1800,
      "status": "active",
      "created_at": "2024-09-29T12:00:00+0000",
      "updated_at": "2024-09-29T12:00:00+0000"
    }
    ```

---
#### Add to Cart

- **URL**: `/api/cart/`
- **Method**: `POST`
- **Description**: Add a product variant to the cart or update its quantity if it already exists
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "product_variant": 1,
    "quantity": 2
  }
  ```
- **Success Response**:
  - **Code**: 201 (Created) or 200 (OK if updating existing item)
  - **Content**: 
    ```json
    {
      "id": 1,
      "product_variant": 1,
      "quantity": 2,
      "price": 1000,
      "discounted_price": 900,
      "subtotal": 1800
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Product variant ID is required"
    }
    ```

---
#### Update Cart Item

- **URL**: `/api/cart/<int:item_id>/`
- **Method**: `PUT`
- **Description**: Update the quantity of a specific cart item
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "quantity": 3
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "product_variant": 1,
      "quantity": 3,
      "price": 1000,
      "discounted_price": 900,
      "subtotal": 2700
    }
    ```

---
#### Remove Cart Item

- **URL**: `/api/cart/<int:item_id>/`
- **Method**: `DELETE`
- **Description**: Remove a specific item from the cart
- **Authentication**: Required
- **Success Response**:
  - **Code**: 204 (No Content)

---
#### Clear Cart

- **URL**: `/api/cart/clear/`
- **Method**: `DELETE`
- **Description**: Clear all items from the cart or remove the applied coupon
- **Authentication**: Required
- **Query Params**:
  - `action`: 'clear_items' (default) or 'remove_coupon'
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Cart cleared successfully"
    }
    ```
  or
    ```json
    {
      "message": "Coupon removed successfully"
    }
    ```

---
#### Apply Coupon

- **URL**: `/api/cart/apply-coupon/`
- **Method**: `POST`
- **Description**: Apply a coupon to the cart
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "coupon_code": "SUMMER20"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Updated cart object (same as Get Cart response)
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Invalid coupon code"
    }
    ```
  or
    ```json
    {
      "error": "Coupon is not applicable to any items in your cart"
    }
    ```

---

### Notifications
#### List New Notifications
- **URL**: `/api/notifications/`
- **Method**: `GET`
- **Description**: Get all new notifications for the authenticated user since their last check
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "notification_type": "example_type",
        "message": "Example notification message",
        "is_read": false,
        "created_at": "2024-09-29T12:00:00Z",
        "content_type": "example_content_type",
        "object_id": 1
      },
      ...
    ]
    ```

---
#### Get Notifications by Timeframe
- **URL**: `/api/notifications/get_by_timeframe/`
- **Method**: `POST`
- **Description**: Get notifications for the authenticated user within a specified timeframe
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "start_date": "2024-09-01T00:00:00Z",
    "end_date": "2024-09-30T23:59:59Z"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "notification_type": "example_type",
        "message": "Example notification message",
        "is_read": false,
        "created_at": "2024-09-15T12:00:00Z",
        "content_type": "example_content_type",
        "object_id": 1
      },
      ...
    ]
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Both start_date and end_date are required."
    }
    ```

---
#### Delete Notification
- **URL**: `/api/notifications/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a specific notification for the authenticated user
- **Authentication**: Required
- **URL Params**: 
  - `id`: ID of the notification to delete
- **Success Response**:
  - **Code**: 204
- **Error Response**:
  - **Code**: 403
  - **Content**: 
    ```json
    {
      "detail": "You don't have permission to delete this notification."
    }
    ```
---

### Order Management
#### User Order List

- **URL**: `/api/orders/`
- **Method**: `GET`
- **Description**: Get all orders for the authenticated user
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "user": 1,
        "items": [
          {
            "id": 1,
            "product_variant": 1,
            "product_name": "Product Title",
            "price": "10.00",
            "quantity": 2,
            "added_at": "2024-09-29T12:00:00+0000"
          }
        ],
        "total_price": "20.00",
        "status": "PENDING",
        "created_at": "2024-09-29T12:00:00+0000",
        "updated_at": "2024-09-29T12:00:00+0000"
      }
    ]
    ```

---
#### Admin Order List

- **URL**: `/api/orders/admin/`
- **Method**: `GET`
- **Description**: Get all orders (admin only)
- **Authentication**: Required
- **Permissions**: IsAdminUser
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    [
      {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "items": [
          {
            "id": 1,
            "product_variant": 1,
            "product_name": "Product Title",
            "price": "10.00",
            "quantity": 2,
            "added_at": "2024-09-29T12:00:00+0000"
          }
        ],
        "total_price": "20.00",
        "status": "PENDING",
        "created_at": "2024-09-29T12:00:00+0000",
        "updated_at": "2024-09-29T12:00:00+0000"
      }
    ]
    ```

---
#### Admin Order Detail

- **URL**: `/api/orders/<int:pk>/`
- **Method**: `GET`
- **Description**: Get details of a specific order (admin only)
- **Authentication**: Required
- **Permissions**: IsAdminUser
- **URL Params**: 
  - `pk`: Order ID
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "user": 1,
      "user_email": "user@example.com",
      "items": [
        {
          "id": 1,
          "product_variant": 1,
          "product_name": "Product Title",
          "price": "10.00",
          "quantity": 2,
          "added_at": "2024-09-29T12:00:00+0000"
        }
      ],
      "total_price": "20.00",
      "status": "PENDING",
      "created_at": "2024-09-29T12:00:00+0000",
      "updated_at": "2024-09-29T12:00:00+0000"
    }
    ```

---
#### Update Order (Admin)

- **URL**: `/api/orders/<int:pk>/`
- **Method**: `PUT`
- **Description**: Update an existing order (admin only)
- **Authentication**: Required
- **Permissions**: IsAdminUser
- **URL Params**: 
  - `pk`: Order ID
- **Data Params**:
  ```json
  {
    "status": "COMPLETED",
    "shipping_address": 1
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "user": 1,
      "user_email": "user@example.com",
      "items": [
        {
          "id": 1,
          "product_variant": 1,
          "product_name": "Product Title",
          "price": "10.00",
          "quantity": 2,
          "added_at": "2024-09-29T12:00:00+0000"
        }
      ],
      "total_price": "20.00",
      "status": "COMPLETED",
      "created_at": "2024-09-29T12:00:00+0000",
      "updated_at": "2024-09-29T13:00:00+0000"
    }
    ```

---
#### Delete Order (Admin)

- **URL**: `/api/orders/<int:pk>/`
- **Method**: `DELETE`
- **Description**: Delete an order (admin only)
- **Authentication**: Required
- **Permissions**: IsAdminUser
- **URL Params**: 
  - `pk`: Order ID
- **Success Response**:
  - **Code**: 204
  - **Content**: No content

---
#### Refund Order (Admin)

- **URL**: `/api/orders/order-refund/admin/<int:pk>/`
- **Method**: `POST`
- **Description**: Refund an order and update inventory (admin only)
- **Authentication**: Required
- **Permissions**: IsAdminUser
- **URL Params**: 
  - `pk`: Order ID
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "id": 1,
      "user": 1,
      "user_email": "user@example.com",
      "items": [
        {
          "id": 1,
          "product_variant": 1,
          "product_name": "Product Title",
          "price": "10.00",
          "quantity": 2,
          "added_at": "2024-09-29T12:00:00+0000"
        }
      ],
      "total_price": "20.00",
      "status": "CANCELLED",
      "created_at": "2024-09-29T12:00:00+0000",
      "updated_at": "2024-09-29T14:00:00+0000"
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Cannot refund an order with PENDING status"
    }
    ```
---

### Payment Management
#### Checkout

- **URL**: `/api/payments/checkout/`
- **Method**: `POST`
- **Description**: Process checkout for the user's cart and create an order
- **Authentication**: Required
- **Data Params**:
  ```json
  {
    "shipping_address": "1"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "order": {
        "id": "1",
        "user": "1",
        "shipping_address": "1",
        "status": "pending",
        "created_at": "2024-09-29T12:00:00Z"
      },
      "payment_url": "https://zarinpal.com/payment/12345"
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Cart is empty"
    }
    ```
  OR
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Shipping address is required"
    }
    ```
  OR
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Invalid shipping address"
    }
    ```
  OR
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Payment initiation failed"
    }
    ```

---
#### Payment Verification

- **URL**: `/api/payments/verify-payment/`
- **Method**: `GET`
- **Description**: Verify the payment status after redirection from payment gateway
- **URL Params**: 
  - `Authority=[string]`
  - `Status=[string]`
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Payment was successful",
      "order_id": "1",
      "payment_id": "1"
    }
    ```
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Payment verification failed"
    }
    ```
  OR
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Payment was not successful"
    }
    ```
  OR
  - **Code**: 404
  - **Content**: 
    ```json
    {
      "error": "Order not found"
    }
    ```

---
#### Create Discount

- **URL**: `/api/discounts/`
- **Method**: `POST`
- **Description**: Create a new discount
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "description": "Summer Sale",
    "discount_percent": 20,
    "valid_from": "2024-06-01T00:00:00Z",
    "valid_to": "2024-08-31T23:59:59Z",
    "is_active": true,
    "applicable_to": [1, 2, 3],
    "applicable_categories": [1, 2]
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 1,
      "description": "Summer Sale",
      "discount_percent": 20,
      "valid_from": "2024-06-01T00:00:00Z",
      "valid_to": "2024-08-31T23:59:59Z",
      "is_active": true,
      "applicable_to": [
        {
          "id": 1,
          "name": "Product Variant 1"
        },
        {
          "id": 2,
          "name": "Product Variant 2"
        },
        {
          "id": 3,
          "name": "Product Variant 3"
        }
      ],
      "applicable_categories": [
        {
          "id": 1,
          "name": "Category 1"
        },
        {
          "id": 2,
          "name": "Category 2"
        }
      ]
    }
    ```

---
#### Create Coupon

- **URL**: `/api/coupons/`
- **Method**: `POST`
- **Description**: Create a new coupon
- **Authentication**: Admin only
- **Data Params**:
  ```json
  {
    "code": "SUMMER2024",
    "discount_percent": 15,
    "valid_from": "2024-06-01T00:00:00Z",
    "valid_to": "2024-08-31T23:59:59Z",
    "active": true,
    "usage_limit": 100,
    "applicable_to": [1, 2, 3],
    "applicable_categories": [1, 2]
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "id": 1,
      "code": "SUMMER2024",
      "discount_percent": 15,
      "valid_from": "2024-06-01T00:00:00Z",
      "valid_to": "2024-08-31T23:59:59Z",
      "active": true,
      "usage_limit": 100,
      "usage_count": 0,
      "applicable_to": [
        {
          "id": 1,
          "name": "Product Variant 1"
        },
        {
          "id": 2,
          "name": "Product Variant 2"
        },
        {
          "id": 3,
          "name": "Product Variant 3"
        }
      ],
      "applicable_categories": [
        {
          "id": 1,
          "name": "Category 1"
        },
        {
          "id": 2,
          "name": "Category 2"
        }
      ]
    }
    ```

---
#### Delete Coupon

- **URL**: `/api/coupons/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a coupon
- **Authentication**: Admin only
- **URL Params**: 
  - `id=[integer]`
- **Success Response**:
  - **Code**: 204
  - **Content**: No content
- **Error Response**:
  - **Code**: 400
  - **Content**: 
    ```json
    {
      "error": "Cannot delete a coupon that has been used."
    }
    ```