from collections import defaultdict
from typing import Any, Callable, ParamSpec, Protocol, TypeVar

from hyprctl.types import EventBase
from hyprctl.utils import safe_call


T = TypeVar("T", bound=EventBase, contravariant=True)
P = ParamSpec("P")


class ListenerType(Protocol[T, P]):
    async def __call__(self, event: T, *args: P.args, **kwargs: P.kwargs) -> None: ...


class Router:
    def __init__(self, **kwargs: Any):
        self.listeners: dict[type[EventBase], list[ListenerType]] = defaultdict(list)
        self.subrouters: list[Router] = []
        self.workflow_data: dict[str, Any] = kwargs

    def add_listener(self, event: type[T], listener: ListenerType[T, P]) -> None:
        self.listeners[event].append(listener)

    def listener(self, event: type[T]) -> Callable[[ListenerType[T, P]], None]:
        """
        A decorator to register a listener for a specific event type.
        Args:
            event (type[EventBase]): The type of event to listen for.
        """

        def decorator(listener: ListenerType[T, P]) -> None:
            self.add_listener(event, safe_call(listener))

        return decorator

    def add_subrouter(self, subrouter: "Router") -> None:
        """
        Adds a subrouter to the current router.
        This method links the provided subrouter to the current router by sharing
        the workflow data and appending the subrouter to the list of subrouters.
        Args:
            subrouter (Router): The subrouter to be added.
        """

        # create a shared workflow data between routers
        subrouter.workflow_data = self.workflow_data
        self.subrouters.append(subrouter)

    async def feed_event(self, event: EventBase) -> None:
        """
        Asynchronously feeds an event to the appropriate listeners and subrouters.
        Args:
            event (EventBase): The event to be processed.
        """


        for listener in self.listeners[type(event)]:
            await listener(event, **self.workflow_data)

        for subrouter in self.subrouters:
            await subrouter.feed_event(event)
