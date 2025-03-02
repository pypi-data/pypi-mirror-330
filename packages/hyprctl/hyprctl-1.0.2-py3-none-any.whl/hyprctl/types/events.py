from abc import ABC
from typing import Literal

from pydantic import BaseModel, field_serializer


class EventBase(BaseModel, ABC):
    event: str


class WorkspaceEvent(EventBase):
    """
    Emitted on workspace change. Is emitted ONLY when a
    user requests a workspace change, and is not emitted
    on mouse movements (see `focusedmon`)
    """

    event: Literal["workspacev2"] = "workspacev2"
    id: int
    name: str


class FocusedMonitorEvent(EventBase):
    """
    Emitted on the active monitor being changed.
    """

    event: Literal["focusedmonv2"] = "focusedmonv2"
    monitor_name: int
    workspace_id: int


class ActiveWindowEvent(EventBase):
    """
    Emitted on the active window being changed.
    """

    event: Literal["activewindowv2"] = "activewindowv2"
    adress: str


class FullScreenEvent(EventBase):
    """
    Emitted when a fullscreen status of a window changes.
    """

    event: Literal["fullscreen"] = "fullscreen"
    is_fullscreen: bool

    @field_serializer("is_fullscreen")
    def serialize_is_fullscreen(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class MonitorRemovedEvent(EventBase):
    """
    Emitted when a monitor is removed (disconnected)
    """

    event: Literal["monitorremoved"] = "monitorremoved"
    monitor_name: int


class MonitorAddedEvent(EventBase):
    """
    Emitted when a monitor is added (connected)
    """

    event: Literal["monitoraddedv2"] = "monitoraddedv2"
    id: int
    name: str
    description: str


class CreateWorkspaceEvent(EventBase):
    """
    Emitted when a workspace is created
    """

    event: Literal["createworkspacev2"] = "createworkspacev2"
    id: int
    name: str


class DestoryWorkspaceEvent(EventBase):
    """
    Emitted when a workspace is destroyed
    """

    event: Literal["destroyworkspacev2"] = "destroyworkspacev2"
    id: int
    name: str


class MoveWorkspaceEvent(EventBase):
    """
    Emitted when a workspace is moved to a different monitor
    """

    event: Literal["moveworkspacev2"] = "moveworkspacev2"
    id: int
    name: str
    new_monitor_name: str


class RenameWorkspaceEvent(EventBase):
    """
    Emitted when a workspace is renamed
    """

    event: Literal["renameworkspace"] = "renameworkspace"
    id: int
    new_name: str


class ActiveSpecialEvent(EventBase):
    """
    Emitted when the special workspace opened in a monitor changes
    (closing results in an empty `name`)
    """

    event: Literal["activespecial"] = "activespecial"
    name: str
    monitor_name: str


class ActiveLayoutEvent(EventBase):
    """
    Emitted on a layout change of the active keyboard
    """

    event: Literal["activelayout"] = "activelayout"
    keyboard_name: str
    layout_name: str


class OpenWindowEvent(EventBase):
    """
    Emitted when a window is opened
    """

    event: Literal["openwindow"] = "openwindow"
    adress: str
    workspace_name: str
    wclass: str
    title: str


class CloseWindowEvent(EventBase):
    """
    Emitted when a window is closed
    """

    event: Literal["closewindow"] = "closewindow"
    adress: str


class MoveWindowEvent(EventBase):
    """
    Emitted when a window is moved to a workspace
    """

    event: Literal["movewindowv2"] = "movewindowv2"
    adress: str
    id: int
    workspace_name: str


class OpenLayerEvent(EventBase):
    """
    Emitted when a layerSurface is mapped
    """

    event: Literal["openlayer"] = "openlayer"
    name: str


class CloseLayerEvent(EventBase):
    """
    Emitted when a layerSurface is unmapped
    """

    event: Literal["closelayer"] = "closelayer"
    name: str


class SubMapEvent(EventBase):
    """
    emitted when a keybind submap changes. Empty means default.
    """

    event: Literal["submap"] = "submap"
    name: str


class ChangeFloatingModeEvent(EventBase):
    """
    emitted when a window changes its floating mode.
    """

    event: Literal["changefloatingmode"] = "changefloatingmode"
    adress: str
    is_floating: bool

    @field_serializer("is_floating")
    def serialize_is_floating(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class UrgentEvent(EventBase):
    """
    Emitted when a window requests an `urgent` state
    """

    event: Literal["urgent"] = "urgent"
    adress: str


class ScreenCastEvent(EventBase):
    """
    Emitted when a screencopy state of a client changes.
    Keep in mind there might be multiple separate clients.
    State is 0/1, owner is 0 - monitor share, 1 - window share
    """

    event: Literal["screencast"] = "screencast"
    state: bool
    owner: int

    @field_serializer("state")
    def serialize_state(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class WindowTitleEvent(EventBase):
    """
    Emitted when a window title changes
    """

    event: Literal["windowtitlev2"] = "windowtitlev2"
    adress: str
    title: str


class ToggleGroupEvent(EventBase):
    """
    Emitted when togglegroup command is used. Returns state,handle where
    the state is a toggle status and the handle is one or more window
    addresses separated by a comma e.g. 0,64cea2525760,64cea2522380
    where 0 means that a group has been destroyed and the rest informs
    which windows were part of it
    """

    event: Literal["togglegroup"] = "togglegroup"
    is_group: bool
    address: str

    @field_serializer("is_group")
    def serialize_is_group(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class MoveIntoGroupEvent(EventBase):
    """
    Emitted when the window is merged into a group.
    Returns the address of a merged window
    """

    event: Literal["moveintogroup"] = "moveintogroup"
    window_address: str


class MoveOutOfGroupEvent(EventBase):
    """
    Emitted when the window is removed from a group.
    Returns the address of a removed window
    """

    event: Literal["moveoutofgroup"] = "moveoutofgroup"
    window_address: str


class IgnoreGroupLockEvent(EventBase):
    """
    Emitted when `ignoregrouplock` is toggled.
    """

    event: Literal["ignoregrouplock"] = "ignoregrouplock"
    is_enabled: bool

    @field_serializer("is_enabled")
    def serialize_is_enabled(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class LockgroupsEvent(EventBase):
    """
    Emitted when `lockgroups` is toggled.
    """

    event: Literal["lockgroups"] = "lockgroups"
    is_enabled: bool

    @field_serializer("is_enabled")
    def serialize_is_enabled(cls, v: bool | int | str) -> bool:
        return bool(int(v))


class ConfigureLoadedEvent(EventBase):
    """
    Emitted when the config is done reloading
    """

    event: Literal["configureloaded"] = "configureloaded"


class PinEvent(EventBase):
    """
    Emitted when a window is pinned or unpinned
    """

    event: Literal["pin"] = "pin"
    adress: str
    is_pinned: bool

    @field_serializer("is_pinned")
    def serialize_is_pinned(cls, v: bool | int | str) -> bool:
        return bool(int(v))
