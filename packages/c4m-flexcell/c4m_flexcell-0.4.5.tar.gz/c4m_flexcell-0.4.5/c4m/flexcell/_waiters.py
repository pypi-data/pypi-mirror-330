# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import List, Optional
import asyncio

__all__ = ["_WaiterFactory"]


class _Waiter:
    def __init__(self, *, name: str, fab: "_WaiterFactory") -> None:
        self._name = name
        self._released = False
        # _queue is not None if waiting
        self._queue: Optional[asyncio.Queue[bool]] = None

    @property
    def name(self) -> str:
        return self._name
    @property
    def waiting(self) -> bool:
        return self._queue is not None
    @property
    def released(self) -> bool:
        return self._released

    async def wait(self) -> None:
        # self.log(f"wait() enter")
        # self.log(f"wait() _queue = {self._queue}, released = {self.released}")
        if not self.released:
            q = self._queue
            if q is None:
                # self.log(f"wait() creating queue")
                self._queue = q = asyncio.Queue()
                # self.log(f"wait() _queue = {self._queue}, released = {self.released}")
                await q.put(True)
            await q.join()
        # self.log("wait() leave")

    def done(self) -> None:
        # self.log("done() enter")
        if self._released:
            raise RuntimeError(f"Waiter '{self.name}' released two times")

        if self._queue is not None:
            async def clear_queue(q):
                assert await q.get()
                q.task_done()
                del q
            ev = asyncio.get_event_loop()
            # If we are waiting on a _Waiter the event_loop should not end before that is released
            # e.g. _queue not None
            assert ev.is_running()
            ev.create_task(clear_queue(self._queue))
        self._queue = None

        self._released = True
        # self.log("done() leave")

    def log(self, *args):
        print(f"[{self.name}]", *args)

class _FloatWaiter(_Waiter):
    def __init__(self, *, name: str, fab: "_WaiterFactory") -> None:
        super().__init__(name=name, fab=fab)
        self._value: Optional[float] = None

    @property
    def has_value(self) -> bool:
        return self._value is not None
    @property
    def value(self) -> float:
        if self._value is None:
            raise AttributeError(f"_FloatWaiter '{self.name}': value accessed before being set")
        return self._value
    @value.setter
    def value(self, v: float) -> None:
        # self.log(f"value = {v} enter")
        if self._value is not None:
            raise AttributeError(
                f"Setting value of FloatWaiter '{self.name}' twice"
            )
        self._value = v
        super().done()
        # self.log(f"value = {v} leave")

    async def wait(self) -> None:
        raise AttributeError("Don't call `_FloatWaiter.wait()`; use `_FloatWaiter.wait4value()`")
    async def wait4value(self) -> float:
        # self.log("wait4value() enter")
        await super().wait()
        # self.log("wait4value() leave")
        return self.value

    def done(self) -> None:
        raise AttributeError(f"Don't call `_FloatWaiter.done()`; use `_FloatWaiter.value = v`")


class _WaiterFactory:
    def __init__(self, *, name: str) -> None:
        self._name = name
        self.waiters: List[_Waiter] = []

    @property
    def name(self) -> str:
        return self._name

    def new_waiter(self, *, name: str) -> _Waiter:
        waiter = _Waiter(name=f"{self.name}:{name}", fab=self)
        self.waiters.append(waiter)
        return waiter

    def new_floatwaiter(self, *, name: str) -> _FloatWaiter:
        waiter = _FloatWaiter(name=f"{self.name}:{name}", fab=self)
        self.waiters.append(waiter)
        return waiter
