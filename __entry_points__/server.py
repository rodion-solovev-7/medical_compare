"""
Точка входа для запуска web-сервера (backend проекта)
"""
from pathlib import Path

import uvicorn
from fastapi import FastAPI

import config
from common import db, di
from web import health
from web.v1 import analysis

app = FastAPI()
# без создания экземпляра контейнера di-инъекции работать не будут
app.container = di.Container()


@app.on_event('startup')
async def startup_event():
    # blocking sync code must be here!
    db.apply_migrations()
    await db.engine.connect()


@app.on_event('shutdown')
async def shutdown_event():
    await db.engine.dispose()


# add sub-apps
app.mount('/health', health.app)
app.mount('/v1/analysis', analysis.app)
# app.mount('/v1/jsonrpc', v1_jsonrpc.app)


def main():
    uvicorn.run(
        app=f'{__name__}:app',
        host=config.HOST,
        port=config.PORT,
        reload=True,
        reload_dirs=[(Path() / '..').as_posix()],
    )


if __name__ == '__main__':
    main()
