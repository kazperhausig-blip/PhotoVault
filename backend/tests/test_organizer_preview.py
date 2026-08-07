from pathlib import Path
from app.organizer.preview import _make_unique, _safe_filename


def test_safe_filename():
    assert _safe_filename("kbh 001.jpg") == "kbh_001.jpg"


def test_make_unique():
    used = set()
    first = _make_unique(Path("/Photos/2006/10/a.jpg"), used)
    second = _make_unique(Path("/Photos/2006/10/a.jpg"), used)
    assert str(first) == "/Photos/2006/10/a.jpg"
    assert str(second) == "/Photos/2006/10/a__2.jpg"
