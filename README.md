```text
 _    _             _              ___  ___           _ _ _         
| |  | |           | |             |  \/  |          | (_) |        
| |  | | ___  ___  | | ___ _   _   | .  . | __ _  __| |_| | _____  
| |/\| |/ _ \/ __| | |/ _ \ | | |  | |\/| |/ _` |/ _` | | |/ / _ \ 
\  /\  /  __/\__ \ | |  __/ |_| |  | |  | | (_| | (_| | |   <  __/ 
 \/  \/ \___||___/ |_|\___|\__, |  \_|  |_/\__,_|\__,_|_|_|\_\___| 
                            __/ |
```

# FastAPI, PostgreSQL, and Alembic Integration 🚀🐘

A professional, production-ready implementation of a REST API using **FastAPI**, **PostgreSQL** for data persistence, **SQLAlchemy** for ORM, and **Alembic** for schema migrations. This project also features secure **JWT-based authentication**. 🔐

---

## 🚀 Quick Start Guide

### 🛠️ Environment Setup

Clone the repository and set up your development environment:

#### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

#### 2. Configure Git (optional)

```bash
git config --global core.editor "code --wait"
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 4. Install dependencies

```bash
pip install -r requirements.txt
```

#### 5. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

==========================================================================================

## 1. 🗄️ Create a .env File for Database URL
Create a `.env` file in your project root to securely store your database connection URL. Example:
N.B (**I'M USING POSTGRESQL** 🐘)

```
DATABASE_URL=database+database_driver://username:password@localhost:5432/dbname
```
- `DB_DRIVER=psycopg2`
- `DB_USER=your_username`
- `DB_PASSWORD=your_password`
- `DB_HOST=localhost`  <!-- or the IP address of your DB provider (e.g., Azure or AWS) -->
- `DB_PORT=5432`       <!-- or the one from your provider -->
- `DB_NAME=your_dbname`

- `ALGORITHM=<your_algorithm>`  
    *(e.g., "HS256" — loaded as `ALGORITHM = settings.ALGORITHM`)*

- `SECRET_KEY=<your_secret_key>`  
    *This is your unique signature for signing tokens. It should be kept secret!  
    Generate a strong key with: `openssl rand -hex 32` or `openssl rand -hex 64`.*
- `ACCESS_TOKEN_EXPIRE_MINUTES=<minutes>`  
    *(e.g., "30" — controls token expiration time)*
This keeps sensitive credentials out of your codebase and allows easy environment switching.

## 2. ⚙️ Create a Config File Using Pydantic's BaseSettings
Create `config.py` in your `app/` directory. Use Pydantic's `BaseSettings` to load environment variables in a type-safe, validated way. This approach centralizes configuration, supports environment switching, and avoids hardcoding sensitive values.

Note: PYDANTIC version 2 uses `from pydantic_settings import BaseSettings`

**Why use Pydantic's BaseSettings?**
- Automatically loads and validates environment variables from `.env`.
- Ensures type safety and clear error messages for missing or invalid config.
- Keeps configuration logic clean, maintainable, and secure.
- Supports easy overrides for testing and deployment.

## 3. 🔗 Connect PostgreSQL with FastAPI in `database.py`
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

## 4. 📝 Define Database Models in `db_models.py`
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

## 5. 🛠️ Alembic Installation & Initialization

Install Alembic (for database migrations):

```bash
pip install alembic
```
*Installs Alembic into your virtual environment.*

Initialize Alembic in your project:

```bash
alembic init alembic
```
*Creates the `alembic/` directory and default migration environment.*

Edit `alembic.ini` and set your database URL:

```bash
# In alembic.ini, set:
sqlalchemy.url = <your-database-url>
```
*Points Alembic to your database. You can also configure this to read from your `.env` via your config.*

Generate a new migration after changing models:

```bash
alembic revision --autogenerate -m "Describe your migration"
```
*Creates a migration script based on model changes.*

Apply migrations to update your database schema:

```bash
alembic upgrade head
```
*Applies the latest migrations to your database.*

Check current migration status:

```bash
alembic current
```
*Shows the current migration version applied to the database.*

Downgrade to a previous migration if needed:

```bash
alembic downgrade -1
```
*Rolls back the last migration.*

**Summary:**  
Alembic helps you version and manage your database schema changes safely and efficiently. Always review autogenerated migration scripts before applying them.

Configure Alembic to track changes in your models:
- For detailed Alembic configuration, see the README in the alembic folder.

Alembic will now detect changes in your models and generate migration scripts to keep your database schema up to date.

---

By following these steps, you ensure a robust, maintainable, and secure integration between FastAPI and PostgreSQL, with automated schema management using Alembic. 🎉

========================================================================================

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

## 7. 🧪 Using Environment Variables in Postman

When testing your API with Postman, you can manage sensitive information securely and efficiently by using environment variables:

- **Add the API URL as an Environment Variable in Postman:**  
    Create a new environment in Postman and add a variable (e.g., `base_url`) with your API's URL as its value. Use `{{base_url}}` in your request URLs. This allows you to easily switch between different environments (development, staging, production) by changing the variable value instead of updating each request manually.

- **Set the Token as a Variable in Postman:**  
    Add another variable (e.g., `token`) to your Postman environment and store your authentication token there. Reference it in your request headers as `Bearer {{token}}`. This makes it easy to update the token when it changes and keeps your requests organized and secure.

Using Postman environment variables for your API URL and token streamlines your workflow and helps protect sensitive data. 🔒

## 8. 🗃️ Database Relationship

- **user.py**: Handles user registration, authentication, and user-related operations.
- **post.py**: Manages creation, retrieval, updating, and deletion of posts by users.
- **like.py**: Allows users to like posts, tracking which user liked which post.
- **auth.py**: Manages authentication logic, including login and token generation.

- **USER** and **POST**: One-to-Many  
    Each USER can create multiple POSTs, but each POST is authored by a single USER.
- **USER** and **LIKE**: One-to-Many  
    Each USER can like multiple POSTs, but each LIKE is associated with a single USER.
- **POST** and **LIKE**: One-to-Many  
    Each POST can be liked by multiple USERs, but each LIKE is associated with a single POST.
- **LIKE** acts as a join table to implement a Many-to-Many relationship between **USER** and **POST**.

### Mermaid Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ POST : "writes"
    USER ||--o{ LIKE : "likes"
    POST ||--o{ LIKE : "liked by"

    USER {
        int id PK
        string username
        string email
        string password
        datetime created_at
    }
    POST {
        int id PK
        string title
        string content
        int owner_id FK
        datetime created_at
    }
    LIKE {
        int user_id FK
        int post_id FK
        datetime created_at
    }
```

