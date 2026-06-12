# Micro ERP AI — API Documentation

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

Authentication:

Protected endpoints require:

```text
Bearer Token
```

Add token in request headers:

```text
Authorization: Bearer <jwt_token>
```

---

# Authentication

## Register User

### Endpoint

```http
POST /auth/register
```

### Request Body

```json
{
  "username": "admin",
  "email": "admin@erp.com",
  "password": "123456",
  "role": "admin"
}
```

### Response

```json
{
  "message": "User created successfully"
}
```

---

## Login User

### Endpoint

```http
POST /auth/login
```

### Request Body

```json
{
  "email": "admin@erp.com",
  "password": "123456"
}
```

### Response

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "role": "admin"
}
```

---

# Products

## Get All Products

### Endpoint

```http
GET /products
```

### Access

Authenticated users

### Response

```json
[
  {
    "id": 1,
    "name": "Rice",
    "sku": "RC001",
    "category": "Food",
    "quantity": 100,
    "price": 5,
    "reorder_level": 10
  }
]
```

---

## Get Product By ID

### Endpoint

```http
GET /products/{product_id}
```

### Example

```http
GET /products/1
```

---

## Create Product

### Endpoint

```http
POST /products
```

### Access

Admin only

### Request Body

```json
{
  "name": "Rice",
  "sku": "RC001",
  "category": "Food",
  "quantity": 100,
  "price": 5,
  "reorder_level": 10
}
```

### Response

```json
{
  "id": 1,
  "name": "Rice",
  "sku": "RC001"
}
```

---

## Update Product

### Endpoint

```http
PUT /products/{product_id}
```

### Access

Admin only

### Example Body

```json
{
  "quantity": 150,
  "price": 7
}
```

---

## Delete Product

### Endpoint

```http
DELETE /products/{product_id}
```

### Access

Admin only

### Response

```json
{
  "message": "Product deleted"
}
```

---

## Low Stock Products

### Endpoint

```http
GET /products/low-stock
```

### Response

```json
[
  {
    "id": 1,
    "name": "Milk",
    "quantity": 2,
    "reorder_level": 10
  }
]
```

---

# Customers

## Get All Customers

### Endpoint

```http
GET /customers
```

---

## Get Customer By ID

### Endpoint

```http
GET /customers/{customer_id}
```

---

## Create Customer

### Endpoint

```http
POST /customers
```

### Request Body

```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "email": "john@email.com",
  "address": "New York",
  "credit_balance": 0
}
```

---

## Update Customer

### Endpoint

```http
PUT /customers/{customer_id}
```

### Access

Admin only

### Example Body

```json
{
  "phone": "9999999999",
  "credit_balance": 200
}
```

---

## Delete Customer

### Endpoint

```http
DELETE /customers/{customer_id}
```

### Access

Admin only

### Response

```json
{
  "message": "Customer deleted"
}
```

---

# Sales

## Create Sale

### Endpoint

```http
POST /sales
```

### Request Body

```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

### Response

```json
{
  "sale_id": 1,
  "total_amount": 50,
  "message": "Sale completed"
}
```

---

## Get All Sales

### Endpoint

```http
GET /sales
```

---

## Get Sale By ID

### Endpoint

```http
GET /sales/{sale_id}
```

---

# Reports

## Revenue Report

### Endpoint

```http
GET /reports/revenue
```

### Response

```json
{
  "total_revenue": 2500
}
```

---

## Low Stock Report

### Endpoint

```http
GET /reports/low-stock
```

### Response

```json
[
  {
    "id": 2,
    "name": "Milk",
    "quantity": 2
  }
]
```

---

# Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

# Roles

## Admin

Can:

- Manage products
- Manage customers
- View reports
- Create sales
- Delete records

## Staff

Can:

- View products
- Create customers
- Create sales

Cannot:

- Delete products
- Edit admin-only resources

---

# Notes

- JWT tokens expire after 60 minutes.
- All protected routes require Bearer authentication.
- SQLite is used as the local database.
- APIs are designed for Android integration and Uno Q deployment.
