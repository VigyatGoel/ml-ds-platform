import os
import tempfile

import pandas as pd
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse


class CsvService:
    @staticmethod
    async def upload_csv_file_service(file: UploadFile) -> dict:
        try:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,  # Don't delete immediately so we can read it later
                suffix=f"_{file.filename}",  # Keep original filename for reference
                prefix="uploaded_csv_",
            )

            # Write uploaded file content to temporary file
            temp_file.write(await file.read())
            temp_file.close()

            # Get the absolute path of the temporary file
            absolute_file_path = os.path.abspath(temp_file.name)

            return {
                "message": f"File '{file.filename}' uploaded successfully to temporary location",
                "absolute_file_path": absolute_file_path,
                "original_filename": file.filename,
            }
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error uploading file: {str(e)}"
            )

    @staticmethod
    def cleanup_temp_file(file_path: str) -> bool:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def extract_features_from_csv(csv_file):
        try:
            if not os.path.exists(csv_file):
                raise HTTPException(
                    status_code=404, detail=f"CSV file not found: {csv_file}"
                )

            df = pd.read_csv(csv_file)

            label_column = df.columns[-1]  # Last column is the label

            feature_columns = df.columns[
                :-1
            ].tolist()  # All columns except the last one

            return JSONResponse(
                content={
                    "feature_columns": feature_columns,
                    "label_column": label_column,
                }
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
