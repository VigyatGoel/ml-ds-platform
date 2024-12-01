from fastapi import APIRouter
from fastapi import Query, status

from ...service.datascience.ds_service import DsService

router = APIRouter()
service = DsService()


@router.get("/scatter_plot", status_code=status.HTTP_200_OK)
async def scatter_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot"),
        feature2: str = Query(..., description="Second feature for scatter plot"),
):
    service = DsService()
    scatter_plot_data = service.get_scatter_plot_data_service(csv_file, feature1, feature2)
    return scatter_plot_data


@router.get("/histogram_plot", status_code=status.HTTP_200_OK)
async def histogram_plot(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    service = DsService()
    histogram_plot_data = service.get_histogram_plot_data_service(csv_file)
    return histogram_plot_data


@router.get("/line_plot", status_code=status.HTTP_200_OK)
async def line_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot")
):
    service = DsService()
    line_plot_data = service.get_line_plot_data_service(csv_file, feature1)
    return line_plot_data


@router.get("/correlation_matrix", status_code=status.HTTP_200_OK)
async def correlation_matrix(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    service = DsService()
    correlation_matrix_data = service.get_correlation_matrix_data_service(csv_file)
    return correlation_matrix_data


@router.get("/box_plot", status_code=status.HTTP_200_OK)
async def box_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot")
):
    service = DsService()
    box_plot_data = service.get_box_plot_data_service(csv_file, feature1)
    return box_plot_data


@router.get("/pair_plot", status_code=status.HTTP_200_OK)
async def pair_plot(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    service = DsService()
    pair_plot_data = service.get_pair_plot_data_service(csv_file)
    return pair_plot_data


@router.get("/area_plot", status_code=status.HTTP_200_OK)
async def area_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot")
):
    service = DsService()
    area_plot_data = service.get_area_plot_data_service(csv_file, feature1)
    return area_plot_data
