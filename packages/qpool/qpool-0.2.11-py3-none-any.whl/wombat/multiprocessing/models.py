### This file contains the models that we composite to represent our Tasks and their behaviors
from __future__ import annotations
from uuid import uuid4
from typing import (
    List,
    Any,
    Optional,
    Dict,
    Callable,
)
from pydantic import BaseModel, Field, UUID4, ConfigDict
from enum import Enum
from wombat.utils.errors.decorators import enforce_type_hints_contracts
import logging
from pydantic_partial import create_partial_model
from contextlib import AsyncExitStack

@enforce_type_hints_contracts
def simple_backoff(
    retries: int, initial_delay: float | int, max_delay: float | int
) -> float:
    """Simple backoff function. Same delay for each retry until max_delay is reached."""
    return min(max_delay, initial_delay * retries)


@enforce_type_hints_contracts
def exponential_backoff(
    retries: int,
    initial_delay: float | int,
    max_delay: float | int,
    multiplier: float | int,
) -> float:
    """Exponential backoff function. Delay increases exponentially with each retry until max_delay is reached."""
    return min(max_delay, initial_delay * (multiplier**retries))


class ResultTaskPair(BaseModel):
    """This represents a tuple of a task and a result."""

    task: Actionable | Sentinel
    result: Any

    def __init__(self, task: Actionable | Sentinel, result: Any) -> None:
        if isinstance(task, Actionable):
            # Remove props from the kwargs of the task
            task.kwargs = {k: v for k, v in task.kwargs.items() if k != "props"}
        super().__init__(task=task, result=result)

    def __str__(self) -> str:
        return f"{self.task} => {self.result}"


class Trackable(BaseModel):
    path: List[str]

    def track(self, action: str):
        self.path.append(action)


class Loggable(BaseModel):
    """Mixin that provides a log_level for tasks which should yield log events during their execution."""

    log_level: int = logging.INFO


class Identifiable(BaseModel):
    """Mixin that provides an id field with a default value of a new UUID4."""

    id: UUID4 = Field(default_factory=lambda: uuid4())


class Actionable(BaseModel):
    """Mixin that indicates a task maps to a prepared function and provides an action field."""

    action: str = Field(
        ...,
        description="The action to be performed by the task. Expected to map to a key in the Workers Action dictionary.",
    )


class Sentinel(BaseModel):
    """Mixin that provides a sentinel field for tasks that should not be executed."""

    sentinel: str


class PositionalActionable(Actionable):
    """Mixin that provides a list of positional arguments for an actionable task."""

    args: List[Any] = []


class KeywordActionable(Actionable):
    """Mixin that provides a dictionary of keyword arguments for an actionable task."""

    kwargs: Dict[str, Any] = {}


class MixedActionable(PositionalActionable, KeywordActionable):
    """Mixin that allows both positional and keyword arguments for an actionable task."""

    pass


class TaskState(Enum):
    """Enumeration of possible task states over the course of a Task lifecycle."""

    create = "create"  # Task has been created but not yet queued
    queue = "queue"  # Task has been queued
    attempt = "attempt"  # Task is being attempted
    retry = "retry"  # Task is being retried according to its retry policy
    fail = "fail"  # Task has failed completely
    success = "success"  # Task has completed successfully


class Lifecycle(BaseModel):
    """Mixin that provides a status field for task lifecycle tracking."""

    status: TaskState = Field(
        default=TaskState.create, description="The current status of the task."
    )


class Progresses(BaseModel):
    """Mixin that provides a progress field for tracking the weighted progress of a task."""

    weight: int = Field(ge=0, default=1)


class Evaluatable(BaseModel):
    evaluator: Optional[Callable[Any, bool]] = None

    def evaluate(self, data: T):
        if self.evaluator:
            return self.evaluator(data)
        else:
            # This is fine, it just means the task is presumed to succeed if it doesn't raise an exception
            return True


class Retryable(Evaluatable, Lifecycle):
    tries: int = Field(
        ge=0, default=0, description="The number of times the task has been attempted."
    )
    max_tries: int = Field(
        ge=0,
        default=3,
        description="The maximum number of times the task can be attempted.",
    )
    initial_delay: float = Field(
        ge=0.0, default=2, description="The initial delay before the first retry."
    )
    max_delay: float = Field(
        ge=0.0, default=60.0, description="The maximum delay between retries."
    )

    def remaining(self) -> int:
        """Calculate the number of remaining retries.

        Returns:
            int: The number of remaining retries.
        """
        return max(0, self.max_tries - self.tries)

    def attempt(self):
        self.status = TaskState.attempt
        if self.tries < self.max_tries:
            self.status = TaskState.retry
            self.tries += 1
        else:
            self.status = TaskState.fail

    def backoff(self):
        return exponential_backoff(self.tries, self.initial_delay, self.max_delay, 2.0)


class Prop(BaseModel):
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True,
    )
    initializer: Any | Callable[[], Any] = Field(description="The function that initializes the prop. This will be called at the start of the worker in the context of the worker. MUST BE PICKLABLE.")
    instance: Any = Field(description="The resolved instance of the prop. This will be stored on the worker and passed to tasks.", default=None)
    exit_stack: Optional[AsyncExitStack] = Field(description="The exit stack that the prop is registered with. This will be used to close the prop when the worker is done. If None, then the workers exit stack is used.", default=None)
    use_context_manager: bool = Field(description="Whether the prop should be used as a context manager. If True, the prop will be closed when the worker is done. If false tasks are responsible for resource cleanup.", default=True)

UninitializedProp = create_partial_model(Prop, "instance")

class RequiresProps(BaseModel):
    """Mixin that provides a requires_props field for tasks that require specific props to be passed to them by their worker."""

    requires_props: List[str] = Field(
        default_factory=list,
        description="A list of required props that the task expects to be passed to it.",
    )
    include_all_props: bool = Field(
        default=False,
        description="Whether to include all props in the kwargs passed to the task or just the required props.",
    )

    def filter_props(self, props: Dict[str, Prop]) -> Dict[str, Any]:
        if self.include_all_props:
            return props
        return {k: v for k, v in props.items() if k in self.requires_props}


class ProgressUpdate(BaseModel):
    task_id: int
    total: int = 0
    completed: int = 0
    elapsed: float = 0.0
    remaining: float = 0.0
    failures: int = 0
    retries: int = 0
    status: str = "created"
