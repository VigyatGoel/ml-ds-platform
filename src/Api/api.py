import os

import pandas as pd
from fastapi import FastAPI, Query, HTTPException, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..DataScience.Plots.plots import Plot

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


@app.get("/extract_features")
async def extract_csv_features(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    try:
        if not os.path.exists(csv_file):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

        df = pd.read_csv(csv_file)

        label_column = df.columns[-1]  # Last column is the label

        # Extract the names of the feature columns (all except the label column)
        feature_columns = df.columns[:-1].tolist()  # All columns except the last one

        return JSONResponse(content={"feature_columns": feature_columns, "label_column": label_column})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


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


@app.post("/upload_csv", status_code=status.HTTP_200_OK)
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_location = f"../CsvFiles/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        absolute_file_path = os.path.abspath(file_location)

        return {
            "message": f"File '{file.filename}' uploaded successfully",
            "file_path": file_location,
            "absolute_file_path": absolute_file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/scatter_plot", status_code=status.HTTP_200_OK)
async def scatter_plot(
        csv_file: str = Query(..., description="Path to the CSV file"),
        feature1: str = Query(..., description="First feature for scatter plot"),
        feature2: str = Query(..., description="Second feature for scatter plot"),
):
    try:
        if not os.path.exists(csv_file):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

        plot = Plot()
        scatter_plot_data = plot.get_scatter_plot_data(csv_file, feature1=feature1, feature2=feature2)

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


@app.get("/histogram_plot", status_code=status.HTTP_200_OK)
async def histogram_plot(
        csv_file: str = Query(..., description="Path to the CSV file")
):
    try:
        if not os.path.exists(csv_file):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

        plot = Plot()
        histogram_plot_data = plot.get_histogram_plot_data(csv_file)
        rounded_data = histogram_plot_data.round(2)
        return rounded_data.to_dict(orient="list")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
