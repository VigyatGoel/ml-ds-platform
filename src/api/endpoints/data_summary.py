from fastapi import APIRouter, Query, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...service.datascience.data_summary_service import DataSummaryService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def common_csv_file(csv_file: str = Query(..., description="Path to the CSV file")):
    return csv_file


def get_service(file_path: str):
    try:
        return DataSummaryService(file_path)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/file_info", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def file_info(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_file_info_service())


@router.get("/data_description", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def data_description(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_data_description_service())


@router.get("/data_info", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def data_info(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_data_info_service())


@router.get("/data_types", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def data_types(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_data_types_service())


@router.get("/categorical_columns_count", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def categorical_columns_count(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_categorical_columns_count_service())


@router.get("/row_col_count", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def row_col_count(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_row_col_count_service())


@router.get("/null_value_count", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
def null_values(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = get_service(csv_file)
    return JSONResponse(content=service.get_null_val_count_service())
