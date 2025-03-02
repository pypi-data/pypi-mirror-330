import json

from hyprctl.types import Monitor, Workspace, Client, DevicesInfo
from .base import HyprCtlBase


class HyprCtlInfo(HyprCtlBase):
    async def version(self) -> str:
        return (await self("version")).decode()

    async def monitors(self) -> list[Monitor]:
        monitors: list[Monitor] = []
        for monitor in json.loads(await self("monitors", "j")):
            monitors.append(Monitor.model_validate(monitor))
        return monitors

    async def workspaces(self) -> list[Workspace]:
        workspaces: list[Workspace] = []
        for workspace in json.loads(await self("workspaces", "j")):
            workspaces.append(Workspace.model_validate(workspace))
        return workspaces

    async def active_workspace(self) -> Workspace:
        return Workspace.model_validate_json(await self("activeworkspace", "j"))

    async def workspace_rules(self) -> list:
        return json.loads(await self("workspacerules", "j"))

    async def clients(self) -> list[Client]:
        clients: list[Client] = []
        for client in json.loads(await self("clients", "j")):
            clients.append(Client.model_validate(client))
        return clients

    async def devices(self) -> DevicesInfo:
        return DevicesInfo.model_validate_json(await self("devices", "j"))
