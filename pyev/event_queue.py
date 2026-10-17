import heapq
from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class QueueItem[T]:
    """Event data queued at timestep `t`, ordered and compared by `(t, priority)`."""

    t: int
    priority: int
    data: T = field(compare=False)


class EventQueue[T]:
    def __init__(self, events: list[QueueItem[T]] | None = None) -> None:
        self.events = [] if events is None else events
        self.counter: dict[int, int] = {}
        for item in self.events:
            self.counter[item.t] = max(self.counter.get(item.t, 0), item.priority + 1)
        heapq.heapify(self.events)

    def __len__(self) -> int:
        return len(self.events)

    def _push(self, item: QueueItem[T]) -> None:
        heapq.heappush(self.events, item)

    def push(self, data: T, t: int) -> None:
        priority = self.counter.get(t, 0)
        item = QueueItem(t=t, priority=priority, data=data)
        self._push(item)
        self.counter[t] = priority + 1

    def pop(self) -> QueueItem[T]:
        return heapq.heappop(self.events)

    def peek(self) -> QueueItem[T] | None:
        if self.events:
            return self.events[0]
        return None
