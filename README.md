# inventory_service

# uvicorn main:app --reload

1. Create a Product
Endpoint:


POST /products/
Request Payload:

{
  "name": "iPhone 15",
  "quantity": 50
}
Response:

{
  "id": 1,
  "name": "iPhone 15",
  "quantity": 50
}
2. Get Product Details
Endpoint:

GET /products/{product_id}
Example:


GET /products/1
Response:


{
  "id": 1,
  "name": "iPhone 15",
  "quantity": 50
}
Error (if not found):

{
  "detail": "Product not found"
}
3. Update Product Stock (Increment or Decrement)
Endpoint:


PUT /products/{product_id}/stock?delta=<int>
Example 1: Decrease stock by 5

PUT /products/1/stock?delta=-5
Response:


{
  "product_id": 1,
  "new_quantity": 45
}
Example 2: Increase stock by 20

PUT /products/1/stock?delta=20
Response:


{
  "product_id": 1,
  "new_quantity": 65
}
Error (if insufficient stock):


{
  "detail": "Insufficient stock"
}
4. List All Products (Optional Extension)
Endpoint:

GET /products/
Response:


[
  {
    "id": 1,
    "name": "iPhone 15",
    "quantity": 65
  },
  {
    "id": 2,
    "name": "MacBook Air",
    "quantity": 30
  }
]