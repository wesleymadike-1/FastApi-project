from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, text
from .database import Base
from datetime import datetime, timezone



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    profile_image = Column(String(255))
    cover_image = Column(String(255))
    website = Column(String(255))
    location = Column(String(100))
    is_active = Column(Boolean, server_default=text("true"))
    is_verified = Column(Boolean, server_default=text("false"))
    is_superuser = Column(Boolean, server_default=text("false"))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))