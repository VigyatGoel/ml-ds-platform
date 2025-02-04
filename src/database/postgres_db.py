import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/apikeys_db")


def get_engine():
    """Create and return an async database engine."""
    return create_async_engine(DATABASE_URL, future=True, echo=True)


def get_session_factory(engine):
    """Create and return a session factory for the database."""
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Base for models
Base = declarative_base()


# Dependency to get database session
def get_db():
    """Provide a session for database operations."""
    engine = get_engine()
    session_factory = get_session_factory(engine)

    async def session_scope():
        async with session_factory() as session:
            yield session

    return session_scope()
