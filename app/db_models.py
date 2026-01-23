from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
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

    poster = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    # Use autoincrement instead of random. It's safer and faster!
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(String(50), nullable=False, index=True)
    content = Column(Text, nullable=False)
    

    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    owner = relationship("User", back_populates="poster")

class Likes(Base):
    __tablename__ = "likes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True ,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True,primary_key=True)