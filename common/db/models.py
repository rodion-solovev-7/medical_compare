import uuid
from decimal import Decimal

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from .base import Base

__all__ = [
    'Analysis',
    'City',
]


class City(Base, table=True):
    """Город для которого хранится информация об анализах"""
    __tablename__ = 'city'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    url: str
    code: str | None = None

    analyses: list['Analysis'] = Relationship(back_populates='city')


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

    city_id: uuid.UUID = Field(foreign_key='city.id', nullable=False)
    city: City = Relationship(back_populates='analyses')
    # city: City = Relationship(
    #     sa_relationship_kwargs={
    #         'primaryjoin': 'City.id==Analysis.city_id',
    #         'lazy': 'joined',
    #     }
    # )

    class Config:
        # Needed for Column(JSON)
        arbitrary_types_allowed = True
