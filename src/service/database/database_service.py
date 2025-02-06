from fastapi import HTTPException

from ...database.crud import is_valid_api_key, create_api_key, delete_api_key
from ...database.postgres_db import Base, engine, get_db


class DatabaseService:

    @staticmethod
    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def verify_api_key_service(db, api_key):
        if not await is_valid_api_key(db, api_key):
            raise HTTPException(status_code=403, detail="Invalid API Key")

    @staticmethod
    async def generate_key_service(db, owner):
        new_key = await create_api_key(db, owner)
        return {"owner": owner, "api_key": new_key}

    @staticmethod
    async def delete_key_service(db, api_key):
        if await delete_api_key(db, api_key):
            return {"message": "API key deleted successfully"}
        raise HTTPException(status_code=404, detail="API key not found")

    @staticmethod
    async def get_db_service():
        async for db in get_db():
            yield db
