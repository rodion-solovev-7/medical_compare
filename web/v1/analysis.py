import uuid

import sqlalchemy as sa
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends, Query

from common import db, di
from common.db import models

app = FastAPI()


@app.get('/')
@inject
async def get_analysis_list(
    q: str | None = Query(default=None, description='Поисковый запрос по названию'),
    offset: int = Query(default=0, ge=0, description='Смещение по поисковым результатам'),
    limit: int = Query(default=100, lte=100, description='Кол-во результатов поиск'),
    *,
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(models.Analysis).offset(offset).limit(limit)
    if q is not None:
        # noinspection PyUnresolvedReferences
        query = query.where(models.Analysis.name.contains(q))
    result = await session.execute(query)
    # unpacking from tuple with single element
    return [r[0] for r in result.all()]


@app.get('/{analysis_id}')
@inject
async def get_single_analysis(
    analysis_id: uuid.UUID,
    *,
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(models.Analysis).where(models.Analysis.id == analysis_id)
    result = await session.execute(query)
    # unpacking from tuple with single element
    return result.one()[0]
