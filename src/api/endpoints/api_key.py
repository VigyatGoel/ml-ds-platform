from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.crud import create_api_key, is_valid_api_key, delete_api_key
from ...database.postgres_db import get_db

router = APIRouter()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def verify_api_key(
        api_key: str = Security(api_key_header), db: AsyncSession = Depends(get_db)
):
    """Verify the provided API key."""
    if not await is_valid_api_key(db, api_key):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


@router.get("/secure-data")
async def get_secure_data(api_key: str = Depends(verify_api_key)):
    """Protected route to fetch secure data."""
    return {"message": "You have access to secure data!"}


@router.post("/generate-key/{owner}")
async def generate_key(owner: str, db: AsyncSession = Depends(get_db)):
    """Route to generate a new API key."""
    new_key = await create_api_key(db, owner)
    return {"owner": owner, "api_key": new_key}


@router.delete("/delete-key/{api_key}")
async def delete_key(api_key: str, db: AsyncSession = Depends(get_db)):
    """Route to delete an API key."""
    if await delete_api_key(db, api_key):
        return {"message": "API key deleted successfully"}
    raise HTTPException(status_code=404, detail="API key not found")
