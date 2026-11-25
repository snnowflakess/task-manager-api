# Task Manager API

A backend task management application built using **FastAPI, Python, PostgreSQL, SQLAlchemy, JWT Authentication and Docker**.

The application provides secure REST APIs for managing users, tasks and comments. It also supports role-based access control, Google OAuth login and pagination.

## Features

- User registration and login
- Secure password hashing using Argon2
- JWT-based authentication
- Role-based access control (USER and ADMIN)
- Google OAuth 2.0 login
- Task CRUD operations
- Comment CRUD operations
- User profile management
- Task ownership and authorization checks
- Pagination using `skip` and `limit`
- PostgreSQL database integration
- Docker containerization
- Swagger API documentation
- Automated unit testing with pytest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Programming language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM and database operations |
| PostgreSQL 16 | Relational database |
| Pydantic | Data validation |
| PyJWT | JWT authentication |
| Argon2 | Password hashing |
| Authlib | Google OAuth |
| Docker | Containerization |
| Docker Compose | Container management |
| Pytest | Unit testing |

## Project Structure

```text
task-manager-api/
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── conftest.py
│
├── tests/
│   └── test_main.py
│
└── README.md
```

## API Endpoints

Base URL: `http://localhost:8000`

### 1. Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register a new user |
| POST | `/login` | Login and obtain JWT token |
| GET | `/users/me` | Get authenticated user profile |
| GET | `/auth/google` | Start Google OAuth login |
| GET | `/auth/google/callback` | Handle Google OAuth callback |

### 2. Task Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve user's tasks |
| GET | `/tasks/{task_id}` | Retrieve a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

**Pagination example:**

```http
GET /tasks?skip=0&limit=10
```

- `skip`: Number of records to skip (default: 0).
- `limit`: Maximum records to return (default: 10, maximum: 100).

### 3. Comment Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks/{task_id}/comments` | Add a comment |
| GET | `/tasks/{task_id}/comments` | Get task comments |
| PUT | `/comments/{comment_id}` | Update a comment |
| DELETE | `/comments/{comment_id}` | Delete a comment |

### 4. User Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | Retrieve user's profile |
| GET | `/users/{user_id}` | Get a specific user |
| PUT | `/users/{user_id}` | Update user profile |
| DELETE | `/users/{user_id}` | Delete user account |

### 5. Administrator

| Method | Endpoint | Access |
|---|---|---|
| GET | `/admin/users` | ADMIN only |

## Authentication and Authorization

The application uses JWT (JSON Web Tokens) for authentication.

1. Register an account using `POST /users`.
2. Login using `POST /login`.
3. Receive an access token.
4. Include the token in protected API requests:

http
Authorization: Bearer YOUR_ACCESS_TOKEN


Passwords are hashed using Argon2 before being stored in the database.

### Role-Based Access Control

The application supports two roles:

- **USER:** Can manage their own profile, tasks and comments.
- **ADMIN:** Has access to administrator-only endpoints, including `/admin/users`.

Users cannot access or modify resources belonging to other users unless explicitly authorized.

### Google OAuth

Google login is implemented using Authlib and OAuth 2.0.

The user starts authentication through:

```http
GET /auth/google
```

Google redirects to the configured callback endpoint after authentication.

## Database Architecture

PostgreSQL is used for persistent data storage.

SQLAlchemy manages database models and queries.

Main database entities:

- **User:** Stores user details, password hash and role.
- **Task:** Stores task title, description, status, priority and due date.
- **Comment:** Stores comments associated with tasks and users.

The application uses SQLAlchemy relationships and foreign keys to maintain data associations.

## Architecture

          Client / Postman
                 |
                 v
           FastAPI Server
                 |
        ---------------------
        |         |         |
      Auth     Routes    Validation
        |         |         |
        ---------------------
                 |
                 v
             SQLAlchemy
                 |
                 v
             PostgreSQL


For Docker deployment, the FastAPI application runs inside a container and connects to PostgreSQL through the configured database URL.

## Installation and Setup

### Prerequisites

- Python 3.14
- PostgreSQL 16
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd task-manager-api
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Configure the following variables:

```env
DATABASE_URL=your_postgresql_connection_url
DATABASE_URL_DOCKER=your_docker_database_connection_url

SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

SESSION_SECRET=your_session_secret
```

Use your own database credentials and generated secret values. Never commit `.env` to GitHub.

### 5. Run the application locally

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://localhost:8000`

## Docker Setup

Build the Docker image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs app
```

Stop the application:

```bash
docker compose down
```

**Database configuration:** The current Compose configuration runs the FastAPI application in Docker and connects to the existing PostgreSQL container through `host.docker.internal:5433`. The existing PostgreSQL data volume is preserved.

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Unit Testing

The project uses pytest and an isolated SQLite test database.

Run the test suite:

```bash
python -m pytest -v
```

### Implemented Tests

1. Login functionality
2. Access without authentication token
3. Task creation
4. Preventing users from accessing another user's task
5. Task pagination

**Latest test result:** 5 passed.

## Postman Collection

The Postman collection will contain API requests for:

- User registration and login
- Task CRUD operations
- Comment CRUD operations
- User management
- Administrator access
- JWT-protected endpoints
- Pagination

Import the collection from the repository's `postman/` directory once added.

## Security Considerations

- Passwords are never stored in plain text.
- JWT tokens protect authenticated endpoints.
- Role-based permissions restrict administrator operations.
- Users can only manage their authorized resources.
- Sensitive environment variables are excluded from version control.

## Future Improvements

- Additional unit and integration tests
- Automated CI/CD pipeline
- API rate limiting
- Production deployment
- Improved logging and monitoring

## Author

Developed as a backend development project using FastAPI and PostgreSQL.
