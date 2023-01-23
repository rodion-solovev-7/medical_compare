import sqlalchemy as sa
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends

from common import db, di
from common.db import models

app = FastAPI()


@app.get('/')
@inject
async def get_city_list(
    *,
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(models.City)
    result = await session.execute(query)
    # unpacking from tuple with single element
    return [r[0] for r in result.all()]
