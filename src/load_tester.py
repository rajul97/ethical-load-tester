import asyncio
import aiohttp
import time
import matplotlib.pyplot as plt
import pandas as pd
from logger import logger  # ✅ Correct
from config import TARGET_URL, NUM_REQUESTS, CONCURRENT_REQUESTS, DELAY_BETWEEN_REQUESTS, LOG_FILE, CSV_FILE, GRAPH_FILE  # ✅ Correct


data = []

async def send_request(session, url):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            elapsed_time = time.time() - start_time
            data.append(elapsed_time)
            logger.info(f"Status: {response.status}, Response Time: {elapsed_time:.3f} sec")
    except Exception as e:
        logger.error(f"Request failed: {e}")

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(NUM_REQUESTS):
            task = asyncio.create_task(send_request(session, TARGET_URL))
            tasks.append(task)

            if len(tasks) >= CONCURRENT_REQUESTS:
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

        if tasks:
            await asyncio.gather(*tasks)

    save_results()
    generate_report()

def save_results():
    df = pd.DataFrame(data, columns=["Response Time (s)"])
    df.to_csv(CSV_FILE, index=False)

def generate_report():
    plt.figure(figsize=(10, 5))
    plt.plot(data, marker="o", linestyle="-", color="b", label="Response Time")
    plt.xlabel("Request Number")
    plt.ylabel("Response Time (s)")
    plt.title("Load Test Response Times")
    plt.legend()
    plt.grid()
    plt.savefig(GRAPH_FILE)
    plt.show()

if __name__ == "__main__":
    logger.info("🚀 Starting ethical load test...")
    asyncio.run(load_test())
    logger.info("✅ Load test completed!")
