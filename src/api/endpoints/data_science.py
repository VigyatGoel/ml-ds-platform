from fastapi import APIRouter, Query, HTTPException, status, Request, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...service.datascience.plot_service import PlotService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def common_csv_file(csv_file: str = Query(..., description="Path to the CSV file")):
    return csv_file


def common_feature1(feature1: str = Query(..., description="First feature for the plot")):
    return feature1


def common_feature2(feature2: str = Query(..., description="Second feature for the plot")):
    return feature2


async def get_service(file_path: str):
    try:
        return PlotService(file_path)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/scatter_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def scatter_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
        feature2: str = Depends(common_feature2)
):
    service = await get_service(csv_file)
    return await service.get_scatter_plot_data_service(feature1, feature2)


@router.get("/histogram_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def histogram_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = await get_service(csv_file)
    return await service.get_histogram_plot_data_service()


@router.get("/line_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def line_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = await get_service(csv_file)
    return await service.get_line_plot_data_service()


@router.get("/correlation_matrix", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def correlation_matrix(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = await get_service(csv_file)
    return await service.get_correlation_matrix_data_service()


@router.get("/box_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def box_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    service = await get_service(csv_file)
    return await service.get_box_plot_data_service(feature1)


@router.get("/pair_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def pair_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    service = await get_service(csv_file)
    return await service.get_pair_plot_data_service()


@router.get("/area_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def area_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    service = await get_service(csv_file)
    return await service.get_area_plot_data_service(feature1)
