import uuid

import sqlalchemy as sa
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_users import FastAPIUsers

from common import db, di
from common.auth.auth import auth_backend
from common.auth.manager import get_user_manager
from web.v1 import schemas

app = FastAPI()

fastapi_users = FastAPIUsers[db.User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()

SUGAR_NAME = 'Сахар в крови'
SUGAR_UNIT = 'mmol/l'


@app.get('/sugar', response_model=list[db.CustomAnalysis])
@inject
async def get_sugar_analysis_list(
    offset: int = Query(default=0, ge=0, description='Смещение по поисковым результатам'),
    limit: int = Query(default=100, lte=100, description='Кол-во результатов поиска'),
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(db.CustomAnalysis).where(
        db.CustomAnalysis.name == SUGAR_NAME,
        db.CustomAnalysis.user_id == user.id,
    ).order_by(
        db.CustomAnalysis.created_at.desc()
    ).offset(offset).limit(limit)
    result = await session.execute(query)
    # unpacking from tuple with single element
    return [r[0] for r in result.all()]


@app.post('/sugar', response_model=db.CustomAnalysis)
@inject
async def create_sugar_analysis(
    sugar: schemas.SugarAnalysisCreate,
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    model = db.CustomAnalysis(
        name=SUGAR_NAME,
        unit=SUGAR_UNIT,
        value=sugar.value,
        user_id=user.id,
    )
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


@app.delete('/sugar')
@inject
async def delete_sugar_analysis(
    sugar: schemas.SugarAnalysisDelete,
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(db.CustomAnalysis).where(
        db.CustomAnalysis.name == SUGAR_NAME,
        db.CustomAnalysis.id == sugar.id,
    ).where(db.CustomAnalysis.user_id == user.id)
    result = await session.execute(query)
    analysis_tuple = result.one_or_none()
    if analysis_tuple is None:
        return
    await session.delete(analysis_tuple[0])
    await session.commit()


@app.get('/custom', response_model=list[db.CustomAnalysis])
@inject
async def get_custom_analyses_list(
    custom: schemas.CustomAnalysisRead | None = None,
    offset: int = Query(default=0, ge=0, description='Смещение по поисковым результатам'),
    limit: int = Query(default=100, lte=100, description='Кол-во результатов поиска'),
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    query = sa.select(db.CustomAnalysis).where(
        db.CustomAnalysis.user_id == user.id,
    ).order_by(
        db.CustomAnalysis.created_at.desc()
    ).offset(offset).limit(limit)
    if custom is not None and custom.name is not None:
        query = query.where(
            db.CustomAnalysis.name == custom.name,
        )
    result = await session.execute(query)
    # unpacking from tuple with single element
    return [r[0] for r in result.all()]


@app.post('/custom', response_model=db.CustomAnalysis)
@inject
async def create_custom_analysis(
    custom: schemas.CustomAnalysisCreate,
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    analysis = db.CustomAnalysis(
        name=custom.name,
        unit=custom.unit,
        value=custom.value,
        user_id=user.id,
    )
    session.add(analysis)
    await session.commit()
    await session.refresh(analysis)
    return analysis


@app.delete('/custom')
@inject
async def delete_custom_analysis(
    custom: schemas.CustomAnalysisDelete,
    *,
    user: db.User = Depends(current_user),
    session: db.AsyncSession = Depends(Provide[di.Container.session]),
):
    if custom.id is None and custom.name is None:
        return

    query = sa.delete(db.CustomAnalysis).where(
        db.CustomAnalysis.user_id == user.id,
    )
    if custom.id is not None:
        query = query.where(
            db.CustomAnalysis.id == custom.id,
        )
    if custom.name is not None:
        query = query.where(
            db.CustomAnalysis.name == custom.name,
        )

    await session.execute(query)
    await session.commit()
