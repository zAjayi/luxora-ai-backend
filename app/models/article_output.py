from sqlalchemy import Column, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class ArticleOutput(Base):
    __tablename__ = "article_outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("article_jobs.id", ondelete="CASCADE"), nullable=False)
    
    content = Column(Text)
    is_favourite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    job = relationship("ArticleJob", back_populates="outputs")
