from functools import wraps

from fastapi import HTTPException

from ...datascience.data_summary import DataSummary


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


class DataSummaryService:
    def __init__(self, file_path: str):
        self.data_summary = DataSummary(file_path)

    @handle_exceptions
    async def get_file_info_service(self):
        file_name, file_size_mb = await self.data_summary.get_file_info()
        return {"file_name": file_name, "file_size_MB": file_size_mb}

    @handle_exceptions
    async def get_data_description_service(self):
        result = await self.data_summary.get_data_description()
        return result.to_dict()

    @handle_exceptions
    async def get_data_info_service(self):
        data_info = await self.data_summary.get_data_info()
        return {"data_info": data_info}

    @handle_exceptions
    async def get_data_types_service(self):
        result = await self.data_summary.get_data_types()
        return result.to_dict()

    @handle_exceptions
    async def get_categorical_columns_count_service(self):
        result = await self.data_summary.get_categorical_columns_count()
        return result.to_dict()

    @handle_exceptions
    async def get_row_col_count_service(self):
        rows, cols = await self.data_summary.get_row_col_count()
        return {"rows": rows, "columns": cols}

    @handle_exceptions
    async def get_null_val_count_service(self):
        missing_values, missing_percentage = await self.data_summary.get_null_val_count()
        return {
            "missing_values": missing_values.to_dict(),
            "missing_percentage": missing_percentage.round(4).to_dict(),
        }
