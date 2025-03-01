from __future__ import annotations
from uuid import uuid4
from annotated_types import Ge
from typing import (
    List,
    Any,
    Optional,
    Dict,
    Type,
    Callable,
    Annotated,
)
from multiprocessing import get_context

from threading import Thread
from wombat.multiprocessing.log import setup_logging, log
from wombat.utils.errors.decorators import enforce_type_hints_contracts
import logging
import time

from wombat.multiprocessing.models import (
    ProgressUpdate,
    Actionable,
    TaskState,
    ResultTaskPair,
    UninitializedProp,
)
from wombat.multiprocessing.tasks import (
    LogTask,
    ProgressTask,
    Task,
    ExitTask,
    EOQ,
    set_task_status,
)
from wombat.multiprocessing.queues import (
    drain_queue,
    TaskQueue,
    LogQueue,
    ResultQueue,
    ControlQueue,
    ProgressQueue,
)
from wombat.multiprocessing.progress import run_progress
from wombat.multiprocessing.worker import Worker, WorkerStatus
from typing import Generator

class Orchestrator:
    @enforce_type_hints_contracts
    def __init__(
        self,
        num_workers: Annotated[int, Ge(0)],
        actions: Dict[str, Callable],
        props: Optional[Dict[str, Any]] = None,
        show_progress: bool = False,
        task_models: List[Type[Task]] | None = None,
        tasks_per_minute_limit: Optional[int] = None,
    ):
        task_models = (
            task_models if task_models is not None and len(task_models) > 0 else [Task]
        )
        self.context = get_context("spawn")
        self.tasks_per_minute_limit = self.context.Value("i", tasks_per_minute_limit // num_workers) if tasks_per_minute_limit else None

        self.total_progress_tasks = self.context.Value("i", 0)
        self.total_tasks = 0
        self.props = props if props is not None else {}
        self.started = False
        self.task_queue = TaskQueue(
            context=self.context, name="tasks", models=task_models, joinable=True
        )
        self.log_queue = LogQueue(context=self.context, name="log", joinable=True)
        self.result_queues = {}
        logger_id = uuid4()
        control_queue_name = f"control-{logger_id}"
        self.logger_control_queues = {
            f"{control_queue_name}": ControlQueue(
                context=self.context,
                name=f"{control_queue_name}",
                joinable=True,
            )
        }
        self.worker_control_queues = {}
        self.workers = []
        self.show_progress = show_progress
        self.progress_thread = None
        self.progress_queue = None
        if show_progress:
            self.progress_queue = ProgressQueue(
                context=self.context, name="progress", joinable=True
            )
            self.total_progress_tasks = self.context.Value("i", 0)
            self.remaining_progress_tasks = self.context.Value("i", 0)

        self.worker_states = {
            "logger-{logger_id}": self.context.Value("i", WorkerStatus.CREATED.value)
        }
        self.logger = Worker(
            context=self.context,
            name=f"logger-{logger_id}",
            id=uuid4(),
            status=self.worker_states["logger-{logger_id}"],
            total_progress_tasks=None,
            control_queues={"primary": self.logger_control_queues[control_queue_name]},
            task_queue=self.log_queue,
            actions={"log": log},
            props={"logger": UninitializedProp(initializer=setup_logging, use_context_manager=False)},
        )
        for i in range(num_workers):
            worker_id = uuid4()
            worker_name = f"worker-{i}"
            control_queue_name = f"control-{worker_id}"
            self.worker_states[worker_name] = self.context.Value("i", WorkerStatus.CREATED.value)
            self.worker_control_queues[control_queue_name] = ControlQueue(
                context=self.context, name=control_queue_name, joinable=True
            )
            self.result_queues[f"worker-{i}"] = ResultQueue(
                context=self.context, name=f"worker-{i}-results", joinable=False
            )
            self.workers.append(
                Worker(
                    context=self.context,
                    name=worker_name,
                    id=worker_id,
                    task_id=i,
                    control_queues={
                        "primary": self.worker_control_queues[control_queue_name]
                    },
                    status=self.worker_states[worker_name],
                    log_queue=self.log_queue,
                    task_queue=self.task_queue,
                    result_queue=self.result_queues[f"worker-{i}"],
                    progress_queue=self.progress_queue,
                    total_progress_tasks=self.total_progress_tasks,
                    actions=actions,
                    props=self.props,
                    tasks_per_minute_limit=self.tasks_per_minute_limit
                )
            )

    @enforce_type_hints_contracts
    def update_progress(self, update: ProgressUpdate):
        with self.total_progress_tasks.get_lock():
            self.total_progress_tasks.value += 1
        if self.show_progress and self.progress_queue:
            self.progress_queue.put(
                ProgressTask(
                    kwargs={
                        "update": update,
                    }
                )
            )

    @enforce_type_hints_contracts
    def log(self, message: str, level: int):
        self.log_queue.put(
            LogTask(
                kwargs={
                    "message": message,
                    "level": level,
                }
            )
        )

    async def start_workers(self):
        """Starts workers and optionally monitors progress."""
        self.started = True
        self.logger.start()
        # Start workers
        self.log(
            message=f"Started logger with id {self.logger.id} and name {self.logger.name}",
            level=logging.DEBUG,
        )

        for worker in self.workers:
            worker.start()

        if self.show_progress:
            self.progress_thread = Thread(
                target=run_progress,
                args=(
                    self.progress_queue,
                    len(self.workers),
                    self.total_progress_tasks,
                    self.remaining_progress_tasks,
                ),
                daemon=True,
            )
            self.progress_thread.start()

    def _sum_worker_finished_tasks(self, workers: List[Worker]) -> int:
        total = 0
        for worker in workers:
            with worker.finished_tasks.get_lock():
                total += worker.finished_tasks.value
        return total

    def finish_tasks(self):
        """
        Purpose: Finish currently enqueued tasks but don't prohibit adding more tasks. Allows you to finish currently enqueue tasks and wait for them to finish.

        - Does NOT return until all tasks are finished.
        - Does NOT prevent adding more tasks.
        - Does NOT fetch task results.
        """
        self.log(message="Finishing work", level=logging.INFO)
        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Finishing work",
            )
        )
        total_finished_tasks = self._sum_worker_finished_tasks(self.workers)
        while self.total_tasks != total_finished_tasks:
            self.log(
                message=f"Waiting for results to be processed {self.total_tasks} != {total_finished_tasks}",
                level=logging.DEBUG,
            )
            time.sleep(0.1)
            total_finished_tasks = self._sum_worker_finished_tasks(self.workers)

        # Wait for all workers status to be WorkerState.sleeping state, this should be the case if all tasks are finished
        for worker in self.workers:
            worker_status = None
            with worker.status.get_lock():
                worker_status = worker.status.value
            while worker_status != WorkerStatus.SLEEPING.value:
                self.log(
                    message=f"Waiting for worker {worker.name} to finish tasks",
                    level=logging.DEBUG,
                )
                time.sleep(0.1)
                with worker.status.get_lock():
                    worker_status = worker.status.value

        # Add EOQ tasks to the result queue to signal the end of the queue
        for worker in self.workers:
            worker.result_queue.queue.put(ResultTaskPair(task=EOQ(), result=None))


    def get_results(self) -> Generator[ResultTaskPair, None, None]:
        """Get all results from the workers."""
        self.log(message="Getting results", level=logging.INFO)
        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Getting results",
            )
        )
        for worker in self.workers:
            self.log(
                message=f"Draining results from worker {worker.name}",
                level=logging.DEBUG,
            )
            yield from drain_queue(worker.result_queue)

    def stop_workers(self) -> List[ResultTaskPair]:
        """Stop workers and ensure progress monitoring is stopped properly."""
        self.log(message="Waiting for workers to finish tasks", level=logging.INFO)
        self.finish_tasks()
        self.task_queue.close()
        self.task_queue.join()

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Closing worker control queues",
            )
        )
        self.log(message="Closing worker control queues", level=logging.DEBUG)
        for control_queue in self.worker_control_queues.values():
            control_queue.put(ExitTask())
            control_queue.close()
            control_queue.join()

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Stopping worker processes",
            )
        )
        # Ensure all worker processes are properly terminated
        self.log(message="Joining worker processes", level=logging.INFO)
        results: List[ResultTaskPair] = list(self.get_results())
        for worker in self.workers:
            worker._process.join()
            self.log(message=f"Worker-{worker.id} has exited.", level=logging.DEBUG)

        self.log(message="All workers have exited", level=logging.INFO)

        self.update_progress(
            ProgressUpdate(
                task_id=-1,
                status="Closing final resources...",
            )
        )
        # Stop progress monitoring
        if self.show_progress and self.progress_queue and self.progress_thread:
            self.update_progress(ProgressUpdate(task_id=-1, total=-1))
            self.progress_queue.join()
            self.progress_thread.join()

        # Stop the logger
        self.log_queue.close()
        self.log_queue.join()
        for queue in self.logger_control_queues.values():
            queue.put(ExitTask())
            queue.close()
            queue.join()
        self.logger._process.join()
        return results

    @enforce_type_hints_contracts
    async def add_task(self, task: Task):
        """Add task to the task queue and start workers if not started."""
        self.total_tasks += 1
        await self.add_tasks([task])

    @enforce_type_hints_contracts
    async def add_tasks(self, tasks: List[Actionable]) -> List[Task]:
        """Add task to the task queue and start workers if not started."""
        if not self.started:
            await self.start_workers()

        self.total_tasks += len(tasks)
        enqueue_failures = []
        for task in tasks:
            set_task_status(task, TaskState.queue)
            if not self.task_queue.put(task):
                enqueue_failures.append(task)
        self.total_tasks -= len(enqueue_failures)
        added = len(tasks) - len(enqueue_failures)

        # Update progress if progress monitoring is enabled
        if self.show_progress and self.progress_queue and added:
            self.update_progress(
                ProgressUpdate(
                    task_id=-1,
                    total=len(tasks),
                )
            )
        self.log(
            message=f"Added {added} tasks to the task queue. Remaining: {len(enqueue_failures)}",
            level=logging.DEBUG,
        )
        return enqueue_failures
