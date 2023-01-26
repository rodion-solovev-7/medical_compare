import uuid

from fastapi_users import models, schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[int]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    id: models.ID
    email: EmailStr
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserUpdate(schemas.BaseUserUpdate):
    name: str


class CustomAnalysisRead(BaseModel):
    name: str | None = None


class CustomAnalysisCreate(BaseModel):
    name: str
    unit: str
    value: str


class CustomAnalysisDelete(BaseModel):
    id: uuid.UUID | None = None
    name: str | None = None


class SugarAnalysisCreate(BaseModel):
    value: float


class SugarAnalysisDelete(BaseModel):
    id: uuid.UUID
