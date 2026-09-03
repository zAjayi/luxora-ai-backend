from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.db.base_class import Base

try:
    from pgvector.sqlalchemy import Vector
except Exception:  # pragma: no cover - best effort import
    Vector = None


class DocumentVector(Base):
    __tablename__ = "document_vectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("repurpose_jobs.id", ondelete="CASCADE"), nullable=True)
    source = Column(Text, nullable=True)
    metadata_ = Column('metadata', JSONB, nullable=True)
    # embedding stored using pgvector Vector type; if pgvector isn't available this will be None
    embedding = Column(Vector(1536) if Vector is not None else Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

