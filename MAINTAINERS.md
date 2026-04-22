# Maintainers Notes

This file is the “sleeper agent” guide for the backup path. Most users should never need it.

## What the backup is

The repo still contains an Excel fallback mode inside `scripts/update_scan.py`. It updates an exported workbook instead of the live Smartsheet.

This exists in case:

- the Smartsheet API is down
- the workflow secrets are broken
- the main automation needs emergency troubleshooting

## When to use it

Use the fallback only when the normal workflow cannot update Smartsheet and you still need a recoverable scan output.

## How to bring it back to life

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Export the Website Content Scan workbook from Smartsheet.

3. Run:

```bash
python3 scripts/update_scan.py \
  --config sites.yml \
  --excel-input "/path/to/Website Content Scan.xlsx" \
  --excel-output "/path/to/Website Content Scan.updated.xlsx"
```

4. Review the updated workbook before using it operationally.

## What to tell non-technical users

Tell them the backup exists, but that it is a maintainer-only recovery path. If they think they need it, they should ask AI or a maintainer for help rather than trying to run it on their own.
