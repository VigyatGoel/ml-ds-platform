from fastapi import APIRouter
from fastapi import Query, status
from fastapi.params import Depends
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter

from ...service.datascience.ds_service import DsService

router = APIRouter()
service = DsService()


def common_csv_file(csv_file: str = Query(..., description="Path to the CSV file")):
    return csv_file


def common_feature1(feature1: str = Query(..., description="First feature for the plot")):
    return feature1


def common_feature2(feature2: str = Query(..., description="Second feature for the plot")):
    return feature2


@router.get("/scatter_plot", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def scatter_plot(
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
        feature2: str = Depends(common_feature2)
):
    scatter_plot_data = service.get_scatter_plot_data_service(csv_file, feature1, feature2)
    return scatter_plot_data


@router.get("/histogram_plot", status_code=status.HTTP_200_OK,
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def histogram_plot(
        csv_file: str = Depends(common_csv_file)
):
    histogram_plot_data = service.get_histogram_plot_data_service(csv_file)
    return histogram_plot_data


@router.get("/line_plot", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def line_plot(
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    line_plot_data = service.get_line_plot_data_service(csv_file, feature1)
    return line_plot_data


@router.get("/correlation_matrix", status_code=status.HTTP_200_OK,
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def correlation_matrix(
        csv_file: str = Depends(common_csv_file)
):
    correlation_matrix_data = service.get_correlation_matrix_data_service(csv_file)
    return correlation_matrix_data


@router.get("/box_plot", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def box_plot(
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    box_plot_data = service.get_box_plot_data_service(csv_file, feature1)
    return box_plot_data


@router.get("/pair_plot", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def pair_plot(
        csv_file: str = Depends(common_csv_file)
):
    pair_plot_data = service.get_pair_plot_data_service(csv_file)
    return pair_plot_data


@router.get("/area_plot", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
@cache(expire=1800)
async def area_plot(
        csv_file: str = Depends(common_csv_file),
        feature1: str = Depends(common_feature1),
):
    area_plot_data = service.get_area_plot_data_service(csv_file, feature1)
    return area_plot_data
