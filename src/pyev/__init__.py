"""PyEv: a discrete event loop."""

from importlib.metadata import version

from pyev.event_loop import EventLoop, ProcessProtocol
from pyev.event_queue import EventQueue, QueueItem

__version__ = version("py-ev")

__all__ = ["EventLoop", "EventQueue", "ProcessProtocol", "QueueItem", "__version__"]
