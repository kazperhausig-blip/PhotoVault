# PhotoVault 0.7 – Exclusion-Aware Scanner

Version 0.7 adds explicit exclusions to scanning and organizer planning.

Example scan:

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

The original library remains mounted read-only. Safe-copy still writes only to the dedicated `/output` mount and verifies copied files with SHA-256.
