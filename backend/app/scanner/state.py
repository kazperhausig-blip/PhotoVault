
from dataclasses import asdict, dataclass
from threading import Lock

@dataclass
class ScanState:
    running: bool = False
    job_id: int | None = None
    root_path: str | None = None
    current_file: str | None = None
    discovered: int = 0
    indexed: int = 0
    skipped_unchanged: int = 0
    errors: int = 0

_lock = Lock()
_state = ScanState()

def begin(job_id: int, root_path: str) -> bool:
    with _lock:
        if _state.running:
            return False
        _state.running = True
        _state.job_id = job_id
        _state.root_path = root_path
        _state.current_file = None
        _state.discovered = _state.indexed = _state.skipped_unchanged = _state.errors = 0
        return True

def update(**kwargs) -> None:
    with _lock:
        for key, value in kwargs.items(): setattr(_state, key, value)

def increment(field: str, amount: int = 1) -> None:
    with _lock:
        setattr(_state, field, getattr(_state, field) + amount)

def finish() -> None:
    with _lock:
        _state.running = False
        _state.current_file = None

def snapshot() -> dict:
    with _lock:
        return asdict(_state)
