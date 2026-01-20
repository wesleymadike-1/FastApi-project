================================================================================================================
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
================================================================================================================
## 6. Using Environment Variables in Postman

When testing your API with Postman, you can manage sensitive information securely and efficiently by using environment variables:

- **Add the API URL as an Environment Variable in Postman:**  
    Create a new environment in Postman and add a variable (e.g., `base_url`) with your API's URL as its value. Use `{{base_url}}` in your request URLs. This allows you to easily switch between different environments (development, staging, production) by changing the variable value instead of updating each request manually.

- **Set the Token as a Variable in Postman:**  
    Add another variable (e.g., `token`) to your Postman environment and store your authentication token there. Reference it in your request headers as `Bearer {{token}}`. This makes it easy to update the token when it changes and keeps your requests organized and secure.

Using Postman environment variables for your API URL and token streamlines your workflow and helps protect sensitive data.
