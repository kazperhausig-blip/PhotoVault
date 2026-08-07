
import hashlib
from pathlib import Path
from app.config import settings

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(settings.hash_chunk_size):
            digest.update(chunk)
    return digest.hexdigest()
