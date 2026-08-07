# Upgrade PhotoVault 0.5 -> 0.6

PhotoVault 0.6 introduces the first write-capable component, but it is deliberately **copy-only**.

## Safety design

- `/storage` remains read-only.
- Originals are never deleted or renamed.
- Output is a separate writable mount: `/output`.
- Every copied file is SHA-256 verified before it is finalized.
- Copying uses a temporary `.photovault-part` file followed by an atomic rename.
- An existing destination is never overwritten.
- If an existing destination already has the expected hash, it is treated as verified/resumable.
- Each item and job is recorded in SQLite.
- A failed item does not stop the remaining items.
- Source deletion is not implemented in 0.6.

## IMPORTANT: create the destination share first

In Unraid create a share named:

`photovault-output`

The Compose file maps:

`/mnt/user/photovault-output:/output`

Do not point `/output` at the original photo folder.

## Upgrade

On Mac, copy this package over your existing repository, then:

```bash
cd ~/Documents/PhotoVault
git add -A
git commit -m "Add PhotoVault 0.6 safe copy engine"
git push
```

On Unraid:

```bash
cd /mnt/user/photovault/source
git pull
```

Rebuild/recreate the stack.

Verify `/health` reports `0.6.0`.

## Recommended first execution test

Do NOT start with all 582 files.

First use `GET /organize/preview` with the existing test path and a small limit to inspect destinations.

Then use `POST /organize/execute` only after you have created the `photovault-output` share.

The request body requires:

```json
{
  "path": "/storage/disk_1/Backup/Billeder",
  "confirmation": "COPY_AND_VERIFY"
}
```

Note: the execute endpoint currently creates a job for the complete selected path. For the first real write test, scan/index a dedicated tiny test folder (for example 3–5 copied sample images) and execute against that tiny path. This prevents using the full collection as the first write test.

Follow progress with:

- `GET /organize/execute/status`
- `GET /organize/jobs/{job_id}`
