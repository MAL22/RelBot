import asyncio
from collections import Coroutine
from jujube.utils.singleton import Singleton


class Timer:
    def __init__(self, timeout, callback, loop: bool = False, *args):
        self._timeout = timeout
        self._callback = callback
        self._loop = loop
        self._task = asyncio.create_task(self._job(*args))

    async def _job(self, *args):
        await asyncio.sleep(self._timeout)
        await self._callback(self, *args)
        if self._loop:
            await self._job(*args)

    def cancel(self):
        self._task.cancel()


class Timers(Singleton):
    def init(self, *args, **kwargs):
        self._timers = {}

    def get_timer(self, name) -> Timer:
        return self._timers[name]

    def add(self, timeout: float, callback: Coroutine, loop: bool = False) -> Timer:
        t = Timer(timeout, callback)
        return t
