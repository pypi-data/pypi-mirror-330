import os
import inspect
from functools import wraps
from inspect import Parameter
from typing import Any, Callable, TypeVar

ReturnType = TypeVar("ReturnType")


def _get_needed_kwargs(callable: Callable, **kwargs) -> dict[str, Any]:
    signature = inspect.signature(callable, follow_wrapped=False)
    kwnames: list[str] = []

    params = signature.parameters.copy()

    positional_args = list(params.keys())[:1]  # event is positional argument

    for argname in positional_args:
        argparam = params[argname]

        if argparam.kind is Parameter.KEYWORD_ONLY:
            raise ValueError("event should be treated as positional argument")

        params.pop(argname)

    for argname, argparam in params.items():
        kind = argparam.kind

        if kind is Parameter.POSITIONAL_ONLY:
            raise ValueError("event should be positional argument")

        elif kind in {Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY}:
            kwnames.append(argname)

        elif kind is Parameter.VAR_KEYWORD:
            return kwargs

    needed_kwargs = {k: v for k, v in kwargs.items() if k in kwnames}

    return needed_kwargs


def safe_call(callable: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    """
    Helper function that makes new `callable` which feeds only needed `kwargs` to original.
    """

    @wraps(callable)
    def wrapper(*args, **kwargs) -> ReturnType:
        needed_kwargs = _get_needed_kwargs(callable=callable, **kwargs)
        return callable(*args, **needed_kwargs)

    return wrapper


def get_socket_path(is_listener_socket: bool) -> str:
    xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    hyprland_instance_signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if not xdg_runtime_dir or not hyprland_instance_signature:
        raise ValueError("XDG_RUNTIME_DIR or HYPRLAND_INSTANCE_SIGNATURE is not set")

    file = ".socket2.sock" if is_listener_socket else ".socket.sock"
    return os.path.join(xdg_runtime_dir, "hypr", hyprland_instance_signature, file)
