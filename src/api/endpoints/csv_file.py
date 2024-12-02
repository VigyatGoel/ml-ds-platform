from fastapi import APIRouter, Query, File, UploadFile, status, Depends
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter

from ...service.fileservice.csv_service import CsvService

router = APIRouter()
csv_service = CsvService()


@router.get("/extract_features", status_code=status.HTTP_200_OK,
            dependencies=[Depends(RateLimiter(times=20, seconds=60))])
@cache(expire=1800)
async def extract_csv_features(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    return csv_service.extract_features_from_csv(csv_file)


@router.post("/upload_csv", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def upload_csv(file: UploadFile = File(...)):
    return await csv_service.upload_csv_file_service(file)
