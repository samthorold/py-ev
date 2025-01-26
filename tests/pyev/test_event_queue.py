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


def test_queue_push_ordering() -> None:
    e1 = Event(t=0, priority=0, data=None)
    e2 = Event(t=0, priority=1, data=None)
    e3 = Event(t=1, priority=0, data=None)

    q = EventQueue[None]()

    assert not q

    q.push(e3)
    assert q.peek() == e3

    q.push(e2)
    assert q.peek() == e2

    q.push(e1)
    assert q.peek() == e1
