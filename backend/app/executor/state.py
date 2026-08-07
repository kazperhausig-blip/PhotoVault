from dataclasses import asdict, dataclass
from threading import Lock


@dataclass
class ExecutionState:
    running: bool = False
    job_id: int | None = None
    current_source: str | None = None
    total: int = 0
    copied: int = 0
    verified: int = 0
    skipped_verified: int = 0
    failed: int = 0


_lock = Lock()
_state = ExecutionState()


def begin(job_id: int, total: int) -> bool:
    with _lock:
        if _state.running:
            return False
        _state.running = True
        _state.job_id = job_id
        _state.current_source = None
        _state.total = total
        _state.copied = 0
        _state.verified = 0
        _state.skipped_verified = 0
        _state.failed = 0
        return True


def update(**kwargs):
    with _lock:
        for k, v in kwargs.items():
            setattr(_state, k, v)


def increment(field: str):
    with _lock:
        setattr(_state, field, getattr(_state, field) + 1)


def finish():
    with _lock:
        _state.running = False
        _state.current_source = None


def snapshot():
    with _lock:
        return asdict(_state)
