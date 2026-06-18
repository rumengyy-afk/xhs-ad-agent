# Chrome Capture Workflow

Use this when the user has opened or can open a Xiaohongshu search page in Chrome, especially when login, current sort state, or dynamic loading matters.

## Preconditions

- Use the Chrome plugin/control-chrome skill if the user mentions `@chrome` or needs their logged-in browser state.
- Claim the existing Xiaohongshu tab from `browser.user.openTabs()`; do not reload it if the user already sorted or filtered the page.
- Prefer the `图文` tab when the user asks for image-text notes.
- If the user says they changed the sort to top likes, trust the visible page state but label results as current loaded search results unless Xiaohongshu exposes an official total ranking.

## Capture Steps

1. Connect to Chrome and read browser documentation as required by the Chrome skill.
2. List open tabs and claim the matching Xiaohongshu tab by title or URL.
3. Take one DOM snapshot to confirm:
   - keyword in search box
   - active tab/filter such as `图文`
   - visible note cards include titles, author/date, and like counts
4. Run a bounded extraction loop:
   - collect all visible `a[href*="/search_result/"]` note links
   - store `href`, `noteId`, and compact `cardText`
   - scroll down, wait briefly, repeat
   - stop after Top N is likely satisfied or results stop increasing
5. Save raw JSON before parsing.
6. Parse with `scripts/parse_xhs_browser_cards.py` or equivalent logic.
7. Rank by numeric likes descending and produce the analysis.
8. Finalize Chrome tabs, keeping the user tab as handoff if useful.

## Browser Extraction Snippet

Run through the Chrome-controlled tab after assigning `tab`:

```js
globalThis.xhsSeen = globalThis.xhsSeen || new Map();

async function extractXhsCards() {
  const rows = await tab.playwright.evaluate(() => {
    function txt(el) {
      return (el && el.innerText || "").replace(/\s+/g, " ").trim();
    }
    const links = [...document.querySelectorAll('a[href*="/search_result/"]')];
    const out = [];
    const seen = new Set();
    for (const a of links) {
      const href = a.href;
      if (!href || !/\/search_result\/[0-9a-f]/.test(href) || seen.has(href)) continue;
      seen.add(href);
      let card = a;
      for (let i = 0; i < 7 && card && card.parentElement; i++) {
        card = card.parentElement;
        const t = txt(card);
        if (t.length > 8 && /\d|赞/.test(t) && t.length < 700) break;
      }
      const cardText = txt(card);
      if (!cardText || cardText.includes("大家都在搜")) continue;
      out.push({
        href,
        noteId: (href.match(/search_result\/([^?]+)/) || [])[1] || "",
        cardText
      });
    }
    return out;
  }, undefined, { timeoutMs: 10000 });
  for (const row of rows) xhsSeen.set(row.href, row);
  return rows.length;
}

for (let i = 0; i < 8; i++) {
  await extractXhsCards();
  await tab.cua.scroll({ x: 900, y: 700, scrollY: 900, scrollX: 0 });
  await tab.playwright.waitForTimeout(900);
}
await extractXhsCards();
nodeRepl.write(JSON.stringify([...xhsSeen.values()], null, 2));
```

## Parsing Notes

Card text usually follows:

`title author publish_date likes`

Use heuristics, not certainty:

- Date patterns include `YYYY-MM-DD`, `MM-DD`, `昨天 22:31`, `1天前`, `5小时前`.
- The last token is usually the visible like count.
- `赞` without a number means missing/hidden likes, not zero.
- Author parsing can fail when a title or username contains spaces. Flag uncertain rows instead of inventing values.

## Reporting Language

Use wording like:

> Collected 131 unique note links from the current loaded Chrome search results; 130 had visible numeric likes. Ranked the parsed rows by visible likes. This is not an official Xiaohongshu full-platform ranking.
