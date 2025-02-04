from passlib.hash import bcrypt
from sqlalchemy import Column, String

from .postgres_db import Base


def create_api_key_model():
    """Define and return the APIKey model class."""

    class APIKey(Base):
        __tablename__ = "api_keys"

        key_hash = Column(String, primary_key=True, index=True)
        owner = Column(String, index=True)

        @staticmethod
        def hash_api_key(api_key: str) -> str:
            return bcrypt.hash(api_key)

        @staticmethod
        def verify_api_key(api_key: str, hashed_key: str) -> bool:
            return bcrypt.verify(api_key, hashed_key)

    return APIKey
