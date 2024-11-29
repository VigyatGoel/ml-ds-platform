from fastapi import FastAPI, Query, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from ..service.datascience.ds_service import DsService
from ..service.fileservice.csv_service import CsvService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {
        "program_name": "ML Platform",
        "version": "1.0"
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully",
    }


@app.get("/help", status_code=status.HTTP_200_OK)
async def help():
    return {
        "message": "API is working properly!"
    }


@app.get("/extract_features", status_code=status.HTTP_200_OK)
async def extract_csv_features(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    csv_service = CsvService()
    return csv_service.extract_features_from_csv(csv_file)


@app.post("/upload_csv", status_code=status.HTTP_200_OK)
async def upload_csv(file: UploadFile = File(...)):
    csv_service = CsvService()

    return await csv_service.upload_csv_file_service(file)


@app.get("/scatter_plot", status_code=status.HTTP_200_OK)
async def scatter_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot"),
        feature2: str = Query(..., description="Second feature for scatter plot"),
):
    print("in api.py")
    service = DsService()
    scatter_plot_data = service.get_scatter_plot_data_service(csv_file, feature1, feature2)
    return scatter_plot_data


@app.get("/histogram_plot", status_code=status.HTTP_200_OK)
async def histogram_plot(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    service = DsService()
    histogram_plot_data = service.get_histogram_plot_data_service(csv_file)
    return histogram_plot_data
