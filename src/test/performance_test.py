import asyncio
import httpx
import time

BASE_URL = "http://localhost:8000/data_summary"  # Change this to match your API's URL
CSV_FILE_PARAM = {"csv_file": "/Users/vigyatgoel/Desktop/Personal_Projects/MachineLearning_Platform/Machine_learning_platform/src/csvfiles/train.csv"}  # Adjust as needed

ENDPOINTS = [
    "/file_info",
    "/data_description",
    "/data_info",
    "/data_types",
    "/categorical_columns_count",
    "/row_col_count",
    "/null_value_count",
]

ALL_STATS_ENDPOINT = "/all_stats"


async def measure_time():
    async with httpx.AsyncClient() as client:
        # Measure time for individual requests
        start_time = time.time()
        responses = await asyncio.gather(
            *[client.get(f"{BASE_URL}{endpoint}", params=CSV_FILE_PARAM) for endpoint in ENDPOINTS])
        end_time = time.time()
        individual_time = end_time - start_time

        # Ensure all responses are successful
        if all(response.status_code == 200 for response in responses):
            print("All individual requests were successful.")
        else:
            print("Some individual requests failed.")

        # Measure time for all_stats request
        start_time = time.time()
        response = await client.get(f"{BASE_URL}{ALL_STATS_ENDPOINT}", params=CSV_FILE_PARAM)
        end_time = time.time()
        all_stats_time = end_time - start_time

        # Ensure response is successful
        if response.status_code == 200:
            print("All stats request was successful.")
        else:
            print("All stats request failed.")

        print(f"Total time for individual requests: {individual_time:.4f} seconds")
        print(f"Time for /all_stats request: {all_stats_time:.4f} seconds")

        if all_stats_time < individual_time:
            print("/all_stats is more optimized than separate requests.")
        else:
            print("Separate requests are faster or equal to /all_stats.")


if __name__ == "__main__":
    asyncio.run(measure_time())
