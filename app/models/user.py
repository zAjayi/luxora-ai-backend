from sqlalchemy import Column, String, Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    name = Column(String(255), nullable=True)
    brand_name = Column(String(255), nullable=True)
    plan = Column(String(50), default="free")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    brand_voices = relationship("BrandVoice", back_populates="user", cascade="all, delete-orphan")
    article_fields = relationship("ArticleField", back_populates="user", cascade="all, delete-orphan")
    article_jobs = relationship("ArticleJob", back_populates="user", cascade="all, delete-orphan")
    repurpose_jobs = relationship("RepurposeJob", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
