from __future__ import annotations
import asyncio
from uuid import uuid4
from annotated_types import Ge
from collections import deque
from typing import (
    List,
    Any,
    Union,
    Optional,
    Dict,
    Type,
    Callable,
    Annotated,
)
import heapq
from pydantic import BaseModel, UUID4, Field
from multiprocessing import Value, get_context

from contextlib import AsyncExitStack
from queue import Empty
from enum import Enum
from threading import Thread
import inspect
from wombat.multiprocessing.logging import setup_logging, log
from wombat.utils.errors.decorators import enforce_type_hints_contracts
from wombat.utils.dictionary import deep_merge
import logging
import time
from traceback import format_exc

from wombat.multiprocessing.models import (
    Identifiable,
    KeywordActionable,
    PositionalActionable,
    MixedActionable,
    RequiresProps,
    ProgressUpdate,
    Progresses,
    Retryable,
    Lifecycle,
    Actionable,
    TaskState,
    Evaluatable,
    ResultTaskPair,
    Prop,
    UninitializedProp,
)
from wombat.multiprocessing.tasks import (
    LogTask,
    ProgressTask,
    Task,
    ControlTask,
    ExitTask,
    EOQ,
    set_task_status,
)
from wombat.multiprocessing.queues import (
    ModelQueue,
    drain_queue,
    TaskQueue,
    LogQueue,
    ResultQueue,
    ControlQueue,
    ProgressQueue,
    explicitly_is,
    implicitly_is,
    log_task,
)
from wombat.multiprocessing.progress import run_progress, add
from wombat.multiprocessing.utilities import is_async_context_manager, is_sync_context_manager

class WorkerStatus(Enum):
    """Enumeration of possible worker states over the course of a Worker lifecycle."""
    CREATED = 0
    RUNNING = 1
    SLEEPING = 2
    STOPPED = 3
    PAUSED = 4

