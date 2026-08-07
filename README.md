# PhotoVault 0.5 – Filename-Preserving Organizer Preview

PhotoVault 0.5 is still **dry-run only**. It does not move, copy, rename, delete or modify original media.

## Proposed structure

Unique/primary media:

`/Photos/YYYY/MM/<original filename>`

Unknown capture date:

`/Photos/UnknownDate/<original filename>`

Extra copies of exact SHA-256 duplicates:

`/Duplicates/YYYY/MM/<original filename>`

Original filenames are preserved, including spaces and Unicode characters. Only path separators and NUL are replaced.

If two different files would receive the same destination path, PhotoVault keeps both by adding `__2`, `__3`, etc.

## Full preview

Use:

`GET /organize/preview?path=/storage/disk_1/Backup/Billeder`

Leave `limit` blank to return the complete plan. A limit can still be used to shorten the response, but duplicate detection and summary counts always use the complete selected collection.

## Safety

`writes_enabled` is always `false` in 0.5, and `/mnt/user` remains mounted as `/storage:ro`.
