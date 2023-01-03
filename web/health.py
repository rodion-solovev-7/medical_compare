import typing

import sqlalchemy as sa
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Body, Depends
from loguru import logger

from common import db, di

app = FastAPI()


@app.get('/')
async def root():
    return {
        'message': "Hello World! It's alive! ... and needs improvements :("
    }


@app.get('/hello/{name}')
async def say_hello(name: str):
    return {'message': f'Hello {name}'}


@app.get('/db')
@inject
async def check_db(session: db.AsyncSession = Depends(Provide[di.Container.session])):
    raw_query = sa.text("SELECT true, 'yes', 1;")
    try:
        result = await session.execute(raw_query)
        alive, *_ = result.one()
        return alive
    except Exception as e:
        logger.error('healthcheck failed due error', exc_info=e)
        return False


@app.post('/echo')
async def echo(body: typing.Any = Body(default=None)):
    return body
