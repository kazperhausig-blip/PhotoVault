# PhotoVault 0.3 – Metadata & Duplicate Inspector

Version 0.3 adds metadata extraction and duplicate inspection while keeping the media library read-only.

## New in 0.3

- EXIF capture date extraction
- Camera make/model
- Lens model
- GPS latitude/longitude when available
- Width/height for supported image formats
- Metadata status tracking
- Unknown-date count
- Duplicate group detail endpoint
- Media detail endpoint
- Metadata refresh during scans

## Safety

Original media is still mounted read-only:

```yaml
- /mnt/user:/storage:ro
```

PhotoVault cannot move, rename, edit or delete your originals in this release.

## Useful endpoints

- `POST /scan`
- `GET /scan/status`
- `GET /stats`
- `GET /duplicates`
- `GET /media/{media_id}`
- `GET /docs`
