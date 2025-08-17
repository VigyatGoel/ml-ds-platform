import time

import httpx

BASE_URL = "https://140.238.255.45/data_summary"
CSV_FILE_PARAM = {"csv_file": "/app/src/csvfiles/train.csv"}

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


def measure_time():
    with httpx.Client(verify=False, timeout=10) as client:
        start_time = time.time()
        responses = []
        for endpoint in ENDPOINTS:
            response = client.get(f"{BASE_URL}{endpoint}", params=CSV_FILE_PARAM)
            responses.append(response)
        end_time = time.time()
        individual_time = end_time - start_time

        for response in responses:
            if response.status_code != 200:
                print(
                    f"Request to {response.url} failed with status code {response.status_code}"
                )

        if all(response.status_code == 200 for response in responses):
            print("All individual requests were successful.")
        else:
            print("Some individual requests failed.")

        start_time = time.time()
        response = client.get(f"{BASE_URL}{ALL_STATS_ENDPOINT}", params=CSV_FILE_PARAM)
        end_time = time.time()
        all_stats_time = end_time - start_time

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
    measure_time()
