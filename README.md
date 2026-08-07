# PhotoVault 0.4 – Organizer Preview

PhotoVault 0.4 adds a **dry-run organizer**. It does not move, rename, delete or modify original media.

## What the preview proposes

Unique/primary media with a capture date:

`/Photos/YYYY/MM/YYYY-MM-DD_HH-MM-SS_original-name.ext`

Media without a capture date:

`/Photos/UnknownDate/original-name.ext`

Extra copies of exact SHA-256 duplicates:

`/Duplicates/YYYY/MM/original-name.ext`

Name collisions are resolved with `__2`, `__3`, etc. No proposed destination is allowed to overwrite another item.

## New endpoint

`GET /organize/preview`

Optional query parameters:

- `path=/storage/disk_1/Backup/Billeder`
- `limit=100`

Example:

`/organize/preview?path=/storage/disk_1/Backup/Billeder&limit=100`

## Safety

The original Unraid tree remains mounted:

`/mnt/user:/storage:ro`

`writes_enabled` in the preview response is always `false` in 0.4.
