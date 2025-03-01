from __future__ import annotations
from typing import Optional, Union, Tuple
from wombat.utils.errors.decorators import enforce_type_hints_contracts
from rich.table import Column
from rich.text import Text
from rich import get_console
from rich.progress import (
    Progress,
    TaskID,
    ProgressColumn,
    Task as RichTask,
    SpinnerColumn,
    BarColumn,
    TimeElapsedColumn,
)
from wombat.multiprocessing.models import ProgressUpdate
from wombat.multiprocessing.queues import ModelQueue
from wombat.utils.dictionary import deep_merge
from multiprocessing import Value
import time
from queue import Empty


def tasks_per_second_from_task(task: RichTask, precision: int):
    # Extract ProgressUpdate from task.fields
    if not task or (not task.elapsed) or (task.elapsed == 0):
        return None

    return round(
        0 if task.completed == 0 else (task.completed / task.elapsed),
        precision,
    )


class TimeRemainingColumn(ProgressColumn):
    """Renders estimated time remaining.

    Args:
        compact (bool, optional): Render MM:SS when time remaining is less than an hour. Defaults to False.
        elapsed_when_finished (bool, optional): Render time elapsed when the task is finished. Defaults to False.
    """

    max_refresh = 0.5

    @enforce_type_hints_contracts
    def __init__(self, compact: bool = False, table_column: Optional[Column] = None):
        self.compact = compact
        super().__init__(table_column=table_column)

    @enforce_type_hints_contracts
    def render(self, task: RichTask) -> Text:
        """Show time remaining."""
        style = "progress.remaining"

        if (
            not task
            or not task.total
            or task.total == 0
            or not task.completed
            or task.completed == 0
            or not task.elapsed
            or task.elapsed == 0
        ):
            return Text("--:--" if self.compact else "-:--:--", style=style)

        tasks_per_second: float | None = tasks_per_second_from_task(task, 2)

        if not tasks_per_second:
            return Text("--:--" if self.compact else "-:--:--", style=style)

        remaining_tasks: int = int(task.total - task.completed)

        estimated_time_remaining = remaining_tasks / tasks_per_second
        minutes, seconds = divmod(round(estimated_time_remaining), 60)
        hours, minutes = divmod(minutes, 60)

        if self.compact and not hours:
            formatted = f"{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{hours:d}:{minutes:02d}:{seconds:02d}"

        return Text(formatted, style=style)


class ItemsPerMinuteColumn(ProgressColumn):
    """Renders tasks per minute."""

    max_refresh = 0.5

    def __init__(self, precision: int = 2, table_column: Optional[Column] = None):
        super().__init__(table_column=table_column)
        self.precision = precision

    def render(self, task: RichTask) -> Text:
        """Show tasks per minute."""
        style = "progress.remaining"

        # Extract ProgressUpdate from task.fields
        if not task or (not task.elapsed) or (task.elapsed == 0):
            return Text("?/s", style=style)
        tasks_per_minute = tasks_per_second_from_task(task, self.precision) * 60
        return Text(f"{tasks_per_minute:.2f}/m", style=style)


def create_progress_bars(num_bars) -> Tuple[Progress, TaskID]:
    console = get_console()
    progress_bar = Progress(
        SpinnerColumn(),
        "{task.fields[status]}...",
        BarColumn(),
        "{task.completed} of {task.total}",
        "[red]❌: {task.fields[failures]}",
        "[yellow]🔃: {task.fields[retries]}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        ItemsPerMinuteColumn(),
        console=console,
        auto_refresh=True,
    )
    tasks = []
    for bar in range(num_bars):
        tasks.append(
            progress_bar.add_task(
                description=f"Worker-{bar}",
                start=True,
                total=0,
                completed=0,
                visible=True,
                status="Starting...",
                failures=0,
                retries=0,
            )
        )
    return progress_bar, tasks


@enforce_type_hints_contracts
def add(a: Union[int, float], b: Union[int, float, None]) -> Union[int, float]:
    if b is None:
        return a
    return a + b


