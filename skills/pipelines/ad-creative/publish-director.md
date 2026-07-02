# Publish Director — Ad-Creative Pipeline

## When To Use

Package every variant for its ad platform with copy, CTA links, and A/B-attributable naming. The publish log is the campaign's source of truth for what ran where.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `render_report`, `final_review`, `brief` | Variants + objective + destination |

## Process

### 1. Per-platform packages
For each declared platform (Meta / TikTok / YouTube / etc.): the correct aspect variant, platform file spec verified (container, size, duration limits), primary text / headline / description fields from the script's copy, and the CTA destination URL with tracking parameters if supplied.

### 2. A/B-attributable naming
Name every file/entry to encode the test dimensions: `{product}_{angle}_{hook-id}_{aspect}_{duration}` (e.g. `invoiceapp_painfirst_h1_9x16_20s`). The `ab_alternates` recorded at script are the next iteration — list them in the publish log as the pending test plan.

### 3. Compliance notes
Record per-platform policy checks relevant to the creative (e.g. claims substantiation for numbers used as proof, before/after restrictions). Flag anything the reviewer should clear before spend.

### 4. Localization handoff (if declared)
Locale variants → `localization-dub` handoff manifest (video + script + caption files).

### 5. Export + log
Export directory: variants + `metadata.json` per platform (copy, CTA, naming, specs) + pending A/B plan. `publish_log` records paths, spec-check results, compliance notes, handoffs.

### Quality Gate
- [ ] Every declared variant packaged with platform-spec verification.
- [ ] Naming encodes angle/hook/aspect/duration for attribution.
- [ ] Ad copy fields + CTA destination present per platform.
- [ ] Compliance notes recorded; A/B alternates listed as the next test.

## Common Pitfalls

- Generic filenames that make performance data unattributable to the creative angle.
- Copy fields left to the platform's ad manager instead of shipped with the package.
- Shipping proof numbers with no substantiation note for policy review.
