---
name: xhs-viral-note-crawler
description: Collect, rank, and analyze Xiaohongshu/小红书 viral image-text notes for a keyword using a logged-in Chrome tab, browser-visible search results, or exported CSV/JSON data. Use when Codex needs to research top-liked XHS notes, operate a user-opened Xiaohongshu search page with the Chrome plugin, crawl or normalize exported XHS search data, filter 图文笔记 versus video notes, build a Top N dataset by likes, or deconstruct viral note titles, covers, hooks, comments, selling points, and content patterns for Chinese social content strategy.
---

# XHS Viral Note Crawler

## Core Rule

Only report notes that are backed by captured or exported source data. Do not invent Top 50 entries from memory, public search snippets, or incomplete pages. If Xiaohongshu blocks access, requires login, rate-limits, or hides likes, ask for a logged-in browser session, screen recording, HAR/export, CSV, or screenshots, then continue from that artifact.

Respect platform terms, privacy, and robots guidance. Do not bypass captchas, paywalls, authentication, or anti-bot controls. Use normal logged-in browsing, user-provided exports, or licensed third-party datasets.

## Workflow

1. Define the research scope:
   - keyword, such as `杏仁酱`
   - note type: default `image-text` only
   - ranking metric: default `likes` descending
   - sample size: default Top 50
   - date window, market, language, and account exclusions if provided
2. Collect evidence:
   - Prefer a logged-in Chrome tab already opened by the user on Xiaohongshu, sorted or filtered as requested.
   - If the user mentions `@chrome`, asks for automatic execution, or Chrome control is available, read `references/chrome-capture-workflow.md` and use that workflow before asking the user for screenshots.
   - Capture note URL/id, title, author, like count, collect count, comment count, publish date, cover image URL, cover alt/text, image count, body text, tags, and whether it is image-text or video.
   - For image generation workflows, capture or download cover images for the highest-ranked notes. Minimum acceptable visual evidence is Top 5 with cover images or screenshots; preferred is Top 10-20.
   - Save raw browser captures or exports before cleaning. Use CSV or JSON whenever possible.
3. Normalize and rank:
   - Run `scripts/normalize_xhs_notes.py` on CSV/JSON exports.
   - Deduplicate by `note_id` or URL.
   - Filter to image-text notes when requested.
   - Sort by numeric likes descending and keep Top N.
4. Deconstruct the winners:
   - Read `references/deconstruction-framework.md` before writing analysis.
   - Analyze title hooks, cover framing, pain point, audience, scene, product role, trust proof, recipe/use case, comment triggers, and conversion path.
5. Deliver:
   - Include source limitations and collection method.
   - Provide the Top N table with URLs/ids and metrics.
   - Summarize repeatable content patterns and specific creative angles.
   - Keep raw data, cleaned data, and analysis outputs separate.

## Data Capture Guidance

For browser-based capture, gather what is visible without automated circumvention:

- Use the user's logged-in Chrome page when the page depends on cookies, current sort state, or dynamic loading.
- Keep the search page state intact. Claim the existing tab instead of reloading when the user already sorted or filtered it.
- Scroll search results until enough candidate notes are loaded.
- Open candidate notes in new tabs when list cards do not show reliable metrics.
- Record the visible note type. Treat autoplay, progress bar, or explicit video marker as video unless the detail page proves otherwise.
- Convert Chinese counters accurately: `1.2万` = `12000`, `3千` = `3000`, `赞过万` is not a precise value and should be flagged as approximate.
- Mark missing metrics as blank/null, not zero.

If a third-party analytics platform is used, record platform name, export timestamp, filter settings, and whether the data is estimated.

## Scripts

Use the normalizer for repeatable cleaning:

```bash
python scripts/normalize_xhs_notes.py input.csv --top 50 --type image-text --out-dir output
```

Use the browser-card parser when Chrome capture produces JSON objects with `cardText`, `href`, and `noteId`:

```bash
python scripts/parse_xhs_browser_cards.py raw_browser_cards.json --top 50 --out-dir output
```

Accepted input formats:

- `.csv`
- `.json` containing either a list of note objects or an object with a `notes` list

Common input aliases are handled, including Chinese headers such as `标题`, `作者`, `点赞数`, `收藏数`, `评论数`, `链接`, `笔记类型`, `发布时间`.

Outputs:

- `xhs_notes_clean.csv`
- `xhs_notes_top.csv`
- `xhs_notes_top.md`
- `xhs_notes_summary.json`
 - when cover URLs are available, downloaded cover files under a `covers/` directory

For Chrome/browser captures, also keep the raw JSON used to create the final table.

When the Chrome workflow is used, the minimum saved set is raw JSON, parsed clean CSV, parsed top CSV/MD, summary JSON, cover manifest, and downloaded cover images when cover URLs exist.

Use the cover downloader after parsing browser-card output when `cover_image_url` exists:

```bash
python scripts/download_xhs_cover_images.py output/xhs_browser_cards_top.csv --top 20 --out-dir output/covers
```

## Quality Checks

Before finalizing:

- Confirm every Top N row has a URL or stable note id.
- Confirm likes are numeric or explicitly marked approximate/missing.
- Confirm the table is sorted descending by likes.
- Confirm image-text filtering did not include obvious videos.
- For any downstream image generation, confirm at least 5 top-ranked rows have `cover_image_url` or a local screenshot/cover image. If not, report that visual generation is blocked and ask for screenshots or logged-in browser access.
- For any downstream image generation, inspect or provide local paths for representative downloaded covers before calling `xhs-ad-image-style`; do not pass only titles and like counts.
- State how many raw candidates were collected, how many survived dedupe/filtering, and whether Top N was fully satisfied.
- For Chrome captures, label the output as "current loaded search results" unless the platform itself exposes an official complete ranking.

## When Data Is Incomplete

Say exactly what is missing and continue with the best supported partial result. Do not fill gaps with generic XHS advice. For example:

> I collected 31 unique image-text notes with visible likes. Xiaohongshu hid metrics after login timeout, so this is not a verified Top 50. Provide a fresh export or logged-in browser access to complete the ranking.
