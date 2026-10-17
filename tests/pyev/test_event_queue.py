from pyev.event_queue import Event, EventQueue


def test_event_ordering() -> None:
    e1 = Event(t=0, priority=0, data=None)
    e2 = Event(t=0, priority=1, data=None)
    e3 = Event(t=1, priority=0, data=None)

    assert e1 < e2 < e3


def test_queue_init_ordering() -> None:
    e1 = Event(t=0, priority=0, data=None)
    e2 = Event(t=0, priority=1, data=None)
    e3 = Event(t=1, priority=0, data=None)

    q = EventQueue([e3, e1, e2])

    assert q.pop() == e1
    assert q.pop() == e2
    assert q.pop() == e3


def test_queue_priority() -> None:
    e1 = Event(t=0, priority=0, data=None)
    e2 = Event(t=0, priority=1, data=None)
    e3 = Event(t=1, priority=0, data=None)

    q = EventQueue[None]()

    assert not q

    q.push(None, 1)
    q.push(None, 0)
    q.push(None, 0)

    assert q.pop() == e1
    assert q.pop() == e2
    assert q.pop() == e3


def test_push_after_init_queues_behind_initial_events() -> None:
    q = EventQueue(
        [Event(t=0, priority=0, data="first"), Event(t=0, priority=1, data="second")]
    )

    q.push("pushed", 0)

    assert [q.pop().data for _ in range(3)] == ["first", "second", "pushed"]


def test_event_is_not_equal_to_other_types() -> None:
    event = Event(t=0, priority=0, data=None)

    assert event != "not an event"
    assert event not in [None, 0]


def test_events_are_hashable() -> None:
    a = Event(t=0, priority=0, data="a")
    b = Event(t=0, priority=1, data="b")

    assert len({a, b, Event(t=0, priority=0, data="a")}) == 2
