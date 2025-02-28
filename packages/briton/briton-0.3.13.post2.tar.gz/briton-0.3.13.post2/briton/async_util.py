import asyncio
from typing import AsyncGenerator, Awaitable, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def get_all_items(queue: asyncio.Queue):
    """Get all items from the queue without waiting."""
    items = []
    try:
        while True:
            item = queue.get_nowait()
            items.append(item)
    except asyncio.QueueEmpty:
        # Once the queue is empty, get_nowait raises QueueEmpty, and we stop
        pass
    return items


def set_event_loop_if_not_exist():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError' will be raised if there is no running loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def retry_predicate(
    pred: Callable[[], Awaitable[bool]], max_retries: int, delay_secs: float
) -> Callable[[], Awaitable[bool]]:
    async def wrapper():
        for attempt in range(max_retries):
            try:
                if await pred():
                    return True
            except Exception:
                pass
            if attempt < max_retries - 1:
                await asyncio.sleep(delay_secs)
        return False

    return wrapper


def predicate_with_timeout(
    pred: Callable[[], Awaitable[bool]], timeout_secs: float
) -> Callable[[], Awaitable[bool]]:
    async def wrapper():
        try:
            return await asyncio.wait_for(pred(), timeout=timeout_secs)
        except Exception:
            return False

    return wrapper


async def interleave_generators(*generators: AsyncGenerator[T, None]) -> AsyncGenerator[T, None]:
    """Interleaves multiple generators."""
    iterators = [aiter(gen) for gen in generators]
    completed = [False] * len(iterators)

    while not all(completed):
        for i, it in enumerate(iterators):
            if not completed[i]:
                try:
                    yield await anext(it)
                except StopAsyncIteration:
                    completed[i] = True


async def try_advance_generator(generator: AsyncGenerator[T, None]) -> AsyncGenerator[T, None]:
    """Advances a generator once and returns the original generator with all items.

    Useful if an error might be thrown on the first iteration that needs to be caught.
    """
    it = aiter(generator)
    try:
        first = await anext(it)
        yield first
        while True:
            yield await anext(it)
    except StopAsyncIteration:
        pass


async def tap_generator(
    generator: AsyncGenerator[T, None], fn: Callable[[T], None]
) -> AsyncGenerator[T, None]:
    """Applies a function to each element of a generator without modifying the sequence."""
    async for item in generator:
        fn(item)
        yield item


async def map_generator(
    generator: AsyncGenerator[T, None], fn: Callable[[T], U]
) -> AsyncGenerator[U, None]:
    """Transforms each element of a generator."""
    async for item in generator:
        yield fn(item)
