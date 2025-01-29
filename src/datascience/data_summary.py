import os

import pandas as pd


class DataSummary:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def get_file_info(self):
        file_path = self.file_path
        file_name = os.path.basename(file_path)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return file_name, file_size_mb

    def get_data_description(self):
        return self.df.describe()

    def get_data_info(self, buffer):
        return self.df.info(buf=buffer)

    def get_data_types(self):
        return self.df.dtypes

    def get_categorical_columns_count(self):
        categorical_cols = self.df.select_dtypes(include=['object', 'category'])
        value_counts = categorical_cols.apply(pd.Series.value_counts)
        return value_counts

    def get_row_col_count(self):
        return self.df.shape[0], self.df.shape[1]

    def get_null_val_count(self):
        df = self.df
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / df.shape[0]) * 100
        return missing_values, missing_percentage
