from fastapi import APIRouter, Query, File, UploadFile, status

from ...service.fileservice.csv_service import CsvService

router = APIRouter()
csv_service = CsvService()


@router.get("/extract_features", status_code=status.HTTP_200_OK)
async def extract_csv_features(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    return csv_service.extract_features_from_csv(csv_file)


@router.post("/upload_csv", status_code=status.HTTP_200_OK)
async def upload_csv(file: UploadFile = File(...)):
    return await csv_service.upload_csv_file_service(file)
