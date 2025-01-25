from fastapi import APIRouter
from fastapi import Query, status, Request
from fastapi.params import Depends
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...service.datascience.ds_service import DsService

router = APIRouter()
service = DsService()

limiter = Limiter(key_func=get_remote_address)


def common_csv_file(csv_file: str = Query(..., description="Path to the CSV file")):
    return csv_file


def common_feature1(feature1: str = Query(..., description="First feature for the plot")):
    return feature1


def common_feature2(feature2: str = Query(..., description="Second feature for the plot")):
    return feature2


@router.get("/scatter_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def scatter_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
        feature2: str = Depends(common_feature2)
):
    scatter_plot_data = service.get_scatter_plot_data_service(csv_file, feature1, feature2)
    return scatter_plot_data


@router.get("/histogram_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def histogram_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    histogram_plot_data = service.get_histogram_plot_data_service(csv_file)
    return histogram_plot_data


@router.get("/line_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def line_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    line_plot_data = service.get_line_plot_data_service(csv_file)
    return line_plot_data


@router.get("/correlation_matrix", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def correlation_matrix(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    correlation_matrix_data = service.get_correlation_matrix_data_service(csv_file)
    return correlation_matrix_data


@router.get("/box_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def box_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    box_plot_data = service.get_box_plot_data_service(csv_file, feature1)
    return box_plot_data


@router.get("/pair_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def pair_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file)
):
    pair_plot_data = service.get_pair_plot_data_service(csv_file)
    return pair_plot_data


@router.get("/area_plot", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def area_plot(
        request: Request,
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    area_plot_data = service.get_area_plot_data_service(csv_file, feature1)
    return area_plot_data
