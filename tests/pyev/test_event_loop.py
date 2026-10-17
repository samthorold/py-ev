from collections.abc import Iterable

from pyev.event_loop import EventLoop


class Recorder[T]:
    """Process that records every (event, t) it receives and responds with nothing."""

    def __init__(self) -> None:
        self.seen: list[tuple[T, int]] = []

    def __call__(self, event: T, t: int) -> Iterable[tuple[T, int]]:
        self.seen.append((event, t))
        return []


def test_events_delivered_in_time_order() -> None:
    recorder = Recorder[str]()
    loop = EventLoop[str](processes=[recorder])
    loop.add_event("late", 5)
    loop.add_event("early", 1)
    loop.add_event("also early", 1)

    loop.run()

    assert recorder.seen == [("early", 1), ("also early", 1), ("late", 5)]


def test_process_responses_are_scheduled() -> None:
    def ping(event: str, t: int) -> Iterable[tuple[str, int]]:
        return [("pong", t + 2)] if event == "ping" else []

    recorder = Recorder[str]()
    loop = EventLoop[str](processes=[ping, recorder])
    loop.add_event("ping", 0)

    loop.run()

    assert recorder.seen == [("ping", 0), ("pong", 2)]


def test_falsy_events_are_delivered() -> None:
    recorder = Recorder[int | None]()
    loop = EventLoop[int | None](processes=[recorder])
    for event in (1, 0, None, 2):
        loop.add_event(event, 0)

    loop.run()

    assert recorder.seen == [(1, 0), (0, 0), (None, 0), (2, 0)]


def test_add_process_does_not_mutate_callers_list() -> None:
    processes = [Recorder[str]()]
    loop = EventLoop[str](processes=processes)

    loop.add_process(Recorder[str]())

    assert len(processes) == 1
