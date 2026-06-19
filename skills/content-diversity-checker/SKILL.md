---
name: content-diversity-checker
description: Check generated social content, Xiaohongshu notes, ad copy, image prompts, carousel concepts, and campaign batches for repetitive wording, repeated hooks, same-looking visual layouts, duplicated audience angles, overused product insertions, and low creative diversity. Use before finalizing or regenerating content when the user says outputs feel similar, repetitive, samey, homogeneous, template-like, or not differentiated enough.
---

# Content Diversity Checker

Use this skill as a pre-publish and regeneration gate. It audits whether a batch of notes, image prompts, generated images, captions, or campaign ideas are meaningfully different from each other and from recent outputs.

## Core Rule

Do not treat "different text" as enough. A content set is repetitive if it reuses the same audience, hook structure, scene, product role, visual composition, color mood, proof type, CTA, or emotional promise even when the exact words differ.

For Xiaohongshu ad-agent work, run this skill after the first draft of copy and image routes, before final delivery. If the set fails the diversity gate, revise before presenting it as ready to publish.

## Diversity Dimensions

Check every generated set across these dimensions:

1. **Audience and occasion**: different reader identity, use moment, pain point, or decision context.
2. **Hook shape**: avoid repeating "not X, but Y", "N benefits", "one spoon", "breakfast upgrade", or the same curiosity gap.
3. **Claim/proof type**: vary nutrition fact, ingredient proof, texture proof, usage proof, comparison, routine, story, or comment-driven proof.
4. **Product role**: vary product as habit tool, ingredient, comparison object, texture proof, gift, pantry staple, or scene prop.
5. **Visual composition**: vary close-up, flat lay, hand/action, shelf/cafe, comparison, checklist, ingredient map, or lifestyle scene.
6. **Color and material system**: avoid repeating warm ivory + almond brown + green accents unless source evidence strongly requires it.
7. **Text density and layout**: vary big-title cover, label-led guide, real-life photo with light overlay, checklist, or minimal product scene.
8. **Sentence rhythm**: avoid repeated openings, repeated paragraph order, repeated CTA, and repeated "recently I..." first-person setup.
9. **Compliance wording**: remove repeated high-risk health claims and convert them into grounded nutrition or lifestyle language.

## Workflow

1. Collect the candidate outputs:
   - titles
   - cover text
   - body copy
   - image prompts or generated-image descriptions
   - CTAs
   - source-note patterns used
   - any recent outputs from the same brand/product
2. Run a quick mechanical scan when text is available:
   - Use `scripts/check_repetition.py` for markdown, text, or JSON exports.
   - Treat script results as signals, not a substitute for judgment.
3. Score each dimension:
   - `0`: repeated or nearly identical
   - `1`: somewhat different but same underlying template
   - `2`: meaningfully different and publishable
4. Identify repeated patterns:
   - repeated hook
   - repeated scene
   - repeated color/layout
   - repeated product insertion
   - repeated CTA
   - repeated benefit wording
5. Revise weak items before final delivery:
   - Change at least two major dimensions per weak item.
   - Prefer changing audience/occasion and visual composition before only changing adjectives.
   - Keep source-derived logic, but borrow from a different source-note pattern.

## Pass/Fail Gate

For a 3-image Xiaohongshu set:

- Pass only if the three images have clearly different visual roles: click cover, trust/proof, and use-scene.
- Pass only if at least two of these differ across all three: scene, camera angle, color system, text density, product role, and proof type.
- Fail if all three use the same product-on-table composition, same warm neutral palette, same "one spoon" message, or same breakfast-only scenario.

For a note/copy batch:

- Pass only if titles use different hook shapes.
- Pass only if openings do not repeat the same "recently I changed X" pattern.
- Pass only if product insertion timing varies naturally.
- Fail if every note ends with the same save/comment CTA or repeats the same benefit stack.

## Revision Moves

When a set feels samey, revise with one or more of these moves:

- Change the audience: fitness breakfast, office snack, mother/child pantry, low-sugar preference, premium gift, ingredient-conscious shopper.
- Change the occasion: breakfast, afternoon snack, travel bag, office drawer, weekend brunch, post-workout food prep.
- Change the proof: ingredient flat lay, texture spoon pull, comparison table, recipe step, pantry shelf, user doubt Q&A.
- Change the format: myth correction, shopping checklist, mistake avoidance, recipe mini-guide, comment-answer note, ingredient explainer.
- Change the visual system: top-down ingredient grid, hand-held product, close macro texture, cafe table, kitchen action, supermarket shelf, simple illustrated cover.
- Change the emotional promise: practical, premium, comforting, efficient, clean-ingredient, gifting, discovery, habit-building.

## Output Format

Use this structure when reporting:

```markdown
## Diversity Verdict
- Overall: Pass / Revise
- Main repetition risk:
- What is already differentiated:

## Repetition Findings
| Item | Repeated pattern | Why it feels samey | Fix |
|---|---|---|---|

## Diversity Score
| Dimension | Score | Notes |
|---|---:|---|

## Revised Directions
| Item | New hook | New visual/scene | New product role |
|---|---|---|---|
```

## Quality Rules

- Be strict. If the user already complained about repetitive output, default to `Revise` unless there is clear diversity.
- Do not solve repetition by adding random novelty. Every change must still fit the product, source-note evidence, and platform.
- Do not make health, beauty, or nutrition claims stronger just to create variety.
- Do not replace source-derived Xiaohongshu style with generic luxury advertising.
- Keep final recommendations practical enough to become new prompts, copy, or image directions immediately.
