"""
Точка запуска для периодических задач
"""
import asyncio

import jobs
from common import db


async def startup_event():
    # blocking sync code must be here!
    db.apply_migrations()
    await db.engine.connect()
    all_jobs = [
        jobs.alive.app_alive,
        jobs.scrape.scrape,
    ]
    for job in all_jobs:
        asyncio.get_event_loop().create_task(job())


async def shutdown_event():
    await db.engine.dispose()


async def main():
    try:
        await startup_event()
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        await shutdown_event()


if __name__ == '__main__':
    asyncio.run(main())
