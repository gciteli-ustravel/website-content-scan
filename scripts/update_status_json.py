#!/usr/bin/env python3
"""Update the GitHub Pages dashboard status file."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def parse_bool(value: str | None) -> bool | None:
    if value is None or value == "":
        return None
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--message")
    parser.add_argument("--last-run-at")
    parser.add_argument("--last-run-result")
    parser.add_argument("--last-upload-processed-at")
    parser.add_argument("--last-upload-result")
    parser.add_argument("--smartsheet-connection-ok")
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--connection-json", type=Path)
    parser.add_argument("--workflow-version")
    parser.add_argument("--workflow-ref")
    parser.add_argument("--workflow-sha")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    current = load_json(args.path)

    if args.summary_json and args.summary_json.exists():
        summary = load_json(args.summary_json)
        current["last_run_summary"] = summary
        current["last_run_at"] = summary.get("finished_at", args.last_run_at)

    if args.connection_json and args.connection_json.exists():
        connection = load_json(args.connection_json)
        current["smartsheet_connection_ok"] = connection.get("smartsheet_connection_ok")
        if connection.get("sheet_name"):
            current["smartsheet_sheet_name"] = connection["sheet_name"]

    if args.message is not None:
        current["message"] = args.message
    if args.last_run_at not in (None, ""):
        current["last_run_at"] = args.last_run_at
    if args.last_run_result not in (None, ""):
        current["last_run_result"] = args.last_run_result
    if args.last_upload_processed_at not in (None, ""):
        current["last_upload_processed_at"] = args.last_upload_processed_at
    if args.last_upload_result not in (None, ""):
        current["last_upload_result"] = args.last_upload_result

    parsed_connection = parse_bool(args.smartsheet_connection_ok)
    if parsed_connection is not None:
        current["smartsheet_connection_ok"] = parsed_connection

    if args.workflow_version not in (None, ""):
        current["workflow_version"] = args.workflow_version
    if args.workflow_ref not in (None, ""):
        current["workflow_ref"] = args.workflow_ref
    if args.workflow_sha not in (None, ""):
        current["workflow_sha"] = args.workflow_sha

    current["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    args.path.parent.mkdir(parents=True, exist_ok=True)
    args.path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(current, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
