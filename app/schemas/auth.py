from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class UserRegister(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    id: UUID
    email: str
    name: str | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
