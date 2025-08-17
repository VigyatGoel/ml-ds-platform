from fastapi import APIRouter, Query, File, UploadFile, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...service.fileservice.csv_service import CsvService

router = APIRouter()
csv_service = CsvService()

limiter = Limiter(key_func=get_remote_address)


@router.get("/extract_features", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def extract_csv_features(
    request: Request, csv_file: str = Query(..., description="Path to the CSV file")
):
    return csv_service.extract_features_from_csv(csv_file)


@router.post("/upload_csv", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def upload_csv(request: Request, file: UploadFile = File(...)):
    return await csv_service.upload_csv_file_service(file)


@router.delete("/cleanup_temp_file", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def cleanup_temp_file(
    request: Request,
    file_path: str = Query(..., description="Path to the temporary file to delete"),
):
    success = csv_service.cleanup_temp_file(file_path)
    if success:
        return {"message": "Temporary file cleaned up successfully"}
    else:
        return {"message": "File not found or already deleted"}
