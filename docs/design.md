## Endpoints

- POST /users
- GET /users/{id}/credentials
- POST /users/{id}/orders
- GET /products/sales

## Tables

- users
  - email (str) -> PK
  - name (str)
- order
  - id (str:uuid) -> PK
  - user_email (str) -> FK users.email
  - total (numeric(10,2))
  - date_created(timestamp with time zone)
- products
  - id (str:uuid) -> PK
  - name (str)
- ordercontents
  - order_id (str:uuid) -> PK FK order.id
  - product_id (str:uuid) -> PK FK product.id
  - quantity (integer)
  - unitary_price (numeric(10,2))
