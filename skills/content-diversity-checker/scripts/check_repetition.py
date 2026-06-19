#!/usr/bin/env python3
"""Lightweight repetition scanner for generated content drafts.

The script is intentionally simple: it flags repeated phrases, repeated line
openings, and highly similar lines. Use the output as a signal for a human or
agent diversity review, not as the final verdict.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        return json.dumps(data, ensure_ascii=False, indent=2)
    return raw


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def ngrams(tokens: list[str], n: int) -> Counter[str]:
    return Counter(" ".join(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1)))


def useful_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 8 and not set(line) <= {"-", "|", ":", "#", "*", " "}:
            lines.append(line)
    return lines


def repeated_openings(lines: list[str], chars: int = 8) -> list[dict[str, object]]:
    counts = Counter(line[:chars] for line in lines if len(line) >= chars)
    return [
        {"opening": opening, "count": count}
        for opening, count in counts.most_common()
        if count > 1
    ][:20]


def similar_line_pairs(lines: list[str], threshold: float) -> list[dict[str, object]]:
    pairs = []
    for i, left in enumerate(lines):
        for j in range(i + 1, len(lines)):
            right = lines[j]
            ratio = SequenceMatcher(None, left, right).ratio()
            if ratio >= threshold:
                pairs.append(
                    {
                        "line_a": i + 1,
                        "line_b": j + 1,
                        "similarity": round(ratio, 3),
                        "a": left,
                        "b": right,
                    }
                )
    return sorted(pairs, key=lambda row: row["similarity"], reverse=True)[:30]


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan generated content for repetition signals.")
    parser.add_argument("input", type=Path, help="Markdown, text, or JSON file to scan.")
    parser.add_argument("--ngram", type=int, default=3, help="Token n-gram size. Default: 3.")
    parser.add_argument("--min-count", type=int, default=3, help="Minimum repeated n-gram count. Default: 3.")
    parser.add_argument("--similarity", type=float, default=0.82, help="Similar-line threshold. Default: 0.82.")
    args = parser.parse_args()

    text = read_text(args.input)
    tokens = tokenize(text)
    lines = useful_lines(text)
    repeated_phrases = [
        {"phrase": phrase, "count": count}
        for phrase, count in ngrams(tokens, args.ngram).most_common(50)
        if count >= args.min_count
    ]

    result = {
        "input": str(args.input),
        "token_count": len(tokens),
        "line_count": len(lines),
        "repeated_phrases": repeated_phrases,
        "repeated_openings": repeated_openings(lines),
        "similar_line_pairs": similar_line_pairs(lines, args.similarity),
        "signal": "revise" if repeated_phrases or repeated_openings(lines) or similar_line_pairs(lines, args.similarity) else "pass",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
