import asyncio
import platform
import queue
import signal
import time

_terminated = False
_TIMEOUT = 10


async def delay(_time: float, function) -> any:
    await asyncio.sleep(_time)
    return await function


def timer(_loop: asyncio.AbstractEventLoop, _delay: float, function):
    if _loop == None:
        return
    try:
        asyncio.run_coroutine_threadsafe(delay(_delay, function), _loop)
    except Exception as e:
        print(e)
        pass


def async_exec(_loop: asyncio.AbstractEventLoop, function):
    if _loop == None:
        return
    try:
        asyncio.run_coroutine_threadsafe(function, _loop)
    except Exception as e:
        print(e)
        pass


def sync_call(_loop: asyncio.AbstractEventLoop, function, _timeout=_TIMEOUT) -> any:
    if _loop == None:
        return

    try:
        f = asyncio.run_coroutine_threadsafe(asyncio.wait_for(function, _timeout), _loop)
        return f.result(timeout=_timeout)
    except Exception as e:
        print(e)
        pass


async def async_call(_loop: asyncio.AbstractEventLoop, function, _timeout=_TIMEOUT) -> any:
    if _loop == None:
        return

    try:
        f = asyncio.run_coroutine_threadsafe(asyncio.wait_for(function, _timeout), _loop)
    except Exception as e:
        print(e)
        pass

    while not _terminated and not f.done():
        await asyncio.sleep(0.1)

    try:
        if not f.cancelled():
            return f.result()
    except Exception as e:
        print(e)
        return


def start_loop(loop: asyncio.BaseEventLoop):
    if platform.system() == "Darwin":
        asyncio.get_running_loop = asyncio.get_event_loop
    asyncio.set_event_loop(loop)
    loop.run_forever()