class Worker:
    def __init__(
        self,
        context: Any,
        actions: Dict[str, Callable],
        control_queues: Dict[str, ModelQueue],
        task_queue: ModelQueue,
        status: Value,
        total_progress_tasks: Optional[Value] = None,
        log_queue: Optional[ModelQueue] = None,
        result_queue: Optional[ModelQueue] = None,
        progress_queue: Optional[ModelQueue] = None,
        props: Optional[Prop] = None,
        name: Optional[str] = None,
        task_id: Optional[int] = -1,
        id: Optional[UUID4] = None,
        get_time: Callable[[], float] = time.monotonic,
        tasks_per_minute_limit: Optional[int] = None,
    ) -> None:
        self.context = context
        self.total_progress_tasks = total_progress_tasks
        self.finished_tasks = self.context.Value("i", 0)
        self.total_tasks = self.context.Value("i", 0)
        self.last_update = None
        self.get_time = get_time
        self.task_timestamps = deque()
        self.tasks_per_minute_limit = tasks_per_minute_limit
        self.start_time = get_time()
        self.id = id if id else uuid4()
        self.name = name if name else f"Worker-{self.id}"
        self.task_id = task_id
        self.control_queues = control_queues
        self.task_queue = task_queue
        self.log_queue = log_queue
        self.result_queue = result_queue
        self.retries = []
        self.progress = ProgressUpdate(task_id=self.task_id)
        self.progress_delta = ProgressUpdate(task_id=self.task_id)
        self.progress_queue = progress_queue
        self.is_retrying = False
        self.actions = actions

        self.props = props
        self.status = status

        self._process = self.context.Process(
            target=self.start_event_loop,
            kwargs={"actions": self.actions, "props": self.props},
            name=self.name,
        )

    def update_progress(self, force_update: bool = False):
        update = self.progress_delta.model_dump(exclude_unset=True)
        if self.progress_queue and (
            force_update
            or self.last_update is None
            or self.get_time() - self.last_update > 1
        ):
            self.last_update = self.get_time()
            merged = deep_merge(
                self.progress.model_dump(),
                update,
                strategies={
                    k: add if isinstance(v, (int, float)) else "override"
                    for k, v in self.progress
                },
            )
            self.progress = ProgressUpdate.parse_obj(merged)
            with self.total_progress_tasks.get_lock():
                self.total_progress_tasks.value += 1
            self.progress_queue.put(
                ProgressTask(
                    kwargs={"update": self.progress_delta},
                )
            )
            self.progress_delta = ProgressUpdate(task_id=self.task_id)

    def log(self, message: str, level: int):
        if self.log_queue:
            self.log_queue.put(
                LogTask(action="log", kwargs={"message": message, "level": level})
            )

    def start(self):
        if not self._process.is_alive():
            self.log(f"Starting process for {self.name}", logging.DEBUG)
            self._process.start()
            with self.status.get_lock():
                self.status.value = WorkerStatus.RUNNING.value

    async def execute_task(self, task: Actionable, func, props: Dict[str, Prop], is_async: bool):
        task_is_identifiable = isinstance(task, Identifiable)
        task_has_lifecycle = isinstance(task, Lifecycle)
        task_provides_progress = isinstance(task, Progresses)
        task_can_be_retried = isinstance(task, Retryable)
        task_requires_props = isinstance(task, RequiresProps)
        task_accepts_positional_args = isinstance(task, PositionalActionable)
        task_accepts_keyword_args = isinstance(task, KeywordActionable)
        task_accepts_mixed_args = isinstance(task, MixedActionable)
        task_can_be_evaluated_for_success = isinstance(task, Evaluatable)
        last_exception = None
        result_data = None
        try:
            if task_is_identifiable:
                log_task(
                    queue=self.log_queue,
                    task=task,
                    message=f"Executing task: {task.id}",
                    level=logging.INFO,
                )

            # Extract arguments from the task
            args = task.args if isinstance(task, PositionalActionable) else []
            kwargs = task.kwargs if isinstance(task, KeywordActionable) else {}

            # Handle props if the task requires them
            if task_requires_props:
                if task_accepts_keyword_args or task_accepts_mixed_args:
                    kwargs["props"] = task.filter_props(props=props)
                elif task_accepts_positional_args:
                    args.append(task.filter_props(props=props))

            # TODO: Detect mismatching number of arguments so we can give a better error
            # Execute the function/coroutine
            if is_async:
                if task_is_identifiable:
                    self.log(f"Running async task: {task.id}", logging.INFO)
                coroutine = func(self, *args, **kwargs)
                result_data = await coroutine
            else:
                if task_is_identifiable:
                    self.log(f"Running sync task: {task.id}", logging.INFO)
                result_data = func(self, *args, **kwargs)

            # Evaluate the result
            success = (
                task.evaluate(result_data)
                if task_can_be_evaluated_for_success
                else True
            )

            if not success:
                if task_is_identifiable:
                    log_task(
                        queue=self.log_queue,
                        task=task,
                        message=f"Task {task.id} failed on evaluation.",
                        level=logging.WARNING,
                    )

                set_task_status(task, TaskState.fail)
                return

            set_task_status(task, TaskState.success)

            if self.result_queue:
                if task_is_identifiable:
                    log_task(
                        queue=self.log_queue,
                        task=task,
                        message=f"Task {task.id} succeeded, pushing result to result queue. Result Queue has {self.result_queue.queue.qsize()} items.",
                        level=logging.DEBUG,
                    )

                self.result_queue.put(ResultTaskPair(task=task, result=result_data))
        except Exception as e:
            last_exception = format_exc()
            set_task_status(task, TaskState.fail)
            log_task(
                queue=self.log_queue,
                task=task,
                message=f"Error while executing task {task} with function {func}: {last_exception}",
                level=logging.ERROR,
            )
        finally:
            if task_has_lifecycle:
                if task.status == TaskState.fail:
                    task_can_be_retried = task_can_be_retried and task.remaining() > 0
                    if not task_can_be_retried:
                        if task_is_identifiable:
                            self.log(
                                f"Retries exhausted for task {task.id}", logging.WARNING
                            )
                        with self.finished_tasks.get_lock():
                            self.finished_tasks.value += 1
                        self.progress_delta.failures += 1
                        if self.result_queue:
                            self.result_queue.put(
                                ResultTaskPair(
                                    task=task, result=[last_exception, result_data]
                                )
                            )
                        if self.is_retrying:
                            self.progress_delta.completed += 1
                    else:
                        set_task_status(task, TaskState.retry)

                if task.status == TaskState.retry:
                    self.progress_delta.retries += 1
                    task.attempt()
                    if task.status == TaskState.retry:
                        if task_is_identifiable:
                            self.log(
                                f"Task {task.id} is being retried, {task.remaining()} retries remaining. Backing off...",
                                logging.INFO,
                            )
                        heapq.heappush(
                            self.retries, (self.get_time() + task.backoff(), task)
                        )
                    else:
                        # He's dead, Jim
                        self.progress_delta.failures += 1
                        self.result_queue.put(
                            ResultTaskPair(
                                task=task, result=[last_exception, result_data]
                            )
                        )
                elif task.status == TaskState.success:
                    self.progress_delta.completed += 1
                    with self.finished_tasks.get_lock():
                        self.finished_tasks.value += 1

                if task_provides_progress:
                    self.update_progress()

    def start_event_loop(self, actions: Dict[str, Callable], props: Dict[str, Any]):
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.log(f"Starting event loop for {self.name}:{self._process.pid}", logging.CRITICAL)
            self.loop.run_until_complete(self.run(actions, props=props))
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()


    async def enforce_rate_limit(self):
        """Ensures the worker does not exceed the tasks per minute limit."""
        if self.tasks_per_minute_limit is None:
            return  # No rate limiting

        now = self.get_time()
        one_minute_ago = now - 60

        # Remove timestamps older than 60 seconds
        while self.task_timestamps and self.task_timestamps[0] < one_minute_ago:
            self.task_timestamps.popleft()

        # Get the current limit safely
        with self.tasks_per_minute_limit.get_lock():
            task_limit = self.tasks_per_minute_limit.value

        if len(self.task_timestamps) >= task_limit:
            # Instead of waiting for the full 60 seconds, sleep until the **next** task falls out of the window
            next_allowed_time = self.task_timestamps[0] + 60  # Oldest task falls out
            wait_time = max(0, next_allowed_time - now)

            if wait_time > 0:
                self.log(f"Worker {self.name} is rate-limited, sleeping for {wait_time:.2f} seconds", logging.INFO)
                await asyncio.sleep(wait_time)

    async def initialize_prop(self, props: Dict[str, Prop], prop_name: str, reinitialize: bool = False):
        """ Initializes (or re-initializes) a single prop, while keeping track of the number of initializations.
            Will also enter the prop as a context manager if necessary.

        Args:
            props (Dict[str, Prop]): The props collection to update
            prop_name (str): The name of the prop to initialize within the collection
        """
        try:
            # Get the prop and its current state
            prop = props[prop_name]
            initializer = prop.initializer
            # Get the current value of the prop
            resolved_value = prop.instance if not reinitialize else None

            # ======================================================================== #
            # Certain things are not picklable, to circumvent this we pass pickable
            # functions (either async/sync) and call them in the worker.
            # ======================================================================== #
            if resolved_value is None:
                if asyncio.iscoroutinefunction(initializer):
                    resolved_value = await initializer()
                elif callable(initializer):
                    resolved_value = initializer()

            # ======================================================================== #
            # Context Manager handling
            # - Exit stack is used to manage the lifecycle of the prop
            # - If the prop is a context manager, we enter it here
            # ======================================================================== #
            # Look for an existing exit stack on the prop, or create one if necessary
            exit_stack = prop.exit_stack
            if exit_stack is None and prop.use_context_manager:
                exit_stack = AsyncExitStack()

            prop_is_async_context_manager = is_async_context_manager(resolved_value)
            prop_is_sync_context_manager = is_sync_context_manager(resolved_value) if not prop_is_async_context_manager else (False, None)
            prop_is_context_manager = prop_is_async_context_manager or prop_is_sync_context_manager

            # Enter context manager if necessary
            if prop.use_context_manager:
                if prop_is_context_manager:
                    context_entrypoint = exit_stack.enter_async_context if prop_is_async_context_manager else exit_stack.enter_context
                    resolved_value = context_entrypoint(resolved_value)
                    # Await the entrypoint if necessary, only if it's an async context manager
                    if inspect.isawaitable(resolved_value):
                        resolved_value = await resolved_value
                else:
                    self.log(
                        f"Prop '{prop_name}' is not a context manager. Suggest setting use_context_manager=False.",
                        logging.WARNING
                    )

            # Store final prop
            props[prop_name] = Prop(
                initializer=initializer,
                instance=resolved_value,
                use_context_manager=prop.use_context_manager,
                exit_stack=exit_stack
            )
        except Exception as e:
            self.log(
                f"Worker {self.name} failed to initialize prop {prop_name}: {e}\n{format_exc()}",
                logging.ERROR,
            )
            return e

    async def run(self, actions: Dict[str, Callable], props: Dict[str, Prop]):
        # ======================================================================== #
        # Resolve all props and enter them as context managers if necessary
        # ======================================================================== #
        # Store the props on the worker
        self.props = props if props is not None else {}

        # Async gather all prop initializations
        to_gather = [self.initialize_prop(self.props, prop_name) for prop_name in props.keys()]
        await asyncio.gather(*to_gather)

        try:
            self.log(f"Worker {self.name} is running", logging.INFO)
            with self.status.get_lock():
                self.status.value = WorkerStatus.RUNNING.value
            self.progress_delta.status = f"Starting {self.name}"
            # ======================================================================== #
            # Main worker loop
            # ======================================================================== #
            while True:
                # Indicates if we're currently retrying a task, relevant as retried tasks are not in queues and do not require a task_done call
                self.is_retrying = False

                # Grab a failed task to retry if available
                self.progress_delta.status = f"Fetching retry tasks in {self.name}"
                task = None
                if (
                    self.retries
                    and self.retries[0]
                    and self.retries[0][0] <= self.get_time()
                ):
                    self.is_retrying = True
                    retry_time, task = heapq.heappop(self.retries)
                    self.log(
                        f"Worker {self.name} is retrying task {task} from the task queue",
                        logging.INFO,
                    )
                    self.progress_delta.status = f"Retrying task {task.id}"

                self.progress_delta.status = (
                    f"Checking for control tasks in {self.name}"
                )
                # If we didn't get a failed task to retry, try to get a new control task
                if task is None:
                    try:
                        for queue in self.control_queues.values():
                            control_task: Optional[ControlTask] = queue.get(block=False)
                            queue.task_done()
                            if (
                                isinstance(control_task, ExitTask)
                                # and total_tasks == finished_tasks
                            ):
                                self.log(
                                    f"Received exit task in worker {self.name}",
                                    logging.INFO,
                                )
                                with self.status.get_lock():
                                    self.status.value = WorkerStatus.STOPPED.value
                                return
                            else:
                                self.log(
                                    message=f"Worker {self.name} received control task {control_task} but is delaying as the conditions for it's execution are not yet met.",
                                    level=logging.INFO,
                                )
                                queue.put(control_task)
                    except Empty:
                        pass

                self.progress_delta.status = f"Checking for work tasks in {self.name}"
                # If we got neither a failed task to retry nor a control task, try to get a new task
                if task is None:
                    try:
                        task = self.task_queue.get(block=False)
                        if task:
                            self.progress_delta.total += 1
                            with self.total_tasks.get_lock():
                                self.total_tasks.value += 1
                            self.task_queue.task_done()
                    except Empty:
                        pass

                task_is_identifiable = isinstance(task, Identifiable)
                task_is_actionable = isinstance(task, Actionable)

                # If we got a valid non-control task by any means, process it
                if task is not None:
                    # Apply rate limiting before executing a task
                    await self.enforce_rate_limit()
                    self.progress_delta.status = f"Attempting task {task.id}"
                    if task_is_identifiable:
                        self.log(
                            f"Worker {self.name} is attempting task {task.id}",
                            logging.INFO,
                        )
                    # If we have a task that maps to an action, execute it
                    if task_is_actionable:
                        self.active_task = task

                        set_task_status(task, TaskState.attempt)

                        func = self.actions[task.action]
                        await self.execute_task(
                            task=task,
                            func=func,
                            props=self.props,
                            is_async=inspect.iscoroutinefunction(func),
                        )
                        self.task_timestamps.append(self.get_time())
                else:
                    with self.status.get_lock():
                        self.status.value = WorkerStatus.SLEEPING.value
                    # TODO: Make this sleep configurable
                    await asyncio.sleep(0.1)
        except Exception as e:
            self.log(
                f"Worker {self.name} encountered an exception: {e}\n{format_exc()}",
                logging.ERROR,
            )
        finally:
            if self.progress_queue:
                self.progress_delta.status = f"Stopping worker {self.name}"
                self.update_progress(force_update=True)

            for prop in self.props.values():
                if prop.use_context_manager:
                    if prop.exit_stack is not None:
                        await prop.exit_stack.aclose()

            if self.result_queue:
                self.result_queue.queue.put(ResultTaskPair(task=EOQ(), result=None))
