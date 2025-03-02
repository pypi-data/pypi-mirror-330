from hyprctl.types.color import RGBA
from hyprctl.types.enums import Backend, Icon

from .base import HyprCtlBase, HyprError


class HyprCtlCommands(HyprCtlBase):
    async def dispatch(self, command: str):
        r = await self(f"dispatch {command}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def keyword(self, command: str):
        r = await self(f"keyword {command}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def kill(self):
        r = await self("kill")
        if r != b"ok":
            raise HyprError(r.decode())

    async def set_cursor(self, name: str, size: int):
        r = await self(f"setcursor {name} {size}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def output_create(
        self, backend: Backend = Backend.AUTO, name: str | None = None
    ):
        r = await self(f"output create {backend} {name}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def output_remove(self, name: str):
        r = await self(f"output remove {name}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def switch_xkb_layout(self, device: str, layout: str):
        r = await self(f"switchxkblayout {device} {layout}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def set_error(self, error: str):
        r = await self(f"seterror {error}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def disable_error(self):
        r = await self("seterror disable")
        if r != b"ok":
            raise HyprError(r.decode())

    async def notify(self, icon: Icon, time: int, color: RGBA, message: str):
        r = await self(f"notify {icon} {time} {color} {message}")
        if r != b"ok":
            raise HyprError(r.decode())

    async def dismissnotify(self, amount: int = -1):
        r = await self(f"dismissnotify {amount}")
        if r != b"ok":
            raise HyprError(r.decode())
