from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base_class import Base

class RepurposedOutput(Base):
    __tablename__ = "repurposed_outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("repurpose_jobs.id", ondelete="CASCADE"))
    platform = Column(String(50), index=True)
    variant_index = Column(Integer)
    content = Column(Text, nullable=False)
    is_favourite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    job = relationship("RepurposeJob", back_populates="outputs")
