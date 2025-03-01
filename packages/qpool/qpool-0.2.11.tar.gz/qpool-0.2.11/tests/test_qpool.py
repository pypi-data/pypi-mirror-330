from __future__ import annotations
import time
import pytest
import pytest_check as check

from typing import List, Dict
from multiprocessing import cpu_count
from aiohttp import ClientSession
import ssl
import certifi
import aresponses
import asyncio
import aiohttp
from aiohttp.web import BaseRequest
from collections import deque

from wombat.multiprocessing.worker import Worker
from wombat.multiprocessing.orchestrator import Orchestrator
from wombat.multiprocessing.tasks import Task, TaskState, RetryableTask
from wombat.multiprocessing.models import RequiresProps, Prop


# ======================================================================== #
# Helper Functions
# ======================================================================== #


def init_aiohttp_session():
    """Initialize an aiohttp session for workers."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))


async def async_fetch_url(worker: Worker, url: str, props: Dict[str, Prop]):
    """Perform asynchronous fetch using aiohttp."""
    session_prop: Prop = props["aiohttp_session"]
    attempts = props.get("attempts")

    session_instance: ClientSession = session_prop.instance
    try:
        if attempts and attempts.instance is not None and attempts.instance == 0:
            attempts.instance += 1
            raise Exception("We expect this exception!")
        async with session_instance.get(url) as resp:
            return resp.status
    except Exception as e:
        # Call the exit stack
        if session_prop.exit_stack is not None:
            await session_prop.exit_stack.aclose()
        await worker.initialize_prop(props=props, prop_name="aiohttp_session")
        raise e


def fail(worker: Worker):
    """Function that raises an exception."""
    raise Exception("This function always fails.")


# ======================================================================== #
# Shared Configuration
# ======================================================================== #

orchestrator_configs = {
    "async": {
        "actions": {"async_fetch_url": async_fetch_url},
        "props": {
            "aiohttp_session": Prop(
                initializer=init_aiohttp_session,
                instance=None,
                exit_stack=None,
            )
        }
    },
    "fail": {
        "actions": {"fail": fail},
        "props": {},
    },
}

orchestrator_configs["async_with_attempts"] = orchestrator_configs["async"].copy()
orchestrator_configs["async_with_attempts"]["props"]["attempts"] = Prop(
    initializer=0,
    instance=0,
    exit_stack=None,
    use_context_manager=False,
)


# ======================================================================== #
# Task Configuration
# ======================================================================== #


class Fail(Task):
    """Task that always fails."""

    action: str = "fail"


class AsyncFetchUrlTask(Task, RequiresProps):
    """Task for asynchronous URL fetching."""

    action: str = "async_fetch_url"
    requires_props: List[str] = ["aiohttp_session"]

class FailFirstAsyncFetchUrlTask(Task, RequiresProps):
    """Task that fails on the first attempt then succeeds."""

    action: str = "async_fetch_url"
    requires_props: List[str] = ["aiohttp_session", "attempts"]

# ======================================================================== #
# Mock Helper
# ======================================================================== #


def mocked_response(request: BaseRequest):
    time.sleep(1)
    return aresponses.Response(text="OK", status=200)


def setup_mock_responses(aresponses, urls: List[str]):
    """
    Centralize the setup of mock responses for aresponses.

    Args:
        aresponses: The aresponses instance.
        urls: List of URLs to mock.
    """
    for url in urls:
        hostname, path = "picsum.photos", f"/{url.split('/')[-1]}"
        aresponses.add(
            hostname,
            path,
            "GET",
            response=mocked_response,
        )


# ======================================================================== #
# Tests
# ======================================================================== #
@pytest.mark.asyncio
async def test_orchestrator_async(aresponses):
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    show_progress = False
    print(f"\nRunning test_orchestrator_async with show_progress={show_progress}...")

    sizes = [100, 200, 300, 400, 500]
    test_urls = [f"https://picsum.photos/{size}" for size in sizes]
    tasks = [AsyncFetchUrlTask(args=[url]) for url in test_urls]

    # Centralize mock response setup
    setup_mock_responses(aresponses, test_urls)

    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=show_progress,
        task_models=[AsyncFetchUrlTask],
        **orchestrator_configs["async_with_attempts"],
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    start_time = time.monotonic()
    await hold
    job_results = orchestrator.stop_workers()
    duration = time.monotonic() - start_time

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), len(sizes), "Expected correct number of results")
    errors = sum(1 for result in job_results if result is None)
    check.equal(errors, 0, "Expected no errors in async approach")
    # Ensure each result is a 200 status code
    check.is_true(all(map(lambda x: x.result == 200, job_results)), "Expected all results to be 200 status codes")


    print(f"Test completed in {duration:.2f} seconds.")


@pytest.mark.asyncio
async def test_repeatedly_finish_tasks():
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_repeatedly_finish_tasks...")

    tasks = [Fail() for _ in range(10)]
    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=False,
        task_models=[Fail],
        **orchestrator_configs["fail"],  # Inject shared actions and props
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    await hold
    # Finish the work
    orchestrator.finish_tasks()
    job_results = list(orchestrator.get_results())

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), 10, "Expected correct number of results")
    failures = [result.task.status == TaskState.fail for result in job_results]
    check.is_true(all(failures), "Expected all tasks to fail")
    # Ensure each result is the result of the fail function
    check.is_true(all(map(lambda x: "Exception: This function always fails." in x.result[0], job_results)), "Expected all results to be the result of the fail function")

    # ======================================================================== #
    # D) Repeat the process
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    await hold
    # Finish the work
    orchestrator.finish_tasks()
    job_results = list(orchestrator.get_results())
    orchestrator.stop_workers()

    # ======================================================================== #
    # E) Validate results
    # ======================================================================== #
    check.equal(len(job_results), 10, "Expected correct number of results")
    failures = [result.task.status == TaskState.fail for result in job_results]
    check.is_true(all(failures), "Expected all tasks to fail")
    # Ensure each result is the result of the fail function
    check.is_true(all(map(lambda x: "Exception: This function always fails." in x.result[0], job_results)), "Expected all results to be the result of the fail function")

@pytest.mark.asyncio
async def test_orchestrator_failure():
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_orchestrator_failure...")

    tasks = [Fail() for _ in range(10)]

    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=False,
        task_models=[Fail],
        **orchestrator_configs["fail"],  # Inject shared actions and props
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    await hold
    job_results = orchestrator.stop_workers()

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), 10, "Expected correct number of results")
    failures = [result.task.status == TaskState.fail for result in job_results]
    check.is_true(all(failures), "Expected all tasks to fail")
    # Ensure each result is the result of the fail function
    check.is_true(all(map(lambda x: "Exception: This function always fails." in x.result[0], job_results)), "Expected all results to be the result of the fail function")


@pytest.mark.asyncio
async def test_add_tasks_of_wrong_model():
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_add_tasks_of_wrong_model...")

    tasks = [AsyncFetchUrlTask(args=[None])]

    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=False,
        task_models=[Fail],
        **orchestrator_configs["fail"],  # Inject shared actions and props
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    enqueue_failures = await orchestrator.add_tasks(tasks)
    check.equal(len(enqueue_failures), 1, "Expected one enqueue failure")
    job_results = orchestrator.stop_workers()

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), 0, "Expected correct number of results")


@pytest.mark.asyncio
@pytest.mark.parametrize("show_progress", [True, False])
async def test_performance(aresponses, show_progress: bool):
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_performance_comparison...")

    sizes = [[100] * 50, [200] * 50, [300] * 50, [400] * 50, [500] * 50]
    sizes = [item for sublist in sizes for item in sublist]
    test_urls = [f"https://picsum.photos/{size}" for size in sizes]
    tasks = [AsyncFetchUrlTask(args=[url]) for url in test_urls]
    results = {}

    # Centralize mock response setup
    setup_mock_responses(aresponses, test_urls)

    # ======================================================================== #
    # B) Baseline: synchronous fetching
    # ======================================================================== #
    start_time = time.monotonic()
    exceptions = 0
    for url in test_urls:
        try:
            async with init_aiohttp_session() as session:
                async with session.get(url) as resp:
                    text = await resp.text()
                    check.equal("OK", text, "Expected OK response")
                    check.equal(200, resp.status, "Expected 200 status")
        except Exception as e:
            print(f"Baseline error fetching {url}: {e}")
            exceptions += 1
    check.equal(exceptions, 0, "Expected no exceptions in baseline")
    baseline_duration = time.monotonic() - start_time

    results["no_pool"] = {
        "duration": baseline_duration,
        "items_per_second": len(test_urls) / baseline_duration,
    }

    # ======================================================================== #
    # C) Async Orchestrator
    # ======================================================================== #
    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=show_progress,
        task_models=[AsyncFetchUrlTask],
        **orchestrator_configs["async"],
    )

    hold = orchestrator.add_tasks(tasks)
    start_time_pool = time.monotonic()
    await hold
    job_results = orchestrator.stop_workers()
    pool_duration = time.monotonic() - start_time_pool

    # ======================================================================== #
    # D) Validate results
    # ======================================================================== #
    check.equal(len(job_results), len(test_urls), "Expected correct number of results")
    exceptions = sum(1 for result in job_results if result is None)
    check.equal(exceptions, 0, "Expected no errors in pooled approach")

    results["pool"] = {
        "duration": pool_duration,
        "items_per_second": len(test_urls) / pool_duration,
    }

    # ======================================================================== #
    # E) Compare Results
    # ======================================================================== #
    for config, result in results.items():
        duration = result["duration"]
        ips = result["items_per_second"]
        speedup = baseline_duration / duration
        print(
            f"{config}: {duration:.2f} seconds, {ips:.2f} items/s, "
            f"{speedup:.2f}x speedup from baseline"
        )

    check.greater(
        results["pool"]["items_per_second"],
        results["no_pool"]["items_per_second"],
        "Expected the pooled approach to outpace the baseline",
    )


class RetryTask(RetryableTask):
    """Task that always fails and retries."""

    action: str = "fail"
    max_tries: int = 3


@pytest.mark.asyncio
async def test_task_retry(aresponses):
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_task_retry...")

    tasks = [RetryTask() for _ in range(10)]

    orchestrator = Orchestrator(
        num_workers=cpu_count(),
        show_progress=False,
        task_models=[RetryTask],
        **orchestrator_configs["fail"],  # Inject shared actions and props
    )
    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    await hold
    job_results = orchestrator.stop_workers()

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), 10, "Expected correct number of results")
    failures = [result.task.status == TaskState.fail for result in job_results]
    check.is_true(all(failures), "Expected all tasks to fail")
    retries = [result.task.tries == 3 for result in job_results]
    check.is_true(all(retries), "Expected all tasks to retry 3 times")

@pytest.mark.parametrize(
    "rate_cut_factor", [
        1,
        2,
        4
    ]
)
@pytest.mark.asyncio
async def test_rate_limiting(aresponses, rate_cut_factor):
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_rate_limiting...")

    sizes = [
        *([100]*10),
        *([200]*10),
        *([300]*10),
        *([400]*10),
        *([500]*10),
    ]
    test_urls = [f"https://picsum.photos/{size}" for size in sizes]
    tasks = [AsyncFetchUrlTask(args=[url]) for url in test_urls]

    # Centralize mock response setup
    setup_mock_responses(aresponses, test_urls)

    tasks_per_minute_limit: int = len(tasks) // rate_cut_factor
    orchestrator = Orchestrator(
        num_workers=4,
        show_progress=True,
        task_models=[AsyncFetchUrlTask],
        tasks_per_minute_limit = tasks_per_minute_limit,
        **orchestrator_configs["async"],
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    enqueue_failures = await orchestrator.add_tasks(tasks)
    start_time = time.monotonic()
    job_results = orchestrator.stop_workers()
    duration = time.monotonic() - start_time

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    # Calculate the number of actual tasks per minute vs expected
    tasks_per_minute = (len(tasks) / duration) * 60
    check.less(tasks_per_minute, tasks_per_minute_limit * 1.10, r"Expected tasks per minute to be less than the 110% limit")
    print(f"Tasks per minute: {tasks_per_minute:.2f} (limit: {tasks_per_minute_limit})")
    check.greater(tasks_per_minute, tasks_per_minute_limit * 0.9, r"Expected tasks per minute to be at least 95% of the limit")

    # Check that the number of results is equal to the number of tasks
    check.equal(len(job_results), len(test_urls), "Expected correct number of results")
    errors = sum(1 for result in job_results if result is None)
    check.equal(errors, 0, "Expected no errors in async approach")

@pytest.mark.asyncio
async def test_rate_limiting_with_retry(aresponses):
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    print("\nRunning test_rate_limiting_with_retry...")
    num_tries = RetryTask().max_tries
    tasks = [RetryTask(initial_delay=0, max_delay=0) for _ in range(10)]

    tasks_per_minute_limit: int = len(tasks)
    orchestrator = Orchestrator(
        num_workers=4,
        show_progress=True,
        task_models=[RetryTask],
        tasks_per_minute_limit = tasks_per_minute_limit,
        **orchestrator_configs["fail"],
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = orchestrator.add_tasks(tasks)
    start_time = time.monotonic()
    await hold
    job_results = orchestrator.stop_workers()
    duration = time.monotonic() - start_time

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    # Calculate the number of actual tasks per minute vs expected, 1 + num_tries to count for the initial task
    tasks_per_minute = (len(tasks) * (1+num_tries) / duration) * 60
    check.less(tasks_per_minute, tasks_per_minute_limit * 1.20, r"Expected tasks per minute to be less than the 120% limit")
    print(f"Tasks per minute: {tasks_per_minute:.2f} (limit: {tasks_per_minute_limit})")
    check.greater(tasks_per_minute, tasks_per_minute_limit * 0.8, r"Expected tasks per minute to be at least 80% of the limit")

    # Check that the number of results is equal to the number of tasks
    check.equal(len(job_results), len(tasks), "Expected correct number of results")
    errors = sum(1 for result in job_results if result is None)
    check.equal(errors, 0, "Expected no errors in async approach")

class RetryableAsyncFetchUrlTask(RetryableTask, RequiresProps):
    """Task for asynchronous URL fetching."""

    action: str = "async_fetch_url"
    requires_props: List[str] = ["aiohttp_session"]


# Write a test to prove the connection can recover from a failure and retry
@pytest.mark.asyncio
async def test_connection_recovery(aresponses):
    sizes = [100,100]
    test_urls = [f"https://picsum.photos/{size}" for size in sizes]

    tasks = [RetryableAsyncFetchUrlTask(args=[url]) for url in test_urls]

    orchestrator = Orchestrator(
        num_workers=1,
        show_progress=False,
        task_models=[RetryableAsyncFetchUrlTask],
        **orchestrator_configs["async"],
    )

    setup_mock_responses(aresponses, test_urls)

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    hold = await orchestrator.add_tasks(tasks)
    start_time = time.monotonic()
    job_results = orchestrator.stop_workers()
    duration = time.monotonic() - start_time

    # ======================================================================== #
    # C) Validate results
    # ======================================================================== #
    check.equal(len(job_results), len(test_urls), "Expected correct number of results")
    # Ensure each result is a 200 status code
    for result in job_results:
        check.equal(result.result, 200, "Expected 200 status code")

    errors = sum(1 for result in job_results if result is None)
    check.equal(errors, 0, "Expected no errors after recovery")

    print(f"Test completed in {duration:.2f} seconds.")