import pytest

from app.event_loop import _Event  # pyright: ignore[reportPrivateUsage]
from app.event_loop import Event, EventLoop


def empty_event_loop() -> EventLoop:
    l = EventLoop(processes=[])
    l.events = []
    return l


def test_event_loop_order() -> None:
    l = empty_event_loop()

    e1 = _Event(t=0, priority=0, event=Event())
    e2 = _Event(t=0, priority=2, event=Event())

    expected_ordering = [e1, e2]

    l.push(e2)
    l.push(e1)

    assert l.events == expected_ordering


def test_event_loop_peek_event() -> None:
    event = Event()
    event_loop = EventLoop(processes=[])
    event_loop.add_event(event, 1)
    event_loop.current_timestep = 1

    assert event_loop.peek_event()


def test_event_loop_next_event() -> None:
    event = Event()
    event_loop = EventLoop(processes=[])
    event_loop.add_event(event, 1)

    assert event_loop.next_event()  # LoopStarted popped
    assert not event_loop.next_event()  # No more t=0

    event_loop.current_timestep = 1

    assert event_loop.next_event()  # Event popped
    assert not event_loop.next_event()  # No more t=1


def test_event_loop_past_event() -> None:
    event_loop = EventLoop(processes=[], timestep=2)
    with pytest.raises(RuntimeError):
        event_loop.add_event(Event(), 1)
