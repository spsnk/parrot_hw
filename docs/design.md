# Parrot Challenge Initial Design

## Endpoints

- POST /users
- GET /users/{id}
- GET /users/{id}/credentials
- POST /users/{id}/orders
- GET /products/sales

## Tables

- users
  - email (str) -> PK
  - name (str)
- orders
  - id (str:uuid) -> PK
  - user_email (str) -> FK users.email
  - total (numeric(10,2))
  - date_created(timestamp with time zone) INDEX
- products
  - id (str:uuid) -> PK
  - name (str)
- ordercontents
  - order_id (str:uuid) -> PK FK orders.id
  - product_id (str:uuid) -> PK FK products.id
  - quantity (integer)
  - unitary_price (numeric(10,2))
