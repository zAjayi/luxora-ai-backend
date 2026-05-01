from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class BrandVoiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    style_guide_text: str

class BrandVoiceCreate(BrandVoiceBase):
    pass

class BrandVoiceUpdate(BrandVoiceBase):
    name: Optional[str] = None
    style_guide_text: Optional[str] = None

class BrandVoiceResponse(BrandVoiceBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
