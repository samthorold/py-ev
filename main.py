"""PyEv Python Discrete Event Loop."""

import logging
import os

from event_loop import EventLoop
from processes import MyEv, Player

logger = logging.getLogger(__name__)


logging.basicConfig(level=os.environ.get("PYEV_LOG_LEVEL") or logging.DEBUG)

loop = EventLoop(
    processes=[Player(name="p1")],
    events=[
        MyEv(t=1, a="a"),
    ],
)
loop.run()
