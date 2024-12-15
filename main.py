"""PyEv Python Discrete Event Loop."""

import logging
import os

from event_loop import EventLoop
from processes import PlayerProcess


logger = logging.getLogger(__name__)


logging.basicConfig(level=os.environ.get("PYEV_LOG_LEVEL") or logging.DEBUG)

loop = EventLoop(processes=[PlayerProcess(name="p1")])
loop.run()
