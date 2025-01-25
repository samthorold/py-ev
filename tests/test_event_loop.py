import pytest

from app.event_loop import Event, EventLoop


def test_event_loop_peek_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop(
        processes=[],
        events=[event],
        add_loop_started_event=False,
    )
    assert event_loop.peek_event() == event
    assert event in event_loop.events


def test_event_loop_add_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop(processes=[])
    event_loop.add_event(event)
    assert event in event_loop.events


def test_event_loop_next_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop(
        processes=[],
        events=[event],
        current_timestep=1,
        add_loop_started_event=False,
    )
    assert event_loop.next_event() == event
    assert event not in event_loop.events
    assert event_loop.current_timestep == 1


def test_event_loop_past_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop(
        processes=[],
        current_timestep=2,
        add_loop_started_event=False,
    )
    with pytest.raises(RuntimeError):
        event_loop.add_event(event)
