import asyncio
import time
from typing import *  # type: ignore

import pytest

import imy.async_utils

T = TypeVar("T")


_count_concurrent_running = 0


async def _async_generator(n: int) -> AsyncIterable[int]:
    """
    Like `range`, but asynchronous.
    """
    for ii in range(n):
        yield ii


async def _count_concurrent(value: T) -> tuple[T, int]:
    """
    Returns the input value as is, as well as how often this function was
    running concurrently during the invocation. In order for this to work the
    function imposes a small delay.
    """
    global _count_concurrent_running
    _count_concurrent_running += 1

    try:
        await asyncio.sleep(0.1)
        return value, _count_concurrent_running
    finally:
        _count_concurrent_running -= 1


@pytest.mark.asyncio
async def test_collect_basic() -> None:
    result = await imy.async_utils.collect(_async_generator(5))
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_collect_limit_too_high() -> None:
    result = await imy.async_utils.collect(_async_generator(5), limit=10)
    assert result == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_collect_limit_too_low() -> None:
    result = await imy.async_utils.collect(_async_generator(5), limit=3)
    assert result == [0, 1, 2]


@pytest.mark.asyncio
async def test_collect_empty() -> None:
    result = await imy.async_utils.collect(_async_generator(0))
    assert result == []


@pytest.mark.asyncio
async def test_amap_simple() -> None:
    results = [
        ii
        async for ii in imy.async_utils.amap(
            _count_concurrent,
            range(5),
            concurrency=100,
        )
    ]

    for ii, (value, concurrent) in enumerate(results):
        assert value == ii


@pytest.mark.asyncio
async def test_amap_concurrency() -> None:
    results = [
        ii
        async for ii in imy.async_utils.amap(
            _count_concurrent,
            range(5),
            concurrency=2,
        )
    ]

    for ii, (value, concurrent) in enumerate(results):
        assert value == ii
        assert concurrent <= 2


# TODO: Test that `amap` returns exceptions ASAP


@pytest.mark.asyncio
async def test_iterator_to_thread_simple() -> None:
    results = [
        val
        async for val in imy.async_utils.iterator_to_thread(
            range(5),
            batch_size=5,
        )
    ]

    for value_should, value_is in enumerate(results):
        assert value_should == value_is


# TODO: More tests for `iterator_to_thread`


@pytest.mark.asyncio
async def test_multitask_empty() -> None:
    """
    Calls `imy.async_utils.multitask` without any tasks. This should
    immediately.
    """
    start_time = time.monotonic()

    await imy.async_utils.multitask()

    end_time = time.monotonic()
    assert end_time - start_time < 0.1


@pytest.mark.asyncio
async def test_multitask_concurrency() -> None:
    """
    Runs several functions via `imy.async_utils.multitask` and ensures that they
    run concurrently.
    """

    async def _slow_function() -> None:
        await asyncio.sleep(0.1)

    start_time = time.monotonic()

    await imy.async_utils.multitask(
        _slow_function(),
        _slow_function(),
        _slow_function(),
    )

    end_time = time.monotonic()
    assert end_time - start_time < 0.2


@pytest.mark.asyncio
async def test_multitask_exception() -> None:
    """
    Tests that `imy.async_utils.multitask` cancels all futures if an exception
    occurs and that the exception is re-raised.
    """

    async def raising_function() -> None:
        await asyncio.sleep(0.1)
        raise ValueError("Test")

    # Start the raising function as well as a much slower one. The exception
    # should be raised, and the whole thing return much faster than if the
    # slow function had been allowed to finish.
    start_time = time.monotonic()

    with pytest.raises(ValueError):
        await imy.async_utils.multitask(
            raising_function(),
            asyncio.sleep(1),
        )

    end_time = time.monotonic()
    assert end_time - start_time < 0.2


@pytest.mark.asyncio
async def test_to_daemon_thread_with_args() -> None:
    """
    Make sure that `imy.async_utils.to_daemon_thread` returns the result of the
    called function and passes through parameters correctly.
    """

    def callback(x: int, y: int) -> int:
        return x + y

    result = await imy.async_utils.to_daemon_thread(callback, 1, 2)
    assert result == 3


@pytest.mark.asyncio
async def test_to_daemon_thread_with_kwargs() -> None:
    """
    Make sure that `imy.async_utils.to_daemon_thread` returns the result of the
    called function and passes through parameters correctly.
    """

    def sync_function(x: int, y: int, z: int = 0) -> int:
        return x + y + z

    result = await imy.async_utils.to_daemon_thread(sync_function, x=1, y=2, z=3)
    assert result == 6


@pytest.mark.asyncio
async def test_to_daemon_thread_with_args_and_kwargs() -> None:
    """
    Make sure that `imy.async_utils.to_daemon_thread` returns the result of the
    called function and passes through parameters correctly.
    """

    def sync_function(x: int, y: int, z: int = 0) -> int:
        return x + y + z

    result = await imy.async_utils.to_daemon_thread(sync_function, 1, 2, z=3)
    assert result == 6


@pytest.mark.asyncio
async def test_to_daemon_thread_exception() -> None:
    """
    Tests that `imy.async_utils.to_daemon_thread` propagates exceptions from the
    called function.
    """

    def sync_function(x: int, y: int) -> int:
        raise ValueError("Test exception")

    with pytest.raises(ValueError, match="Test exception"):
        await imy.async_utils.to_daemon_thread(sync_function, 1, 2)


@pytest.mark.asyncio
async def test_to_daemon_thread_concurrency() -> None:
    """
    Tests that `imy.async_utils.to_daemon_thread` doesn't block execution of
    the current task
    """

    def slow_function() -> None:
        time.sleep(0.3)

    start_time = time.monotonic()

    # Give imy something to do
    asyncio.create_task(imy.async_utils.to_daemon_thread(slow_function))

    # Make sure the other task gets some execution time
    await asyncio.sleep(0.1)

    # This piece of code should be reached before the slow function finishes
    end_time = time.monotonic()
    assert end_time - start_time < 0.2
