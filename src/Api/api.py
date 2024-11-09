from fastapi import FastAPI

from ..DataScience.Plots.plots import Plot

app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "program_name": "ML Platform",
        "version": "0.1"
    }


@app.get("/plot")
async def scatter_plot():
    plot = Plot()
    #
    csv_file = "/Users/vigyatgoel/Desktop/Personal_Projects/MachineLearning_Platform/Machine_learning_platform/src/DataScience/Plots/Salary_dataset.csv"
    feature1 = "YearsExperience"
    feature2 = "Salary"
    #
    scatter_plot_data = plot.get_scatter_plot_data(csv_file, feature1, feature2)
    print(scatter_plot_data)

    return scatter_plot_data.to_json(orient='records')
