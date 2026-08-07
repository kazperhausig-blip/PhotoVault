# Upgrade PhotoVault 0.2 -> 0.3

## Mac

Copy this package over your existing local PhotoVault repository.

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.3 metadata and duplicate inspector"
git push
```

## Unraid

```bash
cd /mnt/user/photovault/source
git pull
```

Then rebuild/recreate the PhotoVault stack in Compose Manager Plus.

## Verify

Open:

```text
http://YOUR-UNRAID-IP:5000/health
```

Version should be `0.3.0`.

## Important

Run the same test scan again. Existing files from 0.2 will be enriched with metadata because their previous rows do not yet have `metadata_status`.

Then inspect:

- `GET /stats`
- `GET /duplicates`
- `GET /media/{media_id}`
