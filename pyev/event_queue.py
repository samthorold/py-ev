import heapq
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Event[T]:
    """Queued event, ordered (and compared) by `(t, priority)` only."""

    t: int
    priority: int
    data: T = field(compare=False)


class EventQueue[T]:
    def __init__(self, events: list[Event[T]] | None = None) -> None:
        self.events = [] if events is None else events
        self.counter: dict[int, int] = {}
        for event in self.events:
            self.counter[event.t] = max(
                self.counter.get(event.t, 0), event.priority + 1
            )
        heapq.heapify(self.events)

    def __len__(self) -> int:
        return len(self.events)

    def _push(self, event: Event[T]) -> None:
        heapq.heappush(self.events, event)

    def push(self, data: T, t: int) -> None:
        priority = self.counter.get(t, 0)
        event = Event(t=t, priority=priority, data=data)
        self._push(event)
        self.counter[t] = priority + 1

    def pop(self) -> Event[T]:
        return heapq.heappop(self.events)

    def peek(self) -> Event[T] | None:
        if self.events:
            return self.events[0]
        return None
