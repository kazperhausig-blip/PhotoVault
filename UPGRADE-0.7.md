# Upgrade PhotoVault 0.6 -> 0.7

PhotoVault 0.7 adds per-job exclusion paths to scanning, organizer preview and safe-copy execution.

For disk_1, use:

```json
{
  "path": "/storage/disk_1",
  "exclude": [
    "/storage/disk_1/ServerFolders",
    "/storage/disk_1/keys",
    "/storage/disk_1/Musik"
  ]
}
```

Excluded directories are pruned before recursive scanning.

The same exclusions can be supplied to preview and safe-copy so previously indexed files under excluded paths cannot accidentally enter an output plan.

## Upgrade

Mac:

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.7 scan exclusions"
git push
```

Unraid:

```bash
cd /mnt/user/photovault/source
git pull
```

Then rebuild/recreate the PhotoVault stack.

Verify `/health` reports `0.7.0`.

## Safety

`/storage` remains read-only. Source deletion is not implemented.
