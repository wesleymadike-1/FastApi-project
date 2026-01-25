================================================================================================================



***# Connecting FastAPI to a Relational Database (PostgreSQL) with SQLAlchemy and Alembic***

This guide explains how to connect FastAPI to a PostgreSQL database using SQLAlchemy for ORM and Alembic for database migrations. It covers environment setup, configuration, model definition, and migration tracking.

## 1. Create a .env File for Database URL
Create a .env file in your project root to securely store your database connection URL. Example:
N.B ((**I'M USING POSTGREsql**))

```
DATABASE_URL=database+ database_driver://username:password@localhost:5432/dbname
```
DB_DRIVER=psycopg2
DB_USER=**********
DB_PASSWORD=************
DB_HOST=localhost or the IP address of your db provider e.g Azure or AWS
DB_PORT=5432 or the one from your provider
DB_NAME=*************

This keeps sensitive credentials out of your codebase and allows easy environment switching.

## 2. Create a Config File Using Pydantic's BaseSettings
Create `config.py` in your `app/` directory. Use Pydantic's `BaseSettings` to load environment variables in a type-safe, validated way. This approach centralizes configuration, supports environment switching, and avoids hardcoding sensitive values.

Note : PYDENTIC version2 uses "from pydantic_settings import BaseSettings"

**Why use Pydantic's BaseSettings?**
- Automatically loads and validates environment variables from `.env`.
- Ensures type safety and clear error messages for missing or invalid config.
- Keeps configuration logic clean, maintainable, and secure.
- Supports easy overrides for testing and deployment.

## 3. Connect PostgreSQL with FastAPI in database.py
Create `database.py` in your app/ directory. Use the URL from config.py to set up SQLAlchemy:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Why use get_db?**
- It provides a database session for each request, ensuring proper resource management and thread safety.
- It allows dependency injection in FastAPI routes for clean, testable code.

## 4. Define Database Models in db_models.py
Create `db_models.py` in your app/ directory. Import Base from database.py and define your tables:

```python
from .database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

## 5. Install and Initialize Alembic
Install Alembic:
```
pip install alembic
```

Initialize Alembic:
```
alembic init alembic
```

Configure Alembic to track changes in your models:
- For detailed Alembic configuration, see the README in the alembic folder.

Alembic will now detect changes in your models and generate migration scripts to keep your database schema up to date.

---

By following these steps, you ensure a robust, maintainable, and secure integration between FastAPI and PostgreSQL, with automated schema management using Alembic.

================================================================================================================

## 6. 🔐 User Login Process with JWT Authentication

This section explains the professional login process implemented in your FastAPI project, including token generation and protecting routes using JWT (JSON Web Tokens).

### 🚀 Login Workflow

1. **User Submits Credentials:**  
    The user sends their username and password to the `/login` endpoint via a POST request.

2. **Credentials Verification:**  
    The backend verifies the credentials against the stored user data (typically hashed passwords in the database).

3. **JWT Token Generation:**  
    Upon successful authentication, the server generates a JWT access token containing user information and an expiration time.

4. **Token Response:**  
    The JWT token is returned to the client, usually in the response body as JSON.

5. **Client Stores Token:**  
    The client (frontend or API consumer) stores the token securely (e.g., in memory or secure storage).

### 🗺️ Login Process Diagram

```mermaid
sequenceDiagram
    participant User
    participant FastAPI
    participant Database

    User->>FastAPI: POST /login (username, password)
    FastAPI->>Database: Verify credentials
    Database-->>FastAPI: User data (hashed password)
    alt Credentials valid
        FastAPI->>FastAPI: Generate JWT token
        FastAPI-->>User: Return JWT token
    else Invalid credentials
        FastAPI-->>User: 401 Unauthorized
    end

    User->>FastAPI: Request protected route (Authorization: Bearer <token>)
    FastAPI->>FastAPI: Validate JWT token
    alt Token valid
        FastAPI-->>User: Grant access
    else Invalid/expired token
        FastAPI-->>User: 401 Unauthorized
    end
```

### 🛡️ Protecting Routes

- **Authorization Header:**  
  For protected endpoints, the client includes the JWT token in the `Authorization` header as `Bearer <token>`.

- **Dependency Injection:**  
  FastAPI uses dependency injection to extract and validate the token for each protected route. If the token is valid and not expired, the request proceeds; otherwise, a 401 Unauthorized error is returned.

- **Example Protected Route:**
     ```python
     from fastapi import Depends, HTTPException, status
     from fastapi.security import OAuth2PasswordBearer
     from jose import JWTError, jwt

     oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

     def get_current_user(token: str = Depends(oauth2_scheme)):
          try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                     raise credentials_exception
                # Fetch user from DB here
          except JWTError:
                raise HTTPException(
                     status_code=status.HTTP_401_UNAUTHORIZED,
                     detail="Could not validate credentials",
                     headers={"WWW-Authenticate": "Bearer"},
                )
          return user
     ```

- **Usage in Routes:**
     ```python
     @app.get("/protected-route")
     async def protected_route(current_user: User = Depends(get_current_user)):
          return {"message": f"Hello, {current_user.name}! 🎉"}
     ```

### 📝 Summary

- Users authenticate via `/login` and receive a JWT token.
- The token is required for accessing protected routes.
- FastAPI ensures only authenticated users can access sensitive endpoints.

✨ This approach provides a secure, scalable, and modern authentication flow for your FastAPI application!  

## 7. Using Environment Variables in Postman

When testing your API with Postman, you can manage sensitive information securely and efficiently by using environment variables:

- **Add the API URL as an Environment Variable in Postman:**  
    Create a new environment in Postman and add a variable (e.g., `base_url`) with your API's URL as its value. Use `{{base_url}}` in your request URLs. This allows you to easily switch between different environments (development, staging, production) by changing the variable value instead of updating each request manually.

- **Set the Token as a Variable in Postman:**  
    Add another variable (e.g., `token`) to your Postman environment and store your authentication token there. Reference it in your request headers as `Bearer {{token}}`. This makes it easy to update the token when it changes and keeps your requests organized and secure.

Using Postman environment variables for your API URL and token streamlines your workflow and helps protect sensitive data.


## 7. Database Relationship

- **user.py**: Handles user registration, authentication, and user-related operations.
- **post.py**: Manages creation, retrieval, updating, and deletion of posts by users.
- **like.py**: Allows users to like posts, tracking which user liked which post.
- **auth.py**: Manages authentication logic, including login and token generation.


- **User** and **Post**: One-to-Many  
    Each user can create multiple posts, but each post is authored by a single user.
- **User** and **Like**: One-to-Many  
    Each user can like multiple posts, but each like is associated with a single user.
- **Post** and **Like**: One-to-Many  
    Each post can be liked by multiple users, but each like is associated with a single post.
- **Like** acts as a join table to implement a Many-to-Many relationship between **User** and **Post**.

### Mermaid Entity Relationship Diagram

```mermaid
erDiagram
        USER ||--o{ POST : "writes"
        USER ||--o{ LIKE : "gives"
        POST ||--o{ LIKE : "receives"
```

### Flow Diagrams

#### User Registration and Post Creation

```mermaid
sequenceDiagram
        participant User
        participant FastAPI
        participant Database

        User->>FastAPI: Register (username, password)
        FastAPI->>Database: Create User
        Database-->>FastAPI: User created
        FastAPI-->>User: Registration success

        User->>FastAPI: Create Post (content)
        FastAPI->>Database: Insert Post (user_id FK)
        Database-->>FastAPI: Post created
        FastAPI-->>User: Post creation success
```

#### Liking a Post

```mermaid
sequenceDiagram
        participant User
        participant FastAPI
        participant Database

        User->>FastAPI: Like Post (post_id)
        FastAPI->>Database: Insert Like (user_id, post_id)
        Database-->>FastAPI: Like recorded
        FastAPI-->>User: Like success
```

