import pandas as pd
import plotly.express as px


class Plot:

    @staticmethod
    def _read_csv(csv_file):
        df = pd.read_csv(csv_file)
        return df

    @staticmethod
    def _scatter_plot(df, feature1, feature2):
        scatter_plot = px.scatter(data_frame=df, x=feature1, y=feature2, title="Scatter Plot")
        return scatter_plot

    def construct_scatter_plot(self, csv_file, feature1, feature2):
        df = self._read_csv(csv_file)
        scatter_plot = self._scatter_plot(df, feature1=feature1, feature2=feature2)
        # print("VIGYAT", type(scatter_plot))  # Debug print to check type
        return scatter_plot
