# Upgrade to PhotoVault 0.8 — Photo Filter

Version 0.8 adds a production photo-archive filter and persistent exclusions.

## What changes

- Default archive media keeps JPEG/JPG, PNG, TIFF, HEIC/HEIF, supported RAW formats and video formats.
- GIF, BMP, WebP, AVIF and ICO are excluded from the default archive profile.
- The organizer applies the same filter as a second safety layer, including against older database rows.
- The Unraid compose file now contains the known `disk_1` exclusions, so they do not have to be typed into Swagger for each production scan.
- New `GET /filter/config` shows the effective filter and fixed exclusions.
- Version is now `0.8.0`.

## Important production step

After deploying 0.8, create a backup of the 0.7 database and start with a fresh `photovault.db` before the final production scan. This removes previously indexed GIF/BMP/system graphics from statistics and duplicate counts.

The source `/storage` remains read-only. Safe-copy still writes only to `/output`; source deletion is not implemented.
