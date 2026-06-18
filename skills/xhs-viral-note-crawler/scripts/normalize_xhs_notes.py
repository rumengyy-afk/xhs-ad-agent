#!/usr/bin/env python3
"""Normalize exported Xiaohongshu note data and produce ranked Top N files."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


FIELD_ALIASES = {
    "note_id": ["note_id", "id", "笔记id", "笔记ID", "作品id", "作品ID"],
    "url": ["url", "link", "链接", "笔记链接", "作品链接"],
    "title": ["title", "标题", "笔记标题"],
    "author": ["author", "nickname", "user", "作者", "昵称", "博主"],
    "likes": ["likes", "like_count", "点赞", "点赞数", "获赞", "赞"],
    "collects": ["collects", "favorites", "收藏", "收藏数"],
    "comments": ["comments", "comment_count", "评论", "评论数"],
    "publish_date": ["publish_date", "published_at", "date", "发布时间", "发布日期"],
    "note_type": ["note_type", "type", "类型", "笔记类型", "内容类型"],
    "cover_text": ["cover_text", "封面文案", "封面文字"],
    "image_count": ["image_count", "图片数", "图数"],
    "body_text": ["body_text", "content", "正文", "笔记正文", "内容"],
    "hashtags": ["hashtags", "tags", "话题", "标签"],
}


def parse_count(value: Any) -> Tuple[int | None, bool]:
    if value is None:
        return None, False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if math.isnan(value) if isinstance(value, float) else False:
            return None, False
        return int(value), False
    text = str(value).strip().replace(",", "")
    if not text or text in {"-", "null", "None", "无"}:
        return None, False
    approximate = any(token in text for token in ["+", "过", "约", "w+"])
    text = text.lower().replace("赞", "").replace("收藏", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)\s*([万w千k]?)", text)
    if not match:
        return None, approximate
    number = float(match.group(1))
    unit = match.group(2)
    multiplier = 1
    if unit in {"万", "w"}:
        multiplier = 10000
    elif unit in {"千", "k"}:
        multiplier = 1000
    return int(number * multiplier), approximate


def normalize_type(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"图文", "image", "image-text", "images", "note", "普通笔记"}:
        return "image-text"
    if text in {"视频", "video", "short_video"}:
        return "video"
    return text


def pick(row: Dict[str, Any], canonical: str) -> Any:
    lowered = {str(k).strip().lower(): v for k, v in row.items()}
    for alias in FIELD_ALIASES[canonical]:
        if alias in row and row[alias] not in (None, ""):
            return row[alias]
        key = alias.lower()
        if key in lowered and lowered[key] not in (None, ""):
            return lowered[key]
    return ""


def load_rows(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            data = data.get("notes", data.get("data", []))
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list or an object with notes/data list")
        return [dict(item) for item in data if isinstance(item, dict)]
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for raw in rows:
        likes, likes_approx = parse_count(pick(raw, "likes"))
        collects, collects_approx = parse_count(pick(raw, "collects"))
        comments, comments_approx = parse_count(pick(raw, "comments"))
        row = {
            "note_id": str(pick(raw, "note_id")).strip(),
            "url": str(pick(raw, "url")).strip(),
            "title": str(pick(raw, "title")).strip(),
            "author": str(pick(raw, "author")).strip(),
            "likes": likes,
            "likes_approx": likes_approx,
            "collects": collects,
            "collects_approx": collects_approx,
            "comments": comments,
            "comments_approx": comments_approx,
            "publish_date": str(pick(raw, "publish_date")).strip(),
            "note_type": normalize_type(pick(raw, "note_type")),
            "cover_text": str(pick(raw, "cover_text")).strip(),
            "image_count": str(pick(raw, "image_count")).strip(),
            "body_text": str(pick(raw, "body_text")).strip(),
            "hashtags": str(pick(raw, "hashtags")).strip(),
        }
        if not row["note_id"] and row["url"]:
            row["note_id"] = row["url"].rstrip("/").split("/")[-1].split("?")[0]
        out.append(row)
    return out


def dedupe(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for row in rows:
        key = row.get("note_id") or row.get("url") or (row.get("title"), row.get("author"))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fields = [
        "rank", "note_id", "url", "title", "author", "likes", "likes_approx",
        "collects", "collects_approx", "comments", "comments_approx",
        "publish_date", "note_type", "cover_text", "image_count", "body_text", "hashtags",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: List[Dict[str, Any]]) -> None:
    lines = ["| Rank | Likes | Title | Author | Type | URL |", "|---:|---:|---|---|---|---|"]
    for row in rows:
        title = str(row.get("title", "")).replace("|", "\\|")
        author = str(row.get("author", "")).replace("|", "\\|")
        url = row.get("url", "")
        link = f"[link]({url})" if url else ""
        lines.append(f"| {row.get('rank')} | {row.get('likes') or ''} | {title} | {author} | {row.get('note_type') or ''} | {link} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--type", choices=["all", "image-text", "video"], default="image-text")
    parser.add_argument("--out-dir", type=Path, default=Path("xhs_output"))
    args = parser.parse_args()

    raw_rows = load_rows(args.input)
    clean = dedupe(normalize_rows(raw_rows))
    if args.type != "all":
        clean = [r for r in clean if r["note_type"] in {"", args.type}]
    clean.sort(key=lambda r: (r["likes"] is not None, r["likes"] or -1), reverse=True)
    for index, row in enumerate(clean, start=1):
        row["rank"] = index
    top = clean[: args.top]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "xhs_notes_clean.csv", clean)
    write_csv(args.out_dir / "xhs_notes_top.csv", top)
    write_markdown(args.out_dir / "xhs_notes_top.md", top)
    summary = {
        "raw_count": len(raw_rows),
        "clean_count": len(clean),
        "top_count": len(top),
        "requested_top": args.top,
        "type_filter": args.type,
        "complete_top": len(top) >= args.top,
        "missing_like_count": sum(1 for r in clean if r["likes"] is None),
    }
    (args.out_dir / "xhs_notes_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
