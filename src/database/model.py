import asyncio
import hashlib

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from .postgres_db import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    key_hash = Column(String, primary_key=True, index=True)
    owner = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    @staticmethod
    async def hash_api_key(api_key: str) -> str:
        """Asynchronously hash the API key and return the hex digest"""
        # Await asyncio.to_thread to get the hashed result and then return the hex digest
        hashed_key = await asyncio.to_thread(hashlib.sha256, api_key.encode())
        return hashed_key.hexdigest()  # Now call hexdigest() after awaiting the result

    @staticmethod
    async def verify_api_key(api_key: str, hashed_key: str) -> bool:
        """Asynchronously verify if the API key matches the stored hash"""
        # Await asyncio.to_thread to get the hex digest and then compare
        calculated_hash = await asyncio.to_thread(hashlib.sha256, api_key.encode())
        return await asyncio.to_thread(lambda: calculated_hash.hexdigest() == hashed_key.lower())