### Flow Diagrams

#### User Registration and Post Creation

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant A as FastAPI Engine
    participant D as PostgreSQL DB

    Note over U, D: Registration Phase
    U->>A: POST /users (credentials)
    A->>A: Hash Password (Bcrypt)
    A->>D: Persist User Record
    D-->>A: Record Created
    A-->>U: 201 Created (User Profile)

    Note over U, D: Content Creation Phase
    U->>A: POST /posts (JWT + Content)
    A->>A: Validate JWT Token
    A->>D: Save Post (Linked to user_id)
    D-->>A: Post Saved
    A-->>U: 201 Created (Post ID)
```

#### Liking a Post

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant A as FastAPI Engine
    participant D as PostgreSQL DB

    U->>A: POST /likes/{post_id} (JWT)
    A->>A: Verify User Identity
    A->>D: Check if Post exists
    D-->>A: Post Validated
    A->>D: Create Like entry
    D-->>A: Entry Saved
    A-->>U: 201 Success (Post Liked ❤️)
```

---
=========================================================================
## 🤝 Contributing & Support

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**! 🚀

1. **Fork** the Project 🍴
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`) 🌿
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`) ✨
4. **Push** to the Branch (`git push origin feature/AmazingFeature`) 📤
5. Open a **Pull Request** 📑

If you find this project helpful, don't forget to give it a ⭐ to show your support!

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/wesleymadike-1/FastApi-project/blob/main/LICENSE) file for more details. ⚖️

---

**Maintained with ❤️ by [Wesley Madike](https://github.com/wesleymadike-1)** 🔗 **Project Link:** [https://github.com/wesleymadike-1/FastApi-project](https://github.com/wesleymadike-1/FastApi-project)


```text
 _    _             _              ___  ___           _ _ _         
| |  | |           | |             |  \/  |          | (_) |        
| |  | | ___  ___  | | ___ _   _   | .  . | __ _  __| |_| | _____  
| |/\| |/ _ \/ __| | |/ _ \ | | |  | |\/| |/ _` |/ _` | | |/ / _ \ 
\  /\  /  __/\__ \ | |  __/ |_| |  | |  | | (_| | (_| | |   <  __/ 
 \/  \/ \___||___/ |_|\___|\__, |  \_|  |_/\__,_|\__,_|_|_|\_\___| 
                            __/ |