import secrets
from datetime import datetime, timedelta, UTC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .model import APIKey


async def create_api_key(db: AsyncSession, owner: str) -> str:
    raw_key = secrets.token_hex(32)
    hashed_key = await APIKey.hash_api_key(raw_key)
    expires_at = datetime.now(UTC) + timedelta(days=30)
    api_key_entry = APIKey(key_hash=hashed_key, owner=owner, expires_at=expires_at)
    db.add(api_key_entry)
    await db.commit()

    return raw_key


async def list_api_keys(db: AsyncSession):
    result = await db.execute(select(APIKey))
    return result.scalars().all()


async def is_valid_api_key(db: AsyncSession, api_key: str) -> bool:
    result = await db.execute(
        select(APIKey).where(APIKey.expires_at >= datetime.now(UTC))
    )  # Select full object
    for key_entry in result.scalars():  # key_entry is now an APIKey object
        if await APIKey.verify_api_key(
            api_key, key_entry.key_hash
        ):  # Now correctly accesses key_hash
            return True
    return False


async def delete_api_key(db: AsyncSession, api_key: str) -> bool:
    result = await db.execute(select(APIKey).where(APIKey.key_hash.is_not(None)))
    for key_entry in result.scalars():
        if await APIKey.verify_api_key(api_key, key_entry.key_hash):
            await db.delete(key_entry)
            await db.commit()
            return True
    return False
