import os

from fastapi import HTTPException

from ...datascience.plots.plots import Plot


class DsService:
    def __init__(self):
        self.plot = Plot()

    def get_scatter_plot_data_service(self, csv_file, feature1, feature2):
        try:
            print("in service.py")
            if not os.path.exists(csv_file):
                raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

            if not feature1 or not feature2:
                raise HTTPException(status_code=400, detail="Both feature1 and feature2 must be specified")

            scatter_plot_data = self.plot.get_scatter_plot_data(csv_file, feature1=feature1, feature2=feature2)

            rounded_data = scatter_plot_data.round(2)

            return rounded_data.to_dict(orient="list")

        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid feature(s): {e}")

        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_histogram_plot_data_service(self, csv_file):
        try:
            if not os.path.exists(csv_file):
                raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")
            histogram_plot_data = self.plot.get_histogram_plot_data(csv_file)

            rounded_data = histogram_plot_data.round(2)
            return rounded_data.to_dict(orient="list")

        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
