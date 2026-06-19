---
name: xhs-viral-ad-agent
description: Orchestrate Xiaohongshu viral note collection, natural soft-ad content generation, and Xiaohongshu ad image style prompting into an end-to-end Chinese product seeding agent. Use when Codex needs to research a keyword, collect and deconstruct viral image-text notes, extract audience pains and content mechanics, turn those insights into product-specific advertorials, Xiaohongshu notes, native social posts, short-video scripts, seeded comments, soft-sell angles, titles, cover directions, visual style routes, product ad image prompts, CTAs, and publishing recommendations.
---

# XHS Viral Ad Agent

Use this skill as the orchestration layer for a complete Xiaohongshu viral-to-soft-ad-to-visual workflow. It does not replace the specialist skills; it coordinates them, extracts proven content and visual mechanics, and turns the combined evidence into native product content and Xiaohongshu-style ad image directions.

## Primary Operating Rule

For product image generation, this agent must not start from generic brand-card design. It must first extract the most popular image-text notes for the user's chosen keyword, capture their cover/carousel visual evidence, and then generate exactly 3 usable product images based on reusable visual mechanisms from those popular notes.

Default image deliverable:

1. **Click cover image**: based on the strongest high-like cover pattern.
2. **Trust/proof image**: based on a high-performing ingredient, comparison, process, or proof pattern.
3. **Use-scene image**: based on a high-performing lifestyle, recipe, breakfast, snack, or routine pattern.

If top-note cover images or screenshots cannot be captured, do not generate images. Ask the user to provide screenshots or a logged-in Xiaohongshu browser/export. Product-only card layouts are not an acceptable fallback unless the user explicitly asks for product-only creative.

When the user mentions `@chrome`, asks to run the agent automatically, or needs logged-in Xiaohongshu state, use the Chrome plugin path documented in `xhs-viral-note-crawler/references/chrome-capture-workflow.md` before asking for manual screenshots. Treat Chrome results as "current loaded search results" unless Xiaohongshu exposes an official complete ranking.

## Specialist Skills

Use the local specialist skills when their trigger conditions are met:

- `xhs-viral-note-crawler`: collect, rank, normalize, and analyze Xiaohongshu viral image-text notes for a keyword or exported dataset.
- `soft-ad-content`: turn content breakdowns, viral note patterns, hook analysis, and audience insight into product-specific soft ads, Xiaohongshu notes, short-video scripts, seeded comments, native ad angles, and brand-integrated social posts.
- `xhs-ad-image-style`: analyze high-performing Xiaohongshu image-note visuals and turn reusable photography, set design, color, composition, and commercial cues into product ad image style routes and generation prompts.

When the full agent is relevant, use this sequence:

1. Run note research first to understand searchable demand, audience language, title/cover patterns, pain points, comments, saves, and conversion signals.
2. Extract the most popular image-text notes for the chosen keyword, ranked by visible likes or the user's selected ranking metric.
3. Capture visual evidence for the top notes: cover image URLs, screenshots, downloaded cover files, or user-provided screenshots. Prefer at least Top 10 with usable covers; minimum Top 5.
4. Run soft-ad content generation to map the winning note mechanisms onto the user's product, scenario, proof, and decision moment.
5. Run ad image style generation to produce exactly 3 product image routes from the strongest observed visual mechanisms.
6. Synthesize into a creator-ready package: the source-note evidence, copy, 3 image prompts or generated images, and a short usage note.

## Intake

Clarify only what is necessary. If the user gives a keyword or niche, proceed with reasonable assumptions and label them.

Collect or infer:

- keyword, niche, product, account, or campaign goal
- target platform, defaulting to Xiaohongshu plus short video if unclear
- audience and desired creator persona
- product context: product name, category, core benefit, differentiator, price/offer, proof, usage scenario, and claim constraints
- visual context: product images, package shape, brand constraints, target ratio, required text/logo accuracy, and any source note images or screenshots
- available evidence: Xiaohongshu export, screenshots, links, transcripts, metrics, notes, or browser access
- desired output: research report, soft-ad note, short-video script, seeded comments, native ad angles, image prompts, cover style routes, content calendar, or all-in-one strategy

## Workflow

1. Define scope:
   - Set target platform, language, date window, content format, sample size, and ranking metric.
   - Default Xiaohongshu note research to Top 50 image-text notes by likes when data supports it.
   - State assumptions before analysis if inputs are partial.

2. Gather note evidence:
   - Use `xhs-viral-note-crawler` for Xiaohongshu collection, normalization, ranking, and note deconstruction.
   - If the user invokes `@chrome` or asks for automatic browser execution, read the Chrome control skill, connect to Chrome through the Node REPL runtime, open or claim the Xiaohongshu search tab, and save the raw card JSON before parsing.
   - Capture visual evidence for the highest-priority notes: cover image URL, screenshot, downloaded local image path, or user-provided note screenshot.
   - Required for image generation: at least 5 ranked image-text notes with visible cover evidence. If fewer than 5 covers are available, stop before image generation and request screenshots/export/login access.
   - Save the raw capture, cleaned/ranked table, cover manifest, and downloaded/source cover files separately.
   - Preserve the source method and limitations.
   - Do not invent ranked notes or metrics.

