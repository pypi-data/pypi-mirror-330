from .types.events import EventBase


def _event_name_from_class(cls: type[EventBase]) -> str:
    return cls.__annotations__["event"].__args__[0]


def _get_class(event: str) -> type[EventBase] | None:
    for cls in EventBase.__subclasses__():
        if _event_name_from_class(cls) == event:
            return cls

    return None


def _parse_event(cls: type[EventBase], args: list[str]) -> EventBase:
    fields = cls.model_fields.copy()
    del fields["event"]
    keys_len = len(fields.keys())
    if len(args) > keys_len:
        args = args[: keys_len - 1] + [",".join(args[keys_len - 1 :])]
    elif len(args) < keys_len:
        raise ValueError(f"Expected {keys_len} arguments, got {len(args)}")

    return cls(**dict(zip(fields.keys(), args)))


def parse_event_from_line(data: str) -> EventBase | None:
    raw = data.split(
        ">>",
    )
    event_name = raw[0]
    args_splitted = raw[1].split(",") if len(raw) > 1 else []

    class_ = _get_class(event_name)
    if not class_:
        return None

    return _parse_event(class_, args_splitted)
