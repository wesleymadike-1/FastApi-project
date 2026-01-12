from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, text
from .database import Base
from datetime import datetime, timezone
import random



class User(Base):
    __tablename__ = "users"

    def generate_user_id():
        return random.randint(100, 99999)

    id = Column(Integer, primary_key=True, unique=True, index=True, default=generate_user_id)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    # Stores the securely hashed password for the user
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))