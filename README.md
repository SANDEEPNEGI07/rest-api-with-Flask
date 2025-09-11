# Flask REST API

A RESTful API built with Flask, SQLAlchemy, Alembic, and Redis.

## Features

- User, Store, Item, and Tag resources
- JWT authentication and authorization
- Database migrations with Alembic
- Redis integration for caching or background tasks
- Docker support for easy deployment

---

This project is a RESTful API built with Flask, designed for managing users, stores, items, and tags. It features JWT authentication, database migrations with Alembic, and Redis integration for caching or background tasks. The API is containerized with Docker for easy deployment and scalability.

---
## Live Demo

### Checkout the API Documentation: [Docs](https://rest-api-flask-project-u9x9.onrender.com/swagger-ui)

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional, for containerization)
- Redis (can be run via Docker)

### Installation

```bash
git clone https://github.com/SANDEEPNEGI07/rest-api-with-Flask.git
cd rest-api-with-Flask
python -m venv .venv
# On Linux/Mac
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

---

## Running Locally

1. Start Redis (if not already running):

    ```bash
    docker run -d -p 6379:6379 redis
    ```

2. Apply database migrations:

    ```bash
    flask db upgrade
    ```

3. Start the Flask server:

    ```bash
    flask run
    ```

---

## Running with Docker (including Redis)

1. Build your Flask app image:

    ```bash
    docker build -t <docker image name> .
    ```

2. Start Redis in a separate container:

    ```bash
    rq worker -u <insert your Redis url here> name_of_redis_db
    ```

3. Run your Flask app container, linking it to Redis:

    ```bash
    docker run -w /app <image name> sh -c "rq worker -u <insert your Redis url here> emails"
    ```
