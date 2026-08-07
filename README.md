# PhotoVault

PhotoVault is a self-hosted photo archive manager designed for people who want full control over their photo library.

## Core principles

- Originals are never modified automatically.
- Nothing is deleted automatically.
- The database can always be rebuilt from the filesystem.
- Every destructive operation must be explicit and reversible.
- PhotoVault should work without cloud services.

## First milestone

The first milestone is intentionally read-only. PhotoVault will:

- start as a Docker container on Unraid
- expose a FastAPI service
- create and validate its SQLite database
- scan configured folders without moving files
- record photo metadata and checksums
- later detect duplicates and plan reorganization

## Unraid paths

PhotoVault application data:

```text
/mnt/user/photovault/
├── database/
├── config/
├── logs/
└── reports/
```

The Docker container will see Unraid shares under:

```text
/storage
```

and that mount is read-only during the first milestone.

## Development

Run locally with:

```bash
docker compose up --build
```

Then open:

- http://localhost:5000/
- http://localhost:5000/health
- http://localhost:5000/docs

## Status

Early development / foundation phase.
