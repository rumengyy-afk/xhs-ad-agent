#!/usr/bin/env python3
"""Download cover images from parsed Xiaohongshu browser-card CSV output."""

from __future__ import annotations

import argparse
import csv
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


def safe_name(value: str) -> str:
    value = re.sub(r"[^\w.-]+", "_", value.strip(), flags=re.UNICODE)
    return value[:80] or "cover"


def ext_from_url(url: str) -> str:
    path = url.split("?", 1)[0].lower()
    for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        if path.endswith(ext):
            return ext
    return ".jpg"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def download(url: str, out: Path, referer: str = "https://www.xiaohongshu.com/") -> bool:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": referer,
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 1024:
            return False
        out.write_bytes(data)
        return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path, help="Parsed xhs_browser_cards_top.csv")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--out-dir", type=Path, default=Path("covers"))
    parser.add_argument("--sleep", type=float, default=0.2)
    args = parser.parse_args()

    rows = read_rows(args.csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    ok = 0
    for row in rows[: args.top]:
        url = (row.get("cover_image_url") or "").strip()
        if not url:
            manifest.append({**row, "local_cover_path": "", "download_status": "missing_url"})
            continue
        rank = row.get("rank") or str(len(manifest) + 1)
        note_id = row.get("note_id") or safe_name(row.get("title", ""))
        out = args.out_dir / f"rank{int(rank):02d}_{safe_name(note_id)}{ext_from_url(url)}"
        status = "ok" if download(url, out, row.get("url") or "https://www.xiaohongshu.com/") else "failed"
        if status == "ok":
            ok += 1
        manifest.append({**row, "local_cover_path": str(out if status == "ok" else ""), "download_status": status})
        time.sleep(args.sleep)

    manifest_path = args.out_dir / "cover_manifest.csv"
    fields = sorted({key for row in manifest for key in row.keys()})
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manifest)
    print(f"downloaded={ok} requested={min(args.top, len(rows))} manifest={manifest_path}")


if __name__ == "__main__":
    main()
