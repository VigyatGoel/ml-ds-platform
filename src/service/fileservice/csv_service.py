import os

import pandas as pd
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse


class CsvService:

    @staticmethod
    async def upload_csv_file_service(file: UploadFile) -> dict:
        try:

            directory = os.path.join(os.path.dirname(__file__), "../../csvfiles")
            os.makedirs(directory, exist_ok=True)

            file_location = os.path.join(directory, file.filename)

            with open(file_location, "wb") as f:
                f.write(await file.read())

            absolute_file_path = os.path.abspath(file_location)

            return {
                "message": f"File '{file.filename}' uploaded successfully",
                "absolute_file_path": absolute_file_path
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

    @staticmethod
    def extract_features_from_csv(csv_file):
        try:
            if not os.path.exists(csv_file):
                raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

            df = pd.read_csv(csv_file)

            label_column = df.columns[-1]  # Last column is the label

            feature_columns = df.columns[:-1].tolist()  # All columns except the last one

            return JSONResponse(content={"feature_columns": feature_columns, "label_column": label_column})
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
