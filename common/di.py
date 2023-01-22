"""Containers module."""

from dependency_injector import containers
from dependency_injector.providers import Configuration, Factory
from dependency_injector.wiring import Provider

from common import db


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        'web', 'jobs', 'scraper', '__entry_points__',
    ])
    config = Configuration()

    session: Provider[db.AsyncSession] = Factory(
        db.SessionLocal,
    )
