from app.event_loop import Event, EventLoop


def test_event_loop_peek_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop([], [event])
    event_loop.tick()  # LoopStarted event
    assert event_loop.peek_event() == event
    assert event in event_loop.events


def test_event_loop_add_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop([], [])
    event_loop.add_event(event)
    assert event in event_loop.events


def test_event_loop_next_event() -> None:
    event = Event(t=1)
    event_loop = EventLoop([], [event])
    event_loop.tick()  # LoopStarted event
    assert event_loop.next_event() == event
    assert event not in event_loop.events
    assert event_loop.current_timestep == 1
