from pathlib import Path

from app.scanner.extensions import NON_PHOTO_IMAGE_EXTENSIONS, parse_extension_list


def test_parse_extension_list_normalizes_dot_and_case():
    assert parse_extension_list("JPG,.HeIc, mp4") == {".jpg", ".heic", ".mp4"}


def test_common_non_photo_graphics_are_blocked_by_default_settings():
    from app.config import settings
    assert NON_PHOTO_IMAGE_EXTENSIONS.isdisjoint(settings.archive_extensions)
    assert ".jpg" in settings.archive_extensions
    assert ".png" in settings.archive_extensions
    assert ".dng" in settings.archive_extensions
    assert ".mov" in settings.archive_extensions


def test_known_disk1_exclusions_are_configured_in_compose():
    compose = Path("docker-compose.yml").read_text()
    assert "/storage/disk_1/Musik" in compose
    assert "/storage/disk_1/ServerFolders" in compose
    assert "/storage/disk_1/Keys" in compose
    assert "/storage/disk_1/Backup/Louise/Louise backup/Musik" in compose
