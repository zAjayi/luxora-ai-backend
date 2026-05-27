from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ArticleFieldCreate(BaseModel):
    name: str
    description: str

class ArticleFieldUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ArticleFieldResponse(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ArticleRequest(BaseModel):
    source_text: str
    field_id: UUID
    tone: Optional[str] = "Professional"

class ArticleOutputResponse(BaseModel):
    id: UUID
    job_id: UUID
    content: str
    is_favourite: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ArticleJobResponse(BaseModel):
    id: UUID
    source_text: Optional[str]
    field_id: Optional[UUID]
    tone: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    outputs: List[ArticleOutputResponse] = []

    model_config = ConfigDict(from_attributes=True)
