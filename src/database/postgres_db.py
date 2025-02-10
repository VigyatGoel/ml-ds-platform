import asyncio
import os
import ssl

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# Create an SSL context
ssl_context = ssl.create_default_context(cafile="./ca.pem")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},
)

SessionLocal = async_scoped_session(
    sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False),
    scopefunc=asyncio.current_task,
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
