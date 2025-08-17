from fastapi import APIRouter, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from ...service.database.database_service import DatabaseService

router = APIRouter()

db_service = DatabaseService()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def verify_api_key(
    api_key: str = Security(api_key_header),
    db: AsyncSession = Depends(db_service.get_db_service),
):
    await db_service.verify_api_key_service(db, api_key)
    return api_key


@router.get("/secure-data")
async def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access to secure data!"}


@router.post("/generate-key/{owner}")
async def generate_key(
    owner: str, db: AsyncSession = Depends(db_service.get_db_service)
):
    return await db_service.generate_key_service(db, owner)


@router.delete("/delete-key/{api_key}")
async def delete_key(
    api_key: str, db: AsyncSession = Depends(db_service.get_db_service)
):
    return await db_service.delete_key_service(db, api_key)
