from pyev import EventQueue, QueueItem


def test_item_ordering() -> None:
    e1 = QueueItem(t=0, priority=0, data=None)
    e2 = QueueItem(t=0, priority=1, data=None)
    e3 = QueueItem(t=1, priority=0, data=None)

    assert e1 < e2 < e3


def test_queue_init_ordering() -> None:
    e1 = QueueItem(t=0, priority=0, data=None)
    e2 = QueueItem(t=0, priority=1, data=None)
    e3 = QueueItem(t=1, priority=0, data=None)

    q = EventQueue([e3, e1, e2])

    assert q.pop() == e1
    assert q.pop() == e2
    assert q.pop() == e3


def test_queue_priority() -> None:
    e1 = QueueItem(t=0, priority=0, data=None)
    e2 = QueueItem(t=0, priority=1, data=None)
    e3 = QueueItem(t=1, priority=0, data=None)

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
        [
            QueueItem(t=0, priority=0, data="first"),
            QueueItem(t=0, priority=1, data="second"),
        ]
    )

    q.push("pushed", 0)

    assert [q.pop().data for _ in range(3)] == ["first", "second", "pushed"]


def test_item_is_not_equal_to_other_types() -> None:
    item = QueueItem(t=0, priority=0, data=None)

    assert item != "not an item"
    assert item not in [None, 0]


def test_items_are_hashable() -> None:
    a = QueueItem(t=0, priority=0, data="a")
    b = QueueItem(t=0, priority=1, data="b")

    assert len({a, b, QueueItem(t=0, priority=0, data="a")}) == 2
