
POST    /users
GET     /users/{id}/credentials
POST    /users/{id}/orders
GET     /products/sales

Tables:
users
    email -> PK
    name
order
    id -> PK
    user_email -> FK
    total
    date_created
ordercontents
    order_id -> PK FK
    product_id -> PK FK
    quantity
    unitary_price
products
    id -> PK
    name
