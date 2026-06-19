# Chrome Capture Workflow

Use this reference when the user mentions `@chrome`, asks Codex to run the Xiaohongshu research automatically, or needs logged-in Chrome state for Xiaohongshu search results.

## Preconditions

- Use the `chrome:control-chrome` skill and the Node REPL execution tool.
- Prefer claiming an existing Xiaohongshu tab if the user already opened, filtered, or sorted the page. Open a new tab only when no useful tab exists or the user provides a fresh search URL.
- Prefer the image-text/note result type when the user asks for image-text notes, covers, or carousel-style posts.
- Respect platform controls. Do not bypass login, captcha, paywall, rate limits, or anti-bot mechanisms.
- Label results as "current loaded search results" unless Xiaohongshu itself provides an official complete ranking.

## Chrome Bootstrap

After reading the Chrome skill, initialize the Chrome extension browser runtime from Node REPL:

```js
const { setupBrowserRuntime } = await import("C:/Users/rumen/.codex/plugins/cache/openai-bundled/chrome/26.611.62324/scripts/browser-client.mjs");
await setupBrowserRuntime({ globals: globalThis });
globalThis.browser = await agent.browsers.get("extension");
nodeRepl.write(await browser.documentation());
```

If the exact version folder changes, locate the current `chrome/*/scripts/browser-client.mjs` under `C:/Users/rumen/.codex/plugins/cache/openai-bundled/chrome/`.

## Open Or Claim Search Page

For a new keyword search, URL-encode the keyword and open a search page:

```js
var tab = await browser.tabs.new();
await tab.goto("https://www.xiaohongshu.com/search_result?keyword=%E6%9D%8F%E4%BB%81%20%E5%81%A5%E5%BA%B7&source=web_search_result_notes&type=51");
await tab.playwright.waitForLoadState({ state: "domcontentloaded", timeoutMs: 15000 }).catch(() => {});
await tab.playwright.waitForTimeout(5000);
```

For an existing user tab, list tabs and claim the Xiaohongshu tab instead of reloading it:

```js
const tabs = await browser.user.openTabs();
nodeRepl.write(JSON.stringify(tabs.map((t, i) => ({ i, title: t.title, url: t.url })), null, 2));
```

## Extract Visible Cards

Run this against the assigned `tab`. It captures note links, compact card text, cover image URL, and cover alt text.

```js
var xhsSeen = new Map();

async function extractXhsCards() {
  const rows = await tab.playwright.evaluate(() => {
    function txt(el) {
      return (el && el.innerText || "").replace(/\s+/g, " ").trim();
    }
    function bestImgUrl(img) {
      if (!img) return "";
      return img.currentSrc || img.src || img.getAttribute("data-src") || img.getAttribute("src") || "";
    }
    const links = [...document.querySelectorAll('a[href*="/search_result/"]')];
    const out = [];
    const seen = new Set();
    for (const a of links) {
      const href = a.href;
      if (!href || !/\/search_result\/[0-9a-f]/.test(href) || seen.has(href)) continue;
      seen.add(href);
      let card = a;
      for (let i = 0; i < 8 && card && card.parentElement; i++) {
        card = card.parentElement;
        const t = txt(card);
        if (t.length > 8 && /\d|赞|万/.test(t) && t.length < 900) break;
      }
      const cardText = txt(card);
      if (!cardText || cardText.includes("大家都在搜")) continue;
      const img = card.querySelector("img");
      out.push({
        href,
        noteId: (href.match(/search_result\/([^?/#]+)/) || [])[1] || "",
        cardText,
        coverImageUrl: bestImgUrl(img),
        coverAlt: img ? (img.alt || "") : ""
      });
    }
    return out;
  }, undefined, { timeoutMs: 10000 });
  for (const row of rows) xhsSeen.set(row.href, row);
  return rows.length;
}
```

Scroll and re-extract until enough cards are loaded:

```js
for (let i = 0; i < 10; i++) {
  await extractXhsCards();
  await tab.cua.scroll({ x: 900, y: 740, scrollY: 850, scrollX: 0 });
  await tab.playwright.waitForTimeout(900);
}
await extractXhsCards();
nodeRepl.write(JSON.stringify({ count: xhsSeen.size, withCover: [...xhsSeen.values()].filter(r => r.coverImageUrl).length }, null, 2));
```

If `tab.cua.scroll` times out but `xhsSeen` already contains at least 5 top-ranked cards with cover URLs, continue with the partial evidence and state the limitation. Otherwise retry with `await tab.playwright.evaluate(() => window.scrollBy(0, 900));` or ask the user for screenshots/export.

## Save Raw Capture

Always save raw JSON before parsing:

```js
const fs = await import("node:fs");
const rawPath = "C:/Users/rumen/Documents/almond/output/xhs_chrome_keyword_raw.json";
fs.writeFileSync(rawPath, JSON.stringify([...xhsSeen.values()], null, 2), "utf8");
nodeRepl.write(rawPath);
```

## Parse And Download Covers

Parse the raw card JSON:

```bash
python C:/Users/rumen/.codex/skills/xhs-viral-note-crawler/scripts/parse_xhs_browser_cards.py C:/Users/rumen/Documents/almond/output/xhs_chrome_keyword_raw.json --top 20 --out-dir C:/Users/rumen/Documents/almond/output/xhs_chrome_keyword
```

Download the highest-ranked cover images:

```bash
python C:/Users/rumen/.codex/skills/xhs-viral-note-crawler/scripts/download_xhs_cover_images.py C:/Users/rumen/Documents/almond/output/xhs_chrome_keyword/xhs_browser_cards_top.csv --top 12 --out-dir C:/Users/rumen/Documents/almond/output/xhs_chrome_keyword/covers
```

Expected artifacts:

- raw JSON from Chrome, for example `xhs_chrome_keyword_raw.json`
- `xhs_browser_cards_clean.csv`
- `xhs_browser_cards_top.csv`
- `xhs_browser_cards_top.md`
- `xhs_browser_cards_summary.json`
- `covers/cover_manifest.csv`
- downloaded `covers/rankXX_*` image files

## Visual Evidence Gate

Before handing the data to `xhs-ad-image-style` or generating images:

- Require at least 5 top-ranked image-text notes with `cover_image_url` or a local cover/screenshot.
- Prefer Top 10-20 covers when available.
- Inspect representative downloaded covers directly before writing prompts.
- Cite source ranks/images for every output image route.
- If this gate fails, do not generate product images. Ask for screenshots, logged-in browser access, or an export with cover images.

## Finalize Chrome

When finished, keep the useful user tab as handoff:

```js
await browser.tabs.finalize({ keep: [{ tab, status: "handoff" }] });
```

## Reporting Language

Use wording like:

> Collected 20 unique image-text note cards from the current loaded Chrome search results; 20 had cover image URLs. Ranked parsed rows by visible likes. This is not an official Xiaohongshu full-platform ranking.
