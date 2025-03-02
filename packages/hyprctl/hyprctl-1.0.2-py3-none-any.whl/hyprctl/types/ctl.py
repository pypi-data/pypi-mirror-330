from pydantic import BaseModel, Field


class WorkspaceInfo(BaseModel):
    id: int
    name: str


class Monitor(BaseModel):
    id: int
    name: str
    description: str
    make: str
    model: str
    serial: str
    width: int
    height: int
    refreshRate: float
    x: int
    y: int
    activeWorkspace: WorkspaceInfo
    specialWorkspace: WorkspaceInfo
    reserved: tuple[int, int, int, int]
    scale: int
    transform: int
    focused: bool
    dpmsStatus: bool
    vrr: bool
    solitary: str
    activelyTearing: bool
    directScanoutTo: str
    disabled: bool
    currentFormat: str
    mirrorOf: str
    availableModes: list[str]


class Workspace(BaseModel):
    id: int
    name: str
    monitor: str
    monitorID: int
    windows: int
    hasfullscreen: bool
    lastwindow: str
    lastwindowtitle: str


class Client(BaseModel):
    address: str
    mapped: bool
    hidden: bool
    at: tuple[int, int]
    size: tuple[int, int]
    workspace: WorkspaceInfo
    floating: bool
    pseudo: bool
    monitor: int
    class_: str = Field(alias="class")
    title: str
    initialClass: str
    initialTitle: str
    pid: int
    xwayland: bool
    pinned: bool
    fullscreen: int
    fullscreenClient: int
    grouped: list[str]
    tags: list[str]
    swallowing: str
    focusHistoryID: int
    inhibitingIdle: bool


class DeviceMice(BaseModel):
    address: str
    name: str
    defaultSpeed: float


class DeviceKeybaord(BaseModel):
    address: str
    name: str
    rules: str
    model: str
    layout: str
    variant: str
    options: str
    active_keymap: str
    capsLock: bool
    numLock: bool
    main: bool


class DeviceSwitch(BaseModel):
    address: str
    name: str


class DevicesInfo(BaseModel):
    mice: list[DeviceMice]
    keyboards: list[DeviceKeybaord]
    tablets: list
    touch: list
    switches: list[DeviceSwitch]
