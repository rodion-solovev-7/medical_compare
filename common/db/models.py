import uuid

from sqlmodel import Field

from .base import Base


__all__ = [
    'Analysis',
]


class Analysis(Base):
    """Информация об анализе с одного из медсайтов"""
    __tablename__ = 'analysis'

    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    # TODO: добавить нормальные поля
    data: str | None = None
