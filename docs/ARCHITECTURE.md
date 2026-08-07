# PhotoVault Architecture

## Safety model

PhotoVault starts in read-only mode for the user's media library.

```text
Unraid shares
    |
    | read-only
    v
/storage
    |
    v
PhotoVault scanner
    |
    +--> metadata
    +--> checksums
    +--> duplicate analysis
    |
    v
SQLite database
```

PhotoVault's writable application data is stored separately under `/data`.

On Unraid this maps to:

```text
/mnt/user/photovault
```

## Rebuildability

The filesystem is the source of truth.

SQLite is an index and job database, not the canonical store for original media.

If the database is lost, PhotoVault must be able to rebuild it by rescanning the filesystem.

## Planned subsystems

- Scanner
- Metadata extraction
- Duplicate detection
- Organizer
- Dry-run planner
- Undo/history
- Reports
- Immich integration
- Web dashboard
- Plugin integrations
