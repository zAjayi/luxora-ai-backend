from pydantic import BaseModel
from typing import List, Optional, Dict

class RepurposeRequest(BaseModel):
    source_text: str
    platforms: List[str]
    tone: Optional[str] = "Professional"
    brand_voice_description: Optional[str] = None

class RepurposeResponse(BaseModel):
    outputs: Dict[str, List[str]]
