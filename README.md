# Parrot Challenge

By Salvador Paz

## Endpoints

- Create User
  - POST /api/v1/users
- Get User information (Requires authentication)
  - GET /api/va/users/{user_email}
- Get user token (JWT authentication, token expires after 10 minutes by default, can be changed on env file)
  - GET /api/v1/users/{user_email}/credentials
- Create Order (Requires authentication)
  - POST /api/v1/users/{user_email}/orders
- Reports
  - GET /api/v1/products/sales?start={ISO date}&end={ISO date}

For more information check the [documentation](/docs). There's also interactive API documentation using Swagger UI on the resulting deployment, on the root address.

## Project Structure

This project is divided in 3 containers:

- Application Container - python/flask/gunicorn (apiv1)
  - Contains application code.
  - For development uses Flask development server, for production uses Gunicorn.
- Database Container - postgresql (db)
  - Contains the database service, initialization and seed scripts.
  - Has persistent volume for data.
- Reverse Proxy Container - Nginx (web)
  - Contains configuration that host a particular api version on its own route (/api/v1/, etc).
  - Hosts interactive API documentation on root route (e.g. <http://localhost> ).

## Development Environment

Requirements:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

Execute in project root directory:

```bash
docker-compose up --build
```

Wait for build and initialization of containers:

```bash
[+] Building 1.9s (26/26) FINISHED
...
[+] Running 5/5
 - Network parrot_default         Created
 - Volume "parrot_database-data"  Created
 - Container parrot_db_1          Created
 - Container parrot_apiv1_1       Created
 - Container parrot_web_1         Created
Attaching to apiv1_1, db_1, web_1
...
apiv1_1  | Postgres is up - starting server
apiv1_1  | > python manage.py run -h 0.0.0.0
apiv1_1  |  * Serving Flask app 'api/__init__.py' (lazy loading)
apiv1_1  |  * Environment: development
apiv1_1  |  * Debug mode: on
apiv1_1  |  * Running on all addresses.
apiv1_1  |    WARNING: This is a development server. Do not use it in a production deployment.
apiv1_1  |  * Running on http://192.168.128.3:5000/ (Press CTRL+C to quit)
```

When above message is shown application is ready for local development, any changes on `apiv1` folder will be automatically reloaded, open up your favorite editor and load up the project directory to make changes.

### Remove Development Environment

Execute command:

```bash
docker-compose down -v
```

`-v` flag removes persistent database volume as well.

## Production Environment

Requirements:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

Execute in project root directory:

```bash
docker-compose -f docker-compose.prod.yml up --build
```

Similarly to development environment, wait for containers to build and initialize.

Production server will copy all the application files at container creation, meaning it wont reload any change of the files when they're modified.

### Remove Production Environment

Execute command:

```bash
docker-compose -f docker-compose.prod.yml down -v
```

## Test API

Included is a Postman collection that you can load to test (automates token use), the same endpoint information is described in the following with curl commands:

Create new user:

```bash
$ curl --location --request POST 'localhost/api/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "salvador.paz.santos@gmail.com",
    "name": "Salvador Paz Santos"
}'
{"email": "salvador.paz.santos@gmail.com","name": "Salvador Paz Santos"}
```

Get user credentials (jwt):

```bash
$ curl --location --request GET 'localhost/api/v1/users/salvador.paz.santos@gmail.com/credentials'
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhbHZhZG9yLnBhei5zYW50b3NAZ21haWwuY29tIiwiZXhwaXJlcyI6MTYzOTY0MzQwMi41MjU4Mzd9.koCVomBKT1zZESz88niYJuI87WX6LNR2tz37mHEwGNw"}
```

Create order (jwt authentication required):

```bash
$ curl --location --request POST 'localhost/api/v1/users/salvador.paz.santos@gmail.com/orders' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNhbHZhZG9yLnBhei5zYW50b3NAZ21haWwuY29tIiwiZXhwaXJlcyI6MTYzOTY0MzQwMi41MjU4Mzd9.koCVomBKT1zZESz88niYJuI87WX6LNR2tz37mHEwGNw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "products":[
        {
            "name": "Donut",
            "quantity": 5,
            "unitary_price": 2.50
        }
    ]
}'
{"products": [{"name": "Donut","quantity": 5,"unitary_price": 2.5}],"user_email": "salvador.paz.santos@gmail.com","order_id": "9b1e5690-4599-4b40-9c8f-f84fd7a4a81c","total": 12.5}
```

Get reports for all orders:

```bash
$ curl --location --request GET 'localhost/api/v1/products/sales'
{"range": "all","products": [{"name": "donut","units": 5,"revenue": 12.5}]}
```

Get reports for start date to `now`:

```bash
$ curl --location --request GET 'localhost/api/v1/products/sales?start=2021-12-10'
{"range": {"start": "2021-12-10","end": "2021-12-16 08:04:59"},"products": [{"name": "donut","units": 5,"revenue": 12.5}]}
```

Get reports between two dates:

```bash
$ curl --location --request GET 'localhost/api/v1/products/sales?start=2021-12-01&end=2021-12-10'
{"range": {"start": "2021-12-01","end": "2021-12-10"},"products": []}
```
