#!/usr/bin/env python3
"""Parse Xiaohongshu browser card captures into ranked note tables.

Expected browser JSON rows may include:
  href, noteId, cardText, coverImageUrl, coverAlt
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


DATE_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}|\d{2}-\d{2}|昨天\s*\d{1,2}:\d{2}|\d+天前|\d+小时前|昨天|前天)"
)
LIKE_RE = re.compile(r"(?:^| )(\d+(?:\.\d+)?(?:万|千|w|k)?|赞)$", re.I)


def parse_count(value: Any) -> Tuple[int | None, bool]:
    if value is None:
        return None, False
    text = str(value).strip().replace(",", "")
    if not text or text in {"-", "赞"}:
        return None, False
    approximate = any(token in text for token in ["+", "过", "约"])
    match = re.search(r"(\d+(?:\.\d+)?)\s*([万千wk]?)", text, re.I)
    if not match:
        return None, approximate
    number = float(match.group(1))
    unit = match.group(2).lower()
    multiplier = 10000 if unit in {"万", "w"} else 1000 if unit in {"千", "k"} else 1
    return int(number * multiplier), approximate


def load_cards(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("cards", data.get("notes", data.get("data", [])))
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON list or an object with cards/notes/data list")
    return [dict(item) for item in data if isinstance(item, dict)]


def first_present(card: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = card.get(key)
        if value:
            return str(value).strip()
    return ""


def parse_card(card: Dict[str, Any]) -> Dict[str, Any]:
    text = re.sub(r"\s+", " ", str(card.get("cardText", "")).strip())
    href = first_present(card, "href", "url")
    note_id = first_present(card, "noteId", "note_id")
    if not note_id and href:
        match = re.search(r"/search_result/([^?/#]+)", href)
        note_id = match.group(1) if match else href.rstrip("/").split("/")[-1].split("?")[0]

    like_match = LIKE_RE.search(text)
    likes_raw = like_match.group(1) if like_match else ""
    likes, likes_approx = parse_count(likes_raw)
    without_likes = text[: like_match.start()].strip() if like_match else text

    date_match = DATE_RE.search(without_likes)
    title = without_likes
    author = ""
    publish_date = ""
    parse_warning = ""
    if date_match:
        publish_date = re.sub(r"\s+", " ", date_match.group(1)).strip()
        before_date = without_likes[: date_match.start()].strip()
        tokens = before_date.split(" ")
        if len(tokens) >= 2:
            author = tokens[-1]
            title = " ".join(tokens[:-1]).strip()
        else:
            title = before_date
            parse_warning = "author_missing"
    else:
        parse_warning = "date_missing"

    return {
        "rank": "",
        "note_id": note_id,
        "url": href,
        "cover_image_url": first_present(card, "coverImageUrl", "cover_image_url", "image", "img"),
        "cover_alt": first_present(card, "coverAlt", "cover_alt", "alt"),
        "title": title,
        "author": author,
        "likes": likes,
        "likes_raw": likes_raw,
        "likes_approx": likes_approx,
        "publish_date": publish_date,
        "note_type": "image-text",
        "card_text": text,
        "source_method": "Chrome visible search results",
        "parse_warning": parse_warning,
    }


def dedupe(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for row in rows:
        key = row["note_id"] or row["url"] or row["card_text"]
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fields = [
        "rank",
        "note_id",
        "url",
        "cover_image_url",
        "cover_alt",
        "title",
        "author",
        "likes",
        "likes_raw",
        "likes_approx",
        "publish_date",
        "note_type",
        "card_text",
        "source_method",
        "parse_warning",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: List[Dict[str, Any]]) -> None:
    lines = [
        "| Rank | Likes | Title | Author | Date | Cover | URL |",
        "|---:|---:|---|---|---|---|---|",
    ]
    for row in rows:
        title = str(row["title"]).replace("|", "\\|")
        author = str(row["author"]).replace("|", "\\|")
        link = f"[link]({row['url']})" if row["url"] else ""
        cover = "yes" if row.get("cover_image_url") else ""
        likes = "" if row["likes"] is None else row["likes"]
        lines.append(
            f"| {row['rank']} | {likes} | {title} | {author} | {row['publish_date']} | {cover} | {link} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--out-dir", type=Path, default=Path("xhs_browser_output"))
    args = parser.parse_args()

    raw_cards = load_cards(args.input)
    parsed = dedupe(parse_card(card) for card in raw_cards)
    parsed.sort(
        key=lambda row: (row["likes"] is not None, row["likes"] if row["likes"] is not None else -1),
        reverse=True,
    )
    for index, row in enumerate(parsed, start=1):
        row["rank"] = index
    top = parsed[: args.top]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "xhs_browser_cards_clean.csv", parsed)
    write_csv(args.out_dir / "xhs_browser_cards_top.csv", top)
    write_markdown(args.out_dir / "xhs_browser_cards_top.md", top)
    summary = {
        "raw_count": len(raw_cards),
        "clean_count": len(parsed),
        "numeric_like_count": sum(1 for row in parsed if row["likes"] is not None),
        "missing_like_count": sum(1 for row in parsed if row["likes"] is None),
        "cover_image_count": sum(1 for row in parsed if row.get("cover_image_url")),
        "top_cover_image_count": sum(1 for row in top if row.get("cover_image_url")),
        "top_count": len(top),
        "requested_top": args.top,
        "complete_top": len(top) >= args.top,
        "source_method": "Chrome visible search results",
    }
    (args.out_dir / "xhs_browser_cards_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
