
POST    /users
GET     /users/{id}/credentials
POST    /users/{id}/orders
GET     /products/sales

Tables:
users
    email -> PK
    name
orders
    id -> PK
    user_email -> FK
    total
    timestamp
order
    order_id -> PK FK
    product_id -> PK FK
    quantity
    date_created
products
    id -> PK
    name
    unitary_price
