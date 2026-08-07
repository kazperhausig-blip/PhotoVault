from pathlib import Path
from app.organizer.preview import _make_unique, _preserve_filename


def test_preserve_filename_unicode_and_spaces():
    assert _preserve_filename("Fætter Mathias 008[1].jpg") == "Fætter Mathias 008[1].jpg"


def test_preserve_filename_replaces_path_separators():
    assert _preserve_filename("a/b\\c.jpg") == "a_b_c.jpg"


def test_make_unique():
    used = set()
    first = _make_unique(Path("/Photos/2006/10/IMG_1234.JPG"), used)
    second = _make_unique(Path("/Photos/2006/10/IMG_1234.JPG"), used)
    third = _make_unique(Path("/Photos/2006/10/IMG_1234.JPG"), used)
    assert str(first) == "/Photos/2006/10/IMG_1234.JPG"
    assert str(second) == "/Photos/2006/10/IMG_1234__2.JPG"
    assert str(third) == "/Photos/2006/10/IMG_1234__3.JPG"
