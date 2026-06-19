---
name: xhs-ad-image-style
description: Analyze high-performing Xiaohongshu/小红书 image-note visuals and turn their reusable photography, set design, color, composition, content, and commercial cues into image-generation prompts for product advertising. Use when the user provides crawled Xiaohongshu note images, screenshots, URLs, exports, or folders of images and asks to summarize visual patterns, imitate high-liked image styles, create similar product ad images, write image prompts, or adapt a product into 小红书风格/种草广告图/软广封面.
---

# XHS Ad Image Style

## Overview

Use this skill to convert high-liked Xiaohongshu image posts into a reusable visual recipe, then generate product-safe ad image prompts that borrow the style mechanics without copying any specific creator, brand, person, watermark, or protected composition too closely.

## Core Rule

Do not default to a generic Xiaohongshu lifestyle aesthetic. This skill must start from observed source visuals: crawled cover images, screenshots, exported image paths, or user-provided note images. If no source visuals are available, state that the visual route cannot be claimed as high-performing-source-derived and ask for images, or label the result as a product-only creative direction.

When used inside `xhs-viral-ad-agent`, the default deliverable is **3 usable images**, not a large concept board:

1. **Click cover**: a first image optimized for scroll-stop and search-result click, derived from the highest-like cover patterns.
2. **Trust/proof image**: a second image that makes the product believable through ingredient, comparison, process, texture, package, or proof cues.
3. **Use-scene image**: a third image that shows the product in a native lifestyle, recipe, breakfast, snack, desk, kitchen, or routine context.

Every generated/promoted image must be traceable to source visual evidence. If the source data has titles and likes but no cover images/screenshots, do not generate images. Ask for top-note screenshots or browser/export data with cover images.

## Workflow

1. Collect inputs: product name/category, target audience, selling points, required platform ratio, brand constraints, and the Xiaohongshu images or exported image paths.
2. Inspect the strongest images first. If engagement data is available, prioritize by likes, saves, comments, or a weighted score. If engagement data is absent, sample the clearest and most visually representative images. If no images are available, stop and request screenshots/images unless the user explicitly accepts a product-only direction.
   - When images come from `xhs-viral-note-crawler`, inspect representative downloaded cover files from `covers/` or screenshots before generating prompts. Do not treat URLs, titles, or like counts alone as visual evidence.
3. Analyze images using `references/style-analysis-matrix.md`. Cover camera angle, distance, framing, scene, props, lighting, color, texture, subject placement, text overlay, human presence, product role, and emotional hook.
4. Cluster images into 3 source-backed output routes by default: click cover, trust/proof, and use-scene. Name each route by the visual promise, such as "high-contrast nutrition correction cover", "clean ingredient proof flat lay", or "morning toast routine scene".
   - Make the routes meaningfully different. Vary camera angle, scene, prop system, color palette, human presence, and product role.
   - Cite which source images or note ranks informed each route.
5. Extract the visual formula for each route:
   - Shot type and camera position
   - Product placement and scale
   - Background and props
   - Color palette and lighting
   - Human/action details
   - Xiaohongshu-native content cues
   - What to avoid copying
6. Convert formulas into generation prompts tailored to the user's product. Keep prompts concrete, visual, and production-ready.
7. If the user asks to generate images, generate or specify exactly 3 images, one per route. Do not produce repeated card layouts or generic black/gold templates unless the observed source visuals actually support that direction.
8. Provide selection guidance: which route is best for clicks, trust, premium feel, affordability, before/after proof, or lifestyle aspiration.

## Usable Image Quality Bar

Before finalizing, reject or revise images that look like:

- presentation slides, report cards, dashboards, or internal strategy summaries
- generic luxury brand posters unrelated to the source Xiaohongshu covers
- product photos pasted into a plain white rectangle without source-derived scene context
- fake product packaging, inaccurate labels, invented logo text, or distorted jars
- repeated designs where only the text changes
- three images with the same composition, color palette, and text-card structure
- claims or labels that read as medical promises, such as "降血糖", "降胆固醇", "保护心脏", "治疗", or guaranteed weight loss

Prefer images with:

- real product image reference for package accuracy
- source-derived composition and mobile-readable text
- visible differences across the three required routes: one click cover, one trust/proof image, and one use-scene image
- food texture, use scene, hand/action, ingredient, package, or comparison proof
- one clear message per image
- Xiaohongshu-native crop and density, usually 3:4 or 4:5

## Output Format

Prefer this structure unless the user asks for something else:

```markdown
## 高赞图片视觉规律
| 维度 | 观察 | 可复用做法 |
| --- | --- | --- |

## 视觉证据
| 来源/排名 | 图片或截图 | 可见风格信号 |
| --- | --- | --- |

## 风格路线
### 路线 1：名称
- 来源依据：
- 适合目标：
- 拍摄角度：
- 布景：
- 色调：
- 内容元素：
- 产品植入：
- 避免：

## 广告图提示词
### 路线 1 Prompt
[image-generation prompt]

Negative prompt:
[things to avoid]

## 推荐
[which route to use first and why]
```

## Prompt Rules

- Write prompts in the language most useful for the target generator. Use English for general image generation unless the user requests Chinese.
- Every prompt must include a source-style anchor, such as "borrow the observed pattern of [route/source], but do not copy the exact layout."
- Specify product category, package shape, visible label handling, composition, lens/angle, lighting, materials, background, props, color palette, mood, and aspect ratio.
- Preserve the user's real brand constraints. If exact text, logo, or packaging must be accurate, recommend using an existing product image as a reference rather than relying on text generation alone.
- Use Xiaohongshu-native visual language: casual but polished, useful-life scene, believable props, soft natural light, editorial crop, phone-camera plausibility, and clear product benefit.
- Avoid direct imitation of a specific post. Do not request watermarks, creator names, exact layouts, recognizable private people, or copied branded packaging from source images.
- For advertorial images, keep the product visibly central enough to sell, but embed it in an authentic use moment rather than a hard-sell studio packshot unless the user asks for studio ads.

## Image Handling

- When images are local files, inspect representative images directly before summarizing.
- When images come from a crawl/export, prefer any available metadata: keyword, note title, likes, saves, comments, author category, publish date, and image order.
- If many images are available, sample across top performers and visual diversity instead of only near-duplicates.
- If image quality is low, state the uncertainty and focus on robust cues such as framing, palette, subject, and prop pattern.

## Deliverables

Create whichever deliverables match the user's request:

- A concise visual insight summary from high-performing images
- A route table of reusable Xiaohongshu ad styles
- Product-specific image-generation prompts, defaulting to 3 prompts/images when used by `xhs-viral-ad-agent`
- Negative prompts and production constraints
- A shot list for a real photoshoot
- A batch prompt set for multiple SKUs, audiences, seasons, or selling points
