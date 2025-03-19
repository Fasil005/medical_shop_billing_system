# Project Setup Instructions

## 1. Building and Running Docker Containers

To build and run the project using Docker, follow these steps:

```sh
# Build the Docker containers
docker-compose build

# Start the containers
docker-compose up
```

To run in detached mode (background):

```sh
docker-compose up -d
```

To stop the containers:

```sh
docker-compose down
```

## 2. Running Django Fixtures

To load initial data into the database using Django fixtures, use the following command:

```sh
docker-compose exec web python manage.py loaddata <fixture_name>.json
```

Replace `<fixture_name>` with the actual fixture file name located in your Django project.

## 3. Using the Postman Collection

A Postman collection is available for testing the API endpoints. You can import it into Postman and use it to interact with the API.

## 4. OpenAPI Documentation

TThe OpenAPI documentation is available at the following URLs on localhost:

Schema: http://localhost:8000/api/schema/

Swagger UI: http://localhost:8000/api/docs/

Redoc UI: http://localhost:8000/api/redoc/

These endpoints provide detailed API documentation, including request and response formats.

## 5. Setting Up Environment Variables

A sample environment file `.env_sample` is provided in the project root. Copy this file and rename it to `.env`:

Then, update the `.env` file with the appropriate values according to your system configuration.

