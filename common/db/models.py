import uuid
from decimal import Decimal

from sqlalchemy import Column, JSON
from sqlmodel import Field

from .base import Base

__all__ = [
    'Analysis',
]


class Analysis(Base, table=True):
    """Информация об анализе с одного из мед.сайтов"""
    __tablename__ = 'analysis'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    description: str | None = None
    preparation: str | None = None
    purpose: str | None = None
    interpretation: str | None = None
    article_number: str | None = None
    total_price: Decimal | None = None
    add_data: dict = Field(
        default={},
        sa_column=Column(JSON),
        description='Слабоструктурированные доп. данные об анализе',
    )

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
