
# PhotoVault 0.2 – Scanner

PhotoVault is a self-hosted photo archive manager for Unraid and Docker.

## What 0.2 adds

- Recursive scanning of configured storage
- Image, RAW and video discovery
- SHA-256 hashing
- File size and modification time indexing
- Incremental rescans
- Exact duplicate statistics
- Scan progress/status API
- Read-only media mount for safety

No photos are moved, renamed, edited or deleted in this release.

## API

- `GET /`
- `GET /health`
- `POST /scan`
- `GET /scan/status`
- `GET /stats`
- `GET /docs`

## Safety

The Unraid media tree is mounted read-only:

```yaml
- /mnt/user:/storage:ro
```

PhotoVault can read and hash files, but cannot modify the media library.
