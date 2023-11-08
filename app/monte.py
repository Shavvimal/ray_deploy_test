import ray
import math
import time
import random

@ray.remote
class ProgressActor:
    """
    Next, we define a Ray actor that can be called by sampling tasks to update progress. Ray actors are essentially
    stateful services that anyone with an instance (a handle) of the actor can call its methods.
    """
    def __init__(self, total_num_samples: int):
        self.total_num_samples = total_num_samples
        self.num_samples_completed_per_task = {}

    def report_progress(self, task_id: int, num_samples_completed: int) -> None:
        self.num_samples_completed_per_task[task_id] = num_samples_completed

    def get_progress(self) -> float:
        return (
            sum(self.num_samples_completed_per_task.values()) / self.total_num_samples
        )

@ray.remote
def sampling_task(num_samples: int, task_id: int,
                  progress_actor: ray.actor.ActorHandle) -> int:
    """
    After our actor is defined, we now define a Ray task that does the sampling up to num_samples and returns the
    number of samples that are inside the circle. Ray tasks are stateless functions. They execute asynchronously,
    and run in parallel.

    :param num_samples:
    :param task_id:
    :param progress_actor:
    :return:
    """
    num_inside = 0
    for i in range(num_samples):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if math.hypot(x, y) <= 1:
            num_inside += 1

        # Report progress every 1 million samples.
        if (i + 1) % 1_000_000 == 0:
            # This is async.
            progress_actor.report_progress.remote(task_id, i + 1)

    # Report the final progress.
    progress_actor.report_progress.remote(task_id, num_samples)
    return num_inside
