# Upgrade PhotoVault 0.3 -> 0.4

## On the Mac

Copy this package over the existing `~/Documents/PhotoVault` repository.

Then:

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.4 organizer preview"
git push
```

## On Unraid

```bash
cd /mnt/user/photovault/source
git pull
```

Rebuild/recreate the PhotoVault stack in Compose Manager Plus.

## Verify

Open:

`http://192.168.1.34:5000/health`

It should report version `0.4.0`.

Then open:

`http://192.168.1.34:5000/docs`

Use:

`GET /organize/preview`

For the current test collection, use the path:

`/storage/disk_1/Backup/Billeder`

Start with a limit of `50` or `100`. This is a dry-run only.
