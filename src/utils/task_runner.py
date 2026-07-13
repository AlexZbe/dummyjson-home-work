from typing import Protocol
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor


class TaskRunner(Protocol):
    def run(self, task: Callable, user_id: int, job_id: int) -> None: ...


class ThreadReportTaskRunner:
    def __init__(self, executor: ThreadPoolExecutor):
        self.executor = executor

    def run(self, task: Callable,  user_id: int, job_id: int) -> None:
        self.executor.submit(
            task,
            user_id,
            job_id,
        )
