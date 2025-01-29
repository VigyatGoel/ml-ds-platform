import os

from fastapi import HTTPException

from ...datascience.data_summary import DataSummary


class DataSummaryService:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._validate_file()
        self.data_summary = DataSummary(file_path=file_path)

    def _validate_file(self):
        if not os.path.exists(self.file_path):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {self.file_path}")

    def get_file_info_service(self):
        try:
            file_name, file_size_mb = self.data_summary.get_file_info()
            return {"file_name": file_name, "file_size_MB": round(file_size_mb, 4)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_data_description_service(self):
        try:
            return self.data_summary.get_data_description().to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_data_info_service(self):
        try:
            from io import StringIO
            buffer = StringIO()
            self.data_summary.get_data_info(buffer)
            return {"data_info": buffer.getvalue()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_data_types_service(self):
        try:
            return self.data_summary.get_data_types().astype(str).to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_categorical_columns_count_service(self):
        try:
            return self.data_summary.get_categorical_columns_count().to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_row_col_count_service(self):
        try:
            rows, cols = self.data_summary.get_row_col_count()
            return {"rows": rows, "columns": cols}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_null_val_count_service(self):
        try:
            missing_values, missing_percentage = self.data_summary.get_null_val_count()
            return {
                "missing_values": missing_values.to_dict(),
                "missing_percentage": missing_percentage.round(4).to_dict(),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
