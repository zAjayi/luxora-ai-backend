from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class RepurposeJob(Base):
    __tablename__ = "repurpose_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    source_text = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=True)
    
    tone = Column(String(50), nullable=True)
    platforms = Column(ARRAY(String), nullable=True)
    
    cta = Column(Text, nullable=True)
    include_hashtags = Column(Boolean, default=True)
    include_emojis = Column(Boolean, default=True)
    
    status = Column(String(50), default="pending")
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    outputs = relationship("RepurposedOutput", back_populates="job", cascade="all, delete-orphan")
