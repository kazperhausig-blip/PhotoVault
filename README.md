# PhotoVault 0.6 – Safe Copy Engine

0.6 adds controlled copying from the read-only photo library to a dedicated writable output share.

The source library remains mounted read-only. PhotoVault does not delete, move, rename or modify originals.

## Output

The default Compose configuration maps:

`/mnt/user/photovault-output` -> `/output`

Preview destinations such as `/Photos/2006/09/DSCF0032[1].jpg` become:

`/output/Photos/2006/09/DSCF0032[1].jpg`

Exact extra duplicate copies become:

`/output/Duplicates/...`

## Copy guarantees

1. Source has an indexed SHA-256.
2. Destination must not already contain different data.
3. Data is copied to a temporary sibling file.
4. Temporary copy is SHA-256 verified.
5. Only a verified copy is atomically renamed to its final destination.
6. Results are stored in SQLite for audit/resume.
7. Originals are never deleted.

## API

- `GET /organize/preview`
- `POST /organize/execute`
- `GET /organize/execute/status`
- `GET /organize/jobs/{job_id}`

Execution requires the exact confirmation string `COPY_AND_VERIFY`.
