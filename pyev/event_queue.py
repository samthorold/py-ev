import heapq
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Event(Generic[T]):
    def __init__(self, t: int, priority: int, data: T) -> None:
        self.t = t
        self.priority = priority
        self.data = data

    def __repr__(self) -> str:
        return f"<Event(t={self.t}, priority={self.priority}, data={repr(self.data)})>"

    def __gt__(self, o: Any) -> bool:
        if isinstance(o, Event):
            return (self.t, self.priority) > (o.t, o.priority)
        raise TypeError(f"Cannot compare Event to {o.__class__}")


class EventQueue(Generic[T]):
    def __init__(self, events: list[Event[T]] | None = None) -> None:
        self.events = [] if events is None else events
        heapq.heapify(self.events)

    def __len__(self) -> int:
        return len(self.events)

    def __contains__(self, o: Event[T]) -> bool:
        return o in self.events

    def push(self, event: Event[T]) -> None:
        heapq.heappush(self.events, event)

    def pop(self) -> Event[T]:
        return heapq.heappop(self.events)

    def peek(self) -> Event[T] | None:
        if self.events:
            return self.events[0]
        return None
