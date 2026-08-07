from pathlib import Path
from app.scanner.service import _is_within

def test_is_within():
    assert _is_within(Path("/storage/disk_1/Pictures/a.jpg"), Path("/storage/disk_1"))
    assert not _is_within(Path("/storage/disk_2/a.jpg"), Path("/storage/disk_1"))