3. Generate soft-ad routes:
   - Use `soft-ad-content` after note evidence has produced a content breakdown, hook pattern, audience pain, or conversion signal.
   - Map the user's product to the observed mechanism without forcing the product into the opening hook too early.
   - If product context is incomplete, make limited assumptions and label them before drafting.

4. Generate image style routes:
   - Use `xhs-ad-image-style` only after note evidence includes usable cover/image evidence: crawled image URLs, screenshots, exported image paths, downloaded cover files, or user-provided note images.
   - Inspect representative downloaded covers before prompting image generation; do not rely on URLs, titles, or like counts alone.
   - Prioritize high-engagement images when likes, saves, comments, or rank are available.
   - Convert visual mechanics into exactly 3 product-safe image routes: click cover, trust/proof, and use-scene.
   - Each route must cite the source note ranks/images that informed it.
   - If exact packaging, label text, or logo accuracy matters, recommend using a real product image as reference rather than relying on generated text.
   - If no source visuals are available, do not generate generic Xiaohongshu-style images. Ask for note screenshots/images.

5. Compare patterns:
   - Map note patterns to native ad roles such as solution after pain, tool in a real scene, proof object, habit upgrade, comparison object, or comment-triggered recommendation.
   - Map observed cover/image patterns to visual roles such as lifestyle proof, ingredient flat lay, routine scene, comparison shot, texture close-up, or clean product hero.
   - Identify repeated audience pains, identities, promises, proof types, comment triggers, save triggers, and conversion paths.
   - Separate observed evidence from inference.

6. Produce:
   - Generate outputs the creator can directly use: top-note evidence, soft-ad note copy, product insertion lines, CTAs, and 3 source-derived image prompts or generated images.
   - If generated images are returned inline by the image tool and not written to disk, say that clearly and keep the source data/covers in the output folder for later regeneration.
   - Prefer fewer, sharper recommendations over generic advice.

Read `references/workflow.md` when the request asks for a full strategy, a content calendar, multiple scripts, or a reusable operating process.

## Output Contract

For end-to-end work, use this structure unless the user asks for another format:

```markdown
**一句话判断**
[这批内容最可能爆的核心机制]

**研究范围与证据**
- 关键词/赛道:
- 平台:
- 数据来源:
- 样本与限制:
- 产品/品牌假设:

**爆款笔记规律**
- 标题:
- 封面:
- 痛点/欲望:
- 信任证明:
- 评论/收藏触发:

**软广转化机会**
- 产品适合承接的用户痛点:
- 最自然的植入角色:
- 适合延迟露出的产品证明:
- 互动/评论触发:
- 需要避免的硬广表达:

**广告图视觉机会**
- 视觉证据来源:
- 参考笔记/图片:
- 可复用的封面/首图规律:
- 适合产品的视觉路线:
- 场景/道具/色调:
- 产品露出方式:
- 需要避免的视觉复制风险:

**可直接做的选题**
| 选题 | 笔记依据 | 软广钩子 | 产品植入方式 | 优先级 |
|---|---|---|---|---|

**软广内容方案**
- 小红书笔记标题/封面:
- 笔记正文:
- 短视频脚本:
- 产品插入句:
- 种草评论:
- CTA:

**广告图风格方案**
- 路线名称:
- 首图构图:
- 拍摄/生成提示词:
- Negative prompt:
- 推荐使用场景:

**发布建议**
- 账号定位:
- 发布节奏:
- A/B 测试:
- 复盘指标:
```

## Quality Rules

- Do not promise virality. Use calibrated language such as "提高爆发概率" or "更利于完播/收藏/互动".
- Do not copy protected creative expression. Extract mechanisms, then adapt to the user's audience, product, and creator persona.
- Do not copy a source image's exact layout, private person, creator identity, watermark, or recognizable branded composition.
- Do not make fake personal experience sound factual. Draft as a content script or clearly label assumptions when the user's own experience is not provided.
- Do not make medical, financial, or guaranteed-result claims unless the user provides compliant proof and constraints.
- Do not fabricate Xiaohongshu ranking data. If evidence is incomplete, state exactly what is missing and continue with a supported partial strategy.
- Do not generate repeated generic visuals when source-style evidence is missing. Either collect top-note cover images/screenshots first, or explicitly label the visual plan as a product-only creative direction.
- Distinguish observation from inference with phrases such as "从已采集笔记看", "从软广转化角度看", or "在缺少产品细节时，这是基于笔记规律的推断".
- Keep outputs practical: every recommendation should be usable as a title, cover, hook, native note paragraph, product insertion line, seeded comment, image prompt, shot list, or testable publishing action.
