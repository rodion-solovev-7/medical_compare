import datetime
import uuid
from decimal import Decimal

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, JSON, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from .base import Base, SABase

__all__ = [
    'Analysis',
    'City',
    'User',
    'CustomAnalysis',
    'LinkFollowingHistory',
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


class User(SQLAlchemyBaseUserTable[int], SABase):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=64), unique=True, nullable=False)
    name = Column(String(length=64), nullable=False)
    hashed_password = Column(String(length=128), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # custom_analyses = relationship('CustomAnalysis', back_populates='user')
    # custom_analyses = relationship('LinkFollowingHistory', back_populates='user')


class CustomAnalysis(Base, table=True):
    __tablename__ = 'customanalysis'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str
    unit: str
    value: float
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    user_id: int = Field(foreign_key='user.id', nullable=False)
    user: User = Relationship(sa_relationship=relationship('User', back_populates='custom_analyses'))


class LinkFollowingHistory(Base, table=True):
    """История переходов по ссылкам на анализы"""
    __tablename__ = 'linkfollowinghistory'

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    link: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    user_id: int = Field(foreign_key='user.id', nullable=False)
    user: User = Relationship(sa_relationship=relationship('User', back_populates='link_followings_history'))
