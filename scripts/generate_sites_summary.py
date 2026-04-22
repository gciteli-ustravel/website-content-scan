#!/usr/bin/env python3
"""Create a user-friendly summary of the current site scan configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - only used on minimally set up machines.
    yaml = None

from update_scan import parse_simple_sites_yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_sites(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    if yaml:
        payload = yaml.safe_load(text) or {}
    else:
        payload = parse_simple_sites_yaml(text)
    sites = payload.get("sites", [])
    if not isinstance(sites, list):
        raise ValueError("sites.yml must contain a sites list")
    return sites


def summarize_site(site: dict[str, object]) -> dict[str, object]:
    exclusions = [str(value) for value in site.get("exclude_paths", []) or []]
    return {
        "name": str(site.get("name", "")),
        "sitemap": str(site.get("sitemap", "")),
        "excluded_sections": exclusions,
        "uses_manual_fallback": bool(site.get("fallback_sitemap_file")),
        "manual_fallback_file": str(site.get("fallback_sitemap_file", "")),
        "allows_sitemap_errors": bool(site.get("allow_sitemap_errors")),
    }


def main() -> int:
    args = parse_args()
    summary = {
        "sites": [summarize_site(site) for site in load_sites(args.config)],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
