---
name: xhs-viral-ad-agent
description: Orchestrate Xiaohongshu viral note collection, natural soft-ad content generation, and Xiaohongshu ad image style prompting into an end-to-end Chinese product seeding agent. Use when Codex needs to research a keyword, collect and deconstruct viral image-text notes, extract audience pains and content mechanics, turn those insights into product-specific advertorials, Xiaohongshu notes, native social posts, short-video scripts, seeded comments, soft-sell angles, titles, cover directions, visual style routes, product ad image prompts, CTAs, and publishing recommendations.
---

# XHS Viral Ad Agent

Use this skill as the orchestration layer for a complete Xiaohongshu viral-to-soft-ad-to-visual workflow. It does not replace the specialist skills; it coordinates them, extracts proven content and visual mechanics, and turns the combined evidence into native product content and Xiaohongshu-style ad image directions.

## Specialist Skills

Use the local specialist skills when their trigger conditions are met:

- `xhs-viral-note-crawler`: collect, rank, normalize, and analyze Xiaohongshu viral image-text notes for a keyword or exported dataset.
- `soft-ad-content`: turn content breakdowns, viral note patterns, hook analysis, and audience insight into product-specific soft ads, Xiaohongshu notes, short-video scripts, seeded comments, native ad angles, and brand-integrated social posts.
- `xhs-ad-image-style`: analyze high-performing Xiaohongshu image-note visuals and turn reusable photography, set design, color, composition, and commercial cues into product ad image style routes and generation prompts.

When the full agent is relevant, use this sequence:

1. Run note research first to understand searchable demand, audience language, title/cover patterns, pain points, comments, saves, and conversion signals.
2. Run soft-ad content generation second to map the winning note mechanisms onto the user's product, scenario, proof, and decision moment.
3. Run ad image style generation third to convert high-performing cover/image patterns into product-specific visual routes, cover concepts, and image-generation prompts.
4. Synthesize the three outputs into a creator-ready content and visual production package.

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
   - Preserve the source method and limitations.
   - Do not invent ranked notes or metrics.

3. Generate soft-ad routes:
   - Use `soft-ad-content` after note evidence has produced a content breakdown, hook pattern, audience pain, or conversion signal.
   - Map the user's product to the observed mechanism without forcing the product into the opening hook too early.
   - If product context is incomplete, make limited assumptions and label them before drafting.

4. Generate image style routes:
   - Use `xhs-ad-image-style` after note evidence or source images provide cover/image patterns, visual hooks, or product scenes.
   - Prioritize high-engagement images when likes, saves, comments, or rank are available.
   - Convert visual mechanics into product-safe style routes, cover concepts, shot lists, and image-generation prompts.
   - If exact packaging, label text, or logo accuracy matters, recommend using a real product image as reference rather than relying on generated text.

5. Compare patterns:
   - Map note patterns to native ad roles such as solution after pain, tool in a real scene, proof object, habit upgrade, comparison object, or comment-triggered recommendation.
   - Map cover/image patterns to visual roles such as lifestyle proof, ingredient flat lay, routine scene, comparison shot, texture close-up, or clean product hero.
   - Identify repeated audience pains, identities, promises, proof types, comment triggers, save triggers, and conversion paths.
   - Separate observed evidence from inference.

6. Produce:
   - Generate outputs the creator can directly use: soft-ad angles, title formulas, cover directions, native note drafts, short-video scripts, seeded comments, product insertion lines, image style routes, ad image prompts, CTAs, and publishing checklist.
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
- Distinguish observation from inference with phrases such as "从已采集笔记看", "从软广转化角度看", or "在缺少产品细节时，这是基于笔记规律的推断".
- Keep outputs practical: every recommendation should be usable as a title, cover, hook, native note paragraph, product insertion line, seeded comment, image prompt, shot list, or testable publishing action.
