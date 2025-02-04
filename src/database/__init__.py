from .postgres_db import Base, get_engine


async def init_db():
    """Initialize the database and create tables."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
