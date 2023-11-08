from ray import serve
from fastapi import FastAPI
from pydantic import BaseModel
from app.monte import ProgressActor, sampling_task
from time import perf_counter
import ray
import time

class DoubleItem(BaseModel):
    input_value: float

class MonteItem(BaseModel):
        samples: int

# Define a FastAPI app & wrap it in a deployment with a route handler.
app = FastAPI(
    title="Test API",
    description="API Test",
    version="0.1.0"
)

@serve.deployment
@serve.ingress(app)
class TestAPI:
    @app.get("/")
    async def root(self):
        return "Welcome to the API"

    @app.post("/double")
    async def double(self, request: DoubleItem):
        t1_start = perf_counter()
        input_value = request.input_value
        double_obj = {"value_double": input_value*2}
        t1_stop = perf_counter()
        elapsed_time = t1_stop-t1_start
        # Add to the response object
        double_obj["elapsed_time"] = elapsed_time
        return double_obj

    @app.post("/monte-carlo")
    async def monte_carlo(self, request: MonteItem):
        t1_start = perf_counter()
        # A compute intensive workload for testing
        NUM_SAMPLING_TASKS = request.samples
        NUM_SAMPLES_PER_TASK = 10_000_000
        TOTAL_NUM_SAMPLES = NUM_SAMPLING_TASKS * NUM_SAMPLES_PER_TASK
        # Create the progress actor.
        progress_actor = ProgressActor.remote(TOTAL_NUM_SAMPLES)
        # Create and execute all sampling tasks in parallel.
        results = [
            sampling_task.remote(NUM_SAMPLES_PER_TASK, i, progress_actor)
            for i in range(NUM_SAMPLING_TASKS)
        ]
        # Query progress periodically.
        while True:
            progress = ray.get(progress_actor.get_progress.remote())
            print(f"Progress: {int(progress * 100)}%")
            if progress == 1:
                break
            time.sleep(1)
        # Get all the sampling tasks results.
        total_num_inside = sum(ray.get(results))
        pi = (total_num_inside * 4) / TOTAL_NUM_SAMPLES
        t1_stop = perf_counter()
        ret_obj = {
            "pi": pi,
            "elapsed_time_s": t1_stop-t1_start,
            "samples": TOTAL_NUM_SAMPLES,
        }
        return ret_obj

       
app = TestAPI.bind()