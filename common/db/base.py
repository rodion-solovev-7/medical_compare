from pathlib import Path
from typing import AsyncIterator

import yoyo
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import SQLModel

import config

__all__ = [
    'DB_URL', 'engine', 'SessionLocal', 'Base', 'SABase',
    'get_session', 'apply_migrations', 'AsyncSession',
]


# подключение открывается только при первом запросе к БД
# так что держать 2 engine относительно безопасно: для sync и async
_CONNECTION_POSTFIX = f'{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
DB_URL = f'postgresql+asyncpg://{_CONNECTION_POSTFIX}'
engine = create_async_engine(DB_URL, echo=config.DB_ECHO, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# классы для наследования моделями БД
Base = SQLModel
SABase = declarative_base(metadata=Base.metadata)

# строка подключения для миграций
YOYO_DB_URL = f'postgresql://{_CONNECTION_POSTFIX}'


async def get_session() -> AsyncIterator[AsyncSession]:
    """DI-инъекция для асинхронной работы с БД"""
    async with SessionLocal() as session:
        yield session


def apply_migrations():
    """Применение миграций из common.db.migrations"""
    backend = yoyo.get_backend(YOYO_DB_URL, 'migrations')
    migrations_folder = Path(__file__).parent / 'migrations'

    with backend.lock():
        migrations = yoyo.read_migrations(migrations_folder.as_posix())
        if not migrations:
            logger.info('No migrations found')
            return
        to_migrate = backend.to_apply(migrations)
        if len(to_migrate) > 0:
            logger.info('Applying migrations')
            backend.apply_migrations(to_migrate)
        else:
            logger.info('No migrations to apply')
