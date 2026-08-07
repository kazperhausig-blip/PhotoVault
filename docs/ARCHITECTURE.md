
# PhotoVault Architecture

PhotoVault 0.2 scans the Unraid media tree read-only, computes file metadata and SHA-256 hashes, and stores an index in SQLite.

The filesystem remains the source of truth. SQLite can be rebuilt.
