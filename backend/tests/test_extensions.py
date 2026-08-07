from app.scanner.extensions import media_type_for_extension


def test_media_type_classification():
    assert media_type_for_extension(".jpg") == "image"
    assert media_type_for_extension(".CR3") == "raw"
    assert media_type_for_extension(".mov") == "video"
