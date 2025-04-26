from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from contextlib import contextmanager
from . import conf


DATABASE_URL = conf.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


SYNC_DATABASE_URL = conf.SYNC_DATABASE_URL 
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=sync_engine)


async def get_db():
    async with async_session() as session:
        yield session

@contextmanager
def sync_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()