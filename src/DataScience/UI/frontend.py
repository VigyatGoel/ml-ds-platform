import streamlit as st

from src.DataScience.Plots.plots import Plot

# Add the project root directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

plots = Plot()
try:
    scatter_plot = plots.construct_scatter_plot(
        "src/DataScience/UI/iris.csv", "petal_width", "sepal_width")
    st.plotly_chart(figure_or_data=scatter_plot)
except Exception as e:
    st.error(f"An error occurred: {e}")
