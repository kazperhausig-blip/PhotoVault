# Architecture

```
Browser
    │
React
    │
FastAPI
    │
Scanner
Metadata
Duplicates
Organizer
Reports
    │
SQLite
    │
Filesystem
```

## Principles

- Originals never modified.
- Database rebuildable.
- Everything logged.
- Undo supported.
- Plugin architecture.
