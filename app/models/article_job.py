from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class ArticleJob(Base):
    __tablename__ = "article_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    source_text = Column(Text, nullable=True)
    field_id = Column(UUID(as_uuid=True), ForeignKey("article_fields.id"), nullable=True)
    
    tone = Column(String(50), nullable=True)
    status = Column(String(50), default="pending")
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    outputs = relationship("ArticleOutput", back_populates="job", cascade="all, delete-orphan")
