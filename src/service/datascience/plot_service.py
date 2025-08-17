from functools import wraps

from fastapi import HTTPException

from ...datascience.plots.plots import Plot


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper


class PlotService:
    def __init__(self, file_path: str):
        self.plot = Plot(file_path)

    @handle_exceptions
    async def get_scatter_plot_data_service(self, feature1, feature2):
        scatter_plot_data = await self.plot.get_scatter_plot_data(feature1, feature2)
        return scatter_plot_data.round(2).to_dict(orient="list")

    @handle_exceptions
    async def get_histogram_plot_data_service(self):
        histogram_plot_data = await self.plot.get_histogram_plot_data()
        return histogram_plot_data.round(2).to_dict(orient="list")

    @handle_exceptions
    async def get_line_plot_data_service(self):
        line_plot_data = await self.plot.get_line_plot_data()
        return line_plot_data.round(2).reset_index(drop=True).to_dict(orient="list")

    @handle_exceptions
    async def get_correlation_matrix_data_service(self):
        correlation_matrix_data = await self.plot.get_correlation_matrix_data()
        if correlation_matrix_data.empty:
            raise HTTPException(
                status_code=422,
                detail="No numeric columns available to calculate correlation.",
            )
        return correlation_matrix_data.round(4).to_dict(orient="list")

    @handle_exceptions
    async def get_box_plot_data_service(self, feature1):
        boxplot_data = await self.plot.get_box_plot_data(feature1)
        return {feature1: boxplot_data.round(2).tolist()}

    @handle_exceptions
    async def get_pair_plot_data_service(self):
        pair_plot_data = await self.plot.get_pair_plot_data()
        return pair_plot_data.round(2).to_dict(orient="list")

    @handle_exceptions
    async def get_area_plot_data_service(self, feature1):
        area_plot_data = await self.plot.get_area_plot_data(feature1)
        return {feature1: area_plot_data.round(2).tolist()}
