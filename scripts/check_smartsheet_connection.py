#!/usr/bin/env python3
"""Check whether the configured Smartsheet sheet is reachable."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sheet-id", default=os.environ.get("SMARTSHEET_SHEET_ID"))
    parser.add_argument("--output", type=Path, help="Optional path to write the JSON result")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("SMARTSHEET_ACCESS_TOKEN")
    if not token:
        raise SystemExit("SMARTSHEET_ACCESS_TOKEN is required")
    if not args.sheet_id:
        raise SystemExit("SMARTSHEET_SHEET_ID or --sheet-id is required")

    url = f"https://api.smartsheet.com/2.0/sheets/{args.sheet_id}"
    response = requests.get(url, timeout=30, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    payload = response.json()
    result = {
        "smartsheet_connection_ok": True,
        "sheet_id": str(args.sheet_id),
        "sheet_name": payload.get("name", ""),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
