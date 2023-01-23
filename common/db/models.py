import uuid
from decimal import Decimal

from sqlalchemy import Column, JSON, cast, Index, func
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from .base import Base

__all__ = [
    'Analysis',
]


# def create_tsvector(*args):
#     return func.to_tsvector('english', ' '.join(args))


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
        default_factory=dict,
        sa_column=Column(JSON),
        description='Слабоструктурированные доп. данные об анализе',
    )

    __table_args__ = (
        # Needed for full text search by 'name' field
        Index(
            'ix_analysis_name_tsv',
            func.to_tsvector('english', 'name'),
            postgresql_using='gin',
        ),
    )

    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True


class City(Base, table=True):
    __tablename__ = 'city'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    url: str
    code: str | None = None
