from pathlib import Path
from app.metadata.extractor import extract_metadata


def test_non_image_metadata_placeholder(tmp_path: Path):
    file = tmp_path / "x.mp4"
    file.write_bytes(b"test")
    result = extract_metadata(file, "video")
    assert result["metadata_status"] == "not_supported_yet"
