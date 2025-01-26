import pytest

from app.event_loop import Event, EventLoop


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
