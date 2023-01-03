from pathlib import Path
from typing import AsyncIterator, Iterator

import yoyo
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel

import config

__all__ = [
    'DB_URL', 'engine', 'sync_engine', 'SessionLocal', 'SyncSessionLocal',
    'Base', 'get_session', 'get_sync_session', 'apply_migrations', 'AsyncSession', 'Session',
]


# подключение открывается только при первом запросе к БД
# так что держать 2 engine относительно безопасно: для sync и async
_CONNECTION_POSTFIX = f'{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
DB_URL = f'postgresql+asyncpg://{_CONNECTION_POSTFIX}'
engine = create_async_engine(DB_URL, echo=config.DB_ECHO, future=True)
sync_engine = create_engine(DB_URL, echo=config.DB_ECHO, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine, class_=Session)

# класс для наследования моделями БД
Base = SQLModel

# строка подключения для миграций
YOYO_DB_URL = f'postgresql://{_CONNECTION_POSTFIX}'


async def get_session() -> AsyncIterator[AsyncSession]:
    """DI-инъекция для асинхронной работы с БД"""
    async with SessionLocal() as session:
        yield session


def get_sync_session() -> Iterator[Session]:
    """DI-инъекция для синхронной работы с БД"""
    with SyncSessionLocal() as session:
        yield session


def apply_migrations():
    """Применение миграций из common.db.migrations"""
    backend = yoyo.get_backend(YOYO_DB_URL, 'migrations')
    migrations_folder = Path(__file__).parent / 'migrations'

    with backend.lock():
        migrations = yoyo.read_migrations(migrations_folder.as_posix())
        if not migrations:
            logger.info('No migrations to apply')
            return
        backend.apply_migrations(backend.to_apply(migrations))
