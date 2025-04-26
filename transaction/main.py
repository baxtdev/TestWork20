from fastapi import FastAPI

from contextlib import asynccontextmanager

from . import routers
from .models import Base
from .db import engine
from .middleware import APIKeyMiddleware

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routers.router)
 
