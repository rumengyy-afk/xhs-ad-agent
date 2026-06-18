# XHS Viral Ad Agent Workflow

Use this reference for full strategy requests, soft-ad packages, Xiaohongshu ad image prompts, content calendars, multi-script packages, seeded comment sets, or reusable content operations.

## Evidence Ladder

Rank evidence from strongest to weakest:

1. User-provided exports, transcripts, screenshots, metrics, or raw datasets.
2. Browser-visible platform data collected during the task.
3. User notes from their own account, campaign, or audience.
4. Pattern inference from collected notes, source images, soft-ad content structures, and visual style clusters.
5. General platform knowledge.

Never present lower-level evidence as if it were verified platform data.

## Visual Evidence Gate

Before generating Xiaohongshu ad image routes, confirm at least one of these inputs exists:

- downloaded cover images from high-ranked notes
- screenshots of high-ranked note covers or carousel images
- exported image paths from the crawl
- user-provided note images or URLs with visible images
- product images plus an explicit user request to create a product-only direction

If the first four are missing, do not claim the generated visuals are based on high-performing Xiaohongshu image styles. Ask for screenshots/images, or continue with a clearly labeled product-only creative direction.

For each visual route, cite 2-5 source notes/images when available:

| Route | Source notes/images | Shared visual pattern | What to borrow | What not to copy |
|---|---|---|---|---|

## Note-To-Soft-Ad Mapping

Translate image-text note signals into native soft-ad mechanics:

| Note signal | Soft-ad translation |
|---|---|
| High-save checklist | Native guide with the product as one step or tool, save CTA |
| Before/after cover | Transformation story with proof shown before product reveal |
| Pain-point title | First-person problem scene, product introduced after empathy |
| Comment debate | Opinion-led note plus seeded comments from different user doubts |
| Product trust proof | Ingredient/process/use-case proof woven into the author's decision |
| Lifestyle aspiration | Day-in-life scene where the product is a small habit upgrade |
| Search-heavy keyword | Searchable title, practical body outline, clear product-fit answer |

## Note-To-Ad-Image Mapping

Translate note and cover signals into product ad image style mechanics:

| Note or cover signal | Ad image translation |
|---|---|
| High-click cover text | Short overlay phrase with one clear benefit or curiosity gap |
| Ingredient/process proof | Ingredient flat lay, spoon texture shot, package plus raw materials |
| Lifestyle scene | Product embedded in breakfast desk, kitchen counter, bag, vanity, gym, or office scene |
| Comparison angle | Side-by-side setup, simple labels, product as the better-fit option |
| Searchable tutorial | Step-by-step carousel cover, numbered props, useful screenshot feel |
| Premium imported/grocery cue | Shelf, receipt, tote bag, cafe table, or international supermarket context |
| Homemade/clean cue | Natural light, raw ingredients, imperfect hand-made texture, low-studio polish |

## Synthesis Method

For each strong pattern:

1. Name the audience tension.
2. Point to the note evidence behind it.
3. Convert the tension into a native hook.
4. Choose a soft-ad role:
   - solution after pain is established
   - tool inside a real scene
   - proof supporting the author's conclusion
   - small habit or lifestyle upgrade
   - comparison object
   - comment-triggered recommendation
5. Choose a visual role:
   - lifestyle proof
   - ingredient flat lay
   - routine scene
   - comparison shot
   - texture close-up
   - product hero in a real environment
6. Create one title, one cover direction, one note outline, one product insertion line, one CTA, one seeded comment angle, and one image prompt route.

## Content Package Templates

### Topic Bank

Use this table for 10-30 idea outputs:

| Priority | Topic | Audience Pain/Desire | Evidence | Soft-Ad Hook | Product Role | CTA |
|---:|---|---|---|---|---|---|

### Visual Route Bank

Use this table for 3-6 Xiaohongshu ad image style routes:

| Route | Visual Promise | Source Evidence | Scene/Props | Product Role | Differentiator | Best For |
|---|---|---|---|---|---|---|

### Native Note

Use this format for each Xiaohongshu note:

```markdown
**标题/封面**
- 标题:
- 封面大字:
- 首图画面:

**正文**
- 开头痛点:
- 场景铺垫:
- 经验/方法:
- 产品自然插入:
- 证明/细节:
- 结尾 CTA:

**评论区**
- 置顶评论:
- 用户视角评论:
- 疑问引导评论:
```

### Short Video Soft-Ad Script

Use this format for each script:

```markdown
**标题/封面**
- 标题:
- 封面大字:
- 首帧画面:

**60 秒脚本**
- 0-3s:
- 3-12s:
- 12-30s:
- 30-45s:
- 45-55s:
- 55-60s:

**产品植入**
- 出现时机:
- 插入句:
- 证明镜头:
- 避免的硬广说法:
```

### Ad Image Prompt

Use this format for each visual route:

```markdown
**路线名称**
- 适合目标:
- 首图构图:
- 场景/道具:
- 色调/光线:
- 产品露出:
- 避免:

Prompt:
[image-generation prompt]

Negative prompt:
[things to avoid]
```

### Seven-Day Test Plan

Use this for launch planning:

| Day | Format | Angle | Variable Tested | Success Metric |
|---:|---|---|---|---|

## Review Checklist

Before finalizing, verify:

- The output names the source data and its limits.
- At least one recommendation is tied to observed note evidence.
- At least one recommendation uses `soft-ad-content` logic: pain first, product second, proof third.
- At least one recommendation uses `xhs-ad-image-style` logic: visual route, product role, scene/props, and generation prompt.
- Each visual route is visibly different in camera angle, scene, color, props, or layout; do not produce five images with the same warm tabletop look.
- Drafts have native platform language and do not sound like hard-sell ad copy.
- Titles and covers are concrete, not abstract.
- CTAs match the likely user intent: comment, save, follow, click, DM, or purchase.
- Product claims are honest, supported, and compliant with the user's constraints.
- Image prompts avoid copying creator names, watermarks, exact source layouts, private people, or protected branded compositions.
