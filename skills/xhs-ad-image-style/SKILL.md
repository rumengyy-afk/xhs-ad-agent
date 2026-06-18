---
name: xhs-ad-image-style
description: Analyze high-performing Xiaohongshu/小红书 image-note visuals and turn their reusable photography, set design, color, composition, content, and commercial cues into image-generation prompts for product advertising. Use when the user provides crawled Xiaohongshu note images, screenshots, URLs, exports, or folders of images and asks to summarize visual patterns, imitate high-liked image styles, create similar product ad images, write image prompts, or adapt a product into 小红书风格/种草广告图/软广封面.
---

# XHS Ad Image Style

## Overview

Use this skill to convert high-liked Xiaohongshu image posts into a reusable visual recipe, then generate product-safe ad image prompts that borrow the style mechanics without copying any specific creator, brand, person, watermark, or protected composition too closely.

## Workflow

1. Collect inputs: product name/category, target audience, selling points, required platform ratio, brand constraints, and the Xiaohongshu images or exported image paths.
2. Inspect the strongest images first. If engagement data is available, prioritize by likes, saves, comments, or a weighted score. If engagement data is absent, sample the clearest and most visually representative images.
3. Analyze images using `references/style-analysis-matrix.md`. Cover camera angle, distance, framing, scene, props, lighting, color, texture, subject placement, text overlay, human presence, product role, and emotional hook.
4. Cluster images into 3-6 style routes. Name each route by the visual promise, such as "desk-side unboxing proof", "clean ingredient flat lay", or "morning routine mirror shot".
5. Extract the visual formula for each route:
   - Shot type and camera position
   - Product placement and scale
   - Background and props
   - Color palette and lighting
   - Human/action details
   - Xiaohongshu-native content cues
   - What to avoid copying
6. Convert formulas into generation prompts tailored to the user's product. Keep prompts concrete, visual, and production-ready.
7. Provide selection guidance: which route is best for clicks, trust, premium feel, affordability, before/after proof, or lifestyle aspiration.

## Output Format

Prefer this structure unless the user asks for something else:

```markdown
## 高赞图片视觉规律
| 维度 | 观察 | 可复用做法 |
| --- | --- | --- |

## 风格路线
### 路线 1：名称
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
- Product-specific image-generation prompts
- Negative prompts and production constraints
- A shot list for a real photoshoot
- A batch prompt set for multiple SKUs, audiences, seasons, or selling points
