import sys
from _typeshed import FileDescriptor
from collections.abc import Sequence

from gevent._ffi.loop import AbstractLoop
from gevent.libev import watcher

def get_version() -> str: ...
def get_header_version() -> str: ...
def supported_backends() -> list[str | int]: ...
def recommended_backends() -> list[str | int]: ...
def embeddable_backends() -> list[str | int]: ...
def time() -> float: ...

class loop(AbstractLoop):
    approx_timer_resolution: float
    error_handler: None
    @property
    def MAXPRI(self) -> int: ...
    @property
    def MINPRI(self) -> int: ...
    def __init__(self, flags: Sequence[str] | str | int | None = None, default: bool | None = None) -> None: ...
    def io(self, fd: FileDescriptor, events: int, ref: bool = True, priority: int | None = None) -> watcher.io: ...
    def closing_fd(self, fd: FileDescriptor) -> bool: ...
    def timer(self, after: float, repeat: float = 0.0, ref: bool = True, priority: int | None = None) -> watcher.timer: ...
    def signal(self, signum: int, ref: bool = True, priority: int | None = None) -> watcher.signal: ...
    def idle(self, ref: bool = True, priority: int | None = None) -> watcher.idle: ...
    def prepare(self, ref: bool = True, priority: int | None = None) -> watcher.prepare: ...
    def check(self, ref: bool = True, priority: int | None = None) -> watcher.check: ...
    def async_(self, ref: bool = True, priority: int | None = None) -> watcher.async_: ...
    if sys.platform != "win32":
        def fork(self, ref: bool = True, priority: int | None = None) -> watcher.fork: ...
        def child(self, pid: int, trace: int = 0, ref: bool = True) -> watcher.child: ...
        def reset_sigchld(self) -> None: ...

    def stat(self, path: str, interval: float = 0.0, ref: bool = True, priority: bool | None = None) -> watcher.stat: ...

__all__ = [
    "get_version",
    "get_header_version",
    "supported_backends",
    "recommended_backends",
    "embeddable_backends",
    "time",
    "loop",
]
