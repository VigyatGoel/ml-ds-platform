import pandas as pd


class Plot:
    @staticmethod
    def _read_csv(csv_file):
        df = pd.read_csv(csv_file)
        return df

    @staticmethod
    def _scatter_plot(df, feature1, feature2):
        return df[[feature1, feature2]]

    def get_scatter_plot_data(self, csv_file, feature1, feature2):
        df = self._read_csv(csv_file)
        return self._scatter_plot(df, feature1=feature1, feature2=feature2)

    @staticmethod
    def _histogram_plot(df):
        return df

    def get_histogram_plot_data(self, csv_file):
        df = self._read_csv(csv_file)
        return self._histogram_plot(df)

    @staticmethod
    def _line_plot(df, feature1):
        return df[feature1]

    def get_line_plot_data(self, csv_file, feature1):
        df = self._read_csv(csv_file)
        return self._line_plot(df, feature1)

    @staticmethod
    def _correlation_matrix(df):
        numeric_df = df.select_dtypes(include=["number"])
        return numeric_df.corr()

    def get_correlation_matrix_data(self, csv_file):
        df = self._read_csv(csv_file)
        return self._correlation_matrix(df)

    @staticmethod
    def _single_box_plot(df, feature1):
        return df[feature1]

    def get_box_plot_data(self, csv_file, feature1):
        df = self._read_csv(csv_file)
        return self._single_box_plot(df, feature1)

    @staticmethod
    def _pair_plot(df):
        numerical_df = df.select_dtypes(include=["number"])
        return numerical_df

    def get_pair_plot_data(self, csv_file):
        df = self._read_csv(csv_file)
        return self._pair_plot(df)

    @staticmethod
    def _area_plot(df, feature1):
        return df[feature1]

    def get_area_plot_data(self, csv_file, feature1):
        df = self._read_csv(csv_file)
        return self._area_plot(df, feature1)
