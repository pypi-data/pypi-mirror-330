import os
import asyncio
import traceback
from typing import Any
from contextlib import suppress

from hyprctl.utils import get_socket_path
from hyprctl.parse import parse_event_from_line
from .router import Router


class Dispatcher(Router):
    """
    Dispatcher class that extends the Router class to handle events from hyprland.
    This class using a unix socker of hyprland and feeding them into the event handling system.

    Methods
    -------
    async feed_event_raw(event: str)
        Parses a raw event string and feeds it into the event handling system.
    start(loop: asyncio.AbstractEventLoop | None)
        Starts the socat listener in a separate thread and begins consuming events.
    run(loop: asyncio.AbstractEventLoop | None)
        Starts the event loop and runs the dispatcher indefinitely.
    """

    def __init__(self, socket: str | None = None, **kwargs: Any):
        super().__init__(**kwargs)

        self.socket_path = socket or get_socket_path(True)
        if not os.path.exists(self.socket_path):
            print(f"Socket {self.socket_path} does not exist!")
            return

    async def feed_event_raw(self, event: str) -> None:
        event_obj = parse_event_from_line(event)
        if event_obj:
            try:
                await self.feed_event(event_obj)
            except Exception as e:
                print(f"Error while feeding event: {e}")
                traceback.print_exception(e)

    async def listen(self):
        reader, writer = await asyncio.open_unix_connection(self.socket_path)
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                for line in data.decode().split("\n"):
                    await self.feed_event_raw(line)

        except asyncio.CancelledError:
            pass

        finally:
            writer.close()
            await writer.wait_closed()

    def start(self, loop: asyncio.AbstractEventLoop | None = None) -> asyncio.Task:
        loop = loop or asyncio.get_event_loop()
        return loop.create_task(self.listen())

    def run(self, loop: asyncio.AbstractEventLoop | None = None) -> None:
        loop = loop or asyncio.get_event_loop()
        task = self.start(loop)

        with suppress(KeyboardInterrupt):
            loop.run_forever()

        task.cancel()
