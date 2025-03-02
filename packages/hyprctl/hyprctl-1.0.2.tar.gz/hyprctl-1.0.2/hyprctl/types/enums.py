from enum import IntEnum, StrEnum


class Backend(StrEnum):
    WAYLAND = "wayland"
    HEADLESS = "headless"
    AUTO = "auto"


class Icon(IntEnum):
    INFO = 1
    HINT = 2
    ERROR = 3
    CONFUSED = 4
    OK = 5
