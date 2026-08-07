# Upgrade PhotoVault 0.4 -> 0.5

PhotoVault 0.5 keeps the organizer in dry-run/read-only mode.

Changes:
- Original filenames are preserved, including spaces, Danish letters and other Unicode.
- Media is proposed under `/Photos/YYYY/MM/<original filename>`.
- Exact extra SHA-256 copies are proposed under `/Duplicates/YYYY/MM/<original filename>`.
- Missing dates go to `/Photos/UnknownDate/`.
- Different files that would get the same destination name receive `__2`, `__3`, etc.
- Duplicate detection always considers the complete selected collection, even when a response `limit` is used.
- Leave `limit` blank to preview the complete collection.

## Mac

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.5 filename-preserving organizer preview"
git push
```

## Unraid

```bash
cd /mnt/user/photovault/source
git pull
```

Rebuild/recreate PhotoVault in Compose Manager Plus.

Verify `/health` reports `0.5.0`.

Then use `GET /organize/preview` with:

`path = /storage/disk_1/Backup/Billeder`

Leave `limit` blank for the complete preview.

Safety: `writes_enabled` remains `false`; the media mount remains read-only.