def merge_progress(progress: ProgressUpdate, update: ProgressUpdate) -> ProgressUpdate:
    strategies = {
        k: add if isinstance(v, (int, float)) and k != "task_id" else "override"
        for k, v in progress
    }
    return ProgressUpdate.model_validate(
        obj=deep_merge(
            progress.model_dump(),
            update.model_dump(exclude_none=True),
            strategies=strategies,
        )
    )


def run_progress(
    queue: ModelQueue,
    num_bars: int,
    total_progress_tasks: Value,
    remaining_progress_tasks: Value,
):
    progress_bar, task_ids = create_progress_bars(num_bars=num_bars)
    processed_tasks: int = 0
    total_task_id = progress_bar.add_task(
        description="Total",
        start=True,
        total=0,
        completed=0,
        visible=True,
        status="Starting...",
        failures=0,
        retries=0,
    )
    task_ids.append(total_task_id)
    progress = {task_id: ProgressUpdate(task_id=task_id) for task_id in task_ids}
    try:
        progress_bar.start()
        while True:
            try:
                update = queue.get(block=False)
                queue.task_done()

                progress_update: ProgressUpdate | None = update.kwargs.get("update")

                if not progress_update:
                    return
                processed_tasks += 1
                with remaining_progress_tasks.get_lock():
                    with total_progress_tasks.get_lock():
                        remaining_progress_tasks.value = (
                            total_progress_tasks.value - processed_tasks
                        )
                    if (
                        progress_update.total == -1
                        and remaining_progress_tasks.value == 0
                    ):
                        break

                task_ids_to_update = set()
                for task_id in set([progress_update.task_id]):
                    if task_id == -1:
                        task_ids_to_update.add(total_task_id)
                    else:
                        task_ids_to_update.add(task_id)

                for task_id in task_ids_to_update:
                    progress[task_id] = merge_progress(
                        progress[task_id], progress_update
                    )
                    progress[task_id].elapsed = (
                        progress_bar.get_time() - progress_bar.tasks[task_id].start_time
                    )
                    progress_bar.update(
                        task_id,
                        total=progress[task_id].total,
                        completed=progress[task_id].completed,
                        status=progress[task_id].status,
                        elapsed=progress[task_id].elapsed,
                        failures=progress[task_id].failures,
                        retries=progress[task_id].retries,
                        remaining=progress[task_id].remaining,
                    )

                    if total_task_id not in task_ids_to_update:
                        # Partial merge, e.g. some fields lile total should be added
                        total = progress[total_task_id].total
                        status = progress[total_task_id].status
                        progress[total_task_id] = merge_progress(
                            progress[total_task_id], progress_update
                        )
                        progress[total_task_id].total = total
                        progress[total_task_id].status = status
                        progress[total_task_id] = ProgressUpdate(
                            task_id=total_task_id,
                            total=progress[total_task_id].total,
                            completed=progress[total_task_id].completed,
                            status=progress[total_task_id].status,
                            failures=progress[total_task_id].failures,
                            retries=progress[total_task_id].retries,
                            remaining=progress[total_task_id].remaining,
                            elapsed=progress[total_task_id].elapsed,
                        )
                        progress_bar.update(
                            total_task_id,
                            total=progress[total_task_id].total,
                            completed=progress[total_task_id].completed,
                            status=progress[total_task_id].status,
                            elapsed=progress[total_task_id].elapsed,
                            failures=progress[total_task_id].failures,
                            retries=progress[total_task_id].retries,
                            remaining=progress[total_task_id].remaining,
                        )
                progress_bar.refresh()
            except Empty:
                time.sleep(0.1)
                continue
            except OSError:
                break
            except ValueError:
                break
    finally:
        progress_bar.refresh()
        progress_bar.stop()


# Write a function that takes a and b which are two instances of ProgressUpdate and diff them returning the number of changed keys
def diff_progress(a: ProgressUpdate, b: ProgressUpdate) -> int:
    result = deep_merge(
        a.model_dump(),
        b.model_dump(exclude_none=True),
        {k: lambda b, a: a - b for k, v in a if isinstance(v, (int, float))},
    )
    del result["status"]
    return result
