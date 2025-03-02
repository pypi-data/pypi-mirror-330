import asyncio

from hyprctl.utils import get_socket_path

from .commands import HyprCtlCommands
from .info import HyprCtlInfo


class HyprCtl(HyprCtlCommands, HyprCtlInfo):
    def __init__(self, socket: str | None = None):
        self.socket_path = socket or get_socket_path(False)

    async def __call__(
        self, command: str | bytes, args: str | bytes | None = None
    ) -> bytes:
        command_raw = command.encode() if isinstance(command, str) else command

        if args:
            args_raw = args.encode() if isinstance(args, str) else args
        else:
            args_raw = b""

        reader, writer = await asyncio.open_unix_connection(self.socket_path)

        if args:
            writer.write(args_raw)
            writer.write(b"/")
        writer.write(command_raw)
        await writer.drain()

        data = await reader.read()
        writer.close()
        return data
