class HyprError(Exception):
    pass


class HyprCtlBase:
    def __call__(self, command: str | bytes, args: str | bytes | None = None) -> bytes:
        raise NotImplementedError
