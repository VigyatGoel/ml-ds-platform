import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .model import create_api_key_model

APIKey = create_api_key_model()


async def create_api_key(db: AsyncSession, owner: str) -> str:
    raw_key = secrets.token_hex(32)
    hashed_key = APIKey.hash_api_key(raw_key)

    api_key_entry = APIKey(key_hash=hashed_key, owner=owner)
    db.add(api_key_entry)
    await db.commit()

    return raw_key


async def is_valid_api_key(db: AsyncSession, api_key: str) -> bool:
    result = await db.execute(select(APIKey).where(APIKey.key_hash.like("%")))
    for key_entry in result.scalars():
        if APIKey.verify_api_key(api_key, key_entry.key_hash):
            return True
    return False


async def delete_api_key(db: AsyncSession, api_key: str) -> bool:
    result = await db.execute(select(APIKey))
    for key_entry in result.scalars():
        if APIKey.verify_api_key(api_key, key_entry.key_hash):
            await db.delete(key_entry)
            await db.commit()
            return True
    return False
