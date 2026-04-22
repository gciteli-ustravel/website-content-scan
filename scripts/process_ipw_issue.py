#!/usr/bin/env python3
"""Download an IPW sitemap attachment from a GitHub issue and save it locally."""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

import requests


TARGET_PATH = Path("manual-sitemaps/ipw.com/sitemap.xml")
URL_PATTERN = re.compile(r"https?://[^\s)>]+")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\((https?://[^)]+)\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-path", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Optional path to write the JSON result")
    return parser.parse_args()


def issue_attachment_urls(body: str) -> list[str]:
    urls: list[str] = []
    for pattern in (MARKDOWN_IMAGE_PATTERN, MARKDOWN_LINK_PATTERN):
        urls.extend(pattern.findall(body))
    urls.extend(URL_PATTERN.findall(body))

    ordered: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        ordered.append(url)
    return ordered


def looks_like_sitemap_url(url: str) -> bool:
    lower = url.lower()
    return lower.endswith((".xml", ".xml.gz", ".gz")) or "githubusercontent.com" in lower or "attachments" in lower


def url_priority(url: str) -> tuple[int, str]:
    host = urlparse(url).netloc.lower()
    if "githubusercontent.com" in host or "attachments" in host:
        return (0, url)
    if url.lower().endswith((".xml", ".xml.gz", ".gz")):
        return (1, url)
    return (2, url)


def load_xml_bytes(url: str) -> bytes:
    headers = {"Accept": "application/octet-stream"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_error: Exception | None = None
    for use_auth in (True, False):
        try_headers = headers if use_auth else {"Accept": "application/octet-stream"}
        try:
            response = requests.get(url, timeout=60, headers=try_headers)
            response.raise_for_status()
            content = response.content
            if content[:2] == b"\x1f\x8b":
                content = gzip.decompress(content)
            return content
        except Exception as exc:  # pragma: no cover - exercised in workflow
            last_error = exc
    raise RuntimeError(f"Could not download sitemap attachment: {last_error}")


def validate_sitemap(content: bytes) -> None:
    root = ElementTree.fromstring(content)
    name = root.tag.rsplit("}", 1)[-1]
    if name not in {"urlset", "sitemapindex"}:
        raise ValueError(f"Attachment root element must be urlset or sitemapindex, found {name}")


def build_result(success: bool, **values: object) -> dict[str, object]:
    result: dict[str, object] = {"success": success}
    result.update(values)
    return result


def main() -> int:
    args = parse_args()
    event = json.loads(args.event_path.read_text(encoding="utf-8"))
    issue = event.get("issue", {})
    body = issue.get("body") or ""
    issue_number = issue.get("number")
    issue_url = issue.get("html_url")
    labels = [label.get("name", "") for label in issue.get("labels", [])]

    if "ipw-sitemap-upload" not in labels:
        result = build_result(False, message="Issue is not marked as an IPW sitemap upload.", issue_number=issue_number)
    else:
        urls = sorted((url for url in issue_attachment_urls(body) if looks_like_sitemap_url(url)), key=url_priority)
        if not urls:
            result = build_result(
                False,
                message="No sitemap attachment URL was found in the issue body. Attach the sitemap file and try again.",
                issue_number=issue_number,
                issue_url=issue_url,
            )
        else:
            selected_url = urls[0]
            content = load_xml_bytes(selected_url)
            validate_sitemap(content)
            target_path = args.repo_root / TARGET_PATH
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(content)
            filename = Path(urlparse(selected_url).path).name or "uploaded-sitemap.xml"
            result = build_result(
                True,
                message=f"Saved {filename} to {TARGET_PATH.as_posix()}",
                issue_number=issue_number,
                issue_url=issue_url,
                source_url=selected_url,
                target_path=TARGET_PATH.as_posix(),
            )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
