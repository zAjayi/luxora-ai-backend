from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID

class RepurposeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: str = Field(alias="source_text")
    source_url: Optional[str] = None
    instruction: Optional[str] = None
    platforms: Optional[List[str]] = None
    tone: Optional[str] = "Professional"
    brand_voice_description: Optional[str] = None
    brand_voice_id: Optional[UUID] = None
    hashtags_enabled: Optional[bool] = True
    emojis_enabled: Optional[bool] = True
    cta_text: Optional[str] = None

class RepurposeResponse(BaseModel):
    outputs: Dict[str, List[str]]

class RepurposedOutputResponse(BaseModel):
    id: UUID
    job_id: UUID
    platform: str
    variant_index: int
    content: str
    is_favourite: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RepurposeJobResponse(BaseModel):
    id: UUID
    source_text: Optional[str]
    source_url: Optional[str]
    source_type: Optional[str]
    title: Optional[str]
    tone: Optional[str]
    platforms: Optional[List[str]]
    cta: Optional[str]
    include_hashtags: bool
    include_emojis: bool
    status: str
    created_at: datetime
    updated_at: datetime
    outputs: List[RepurposedOutputResponse] = []

    model_config = ConfigDict(from_attributes=True)
