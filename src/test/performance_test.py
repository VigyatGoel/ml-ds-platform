import asyncio
import time

import httpx


async def send_requests(client, url):
    # Send a single HTTP GET request
    response = await client.get(url)
    return response.status_code


async def simulate_load(url, num_requests=100):
    async with httpx.AsyncClient(verify=False) as client:
        tasks = [send_requests(client, url) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

        # Print the status codes of the responses
        for response in responses:
            print(response)  # You can modify this to log or process responses


# URL of your FastAPI app
url = "https://140.238.255.45/data_science/correlation_matrix?csv_file=../datascience/plots/iris.csv"

# Start the simulation with 100 concurrent requests
start_time = time.time()
asyncio.run(simulate_load(url, num_requests=10))
end_time = time.time()

print(f"Completed 10 requests in {end_time - start_time:.2f} seconds")
