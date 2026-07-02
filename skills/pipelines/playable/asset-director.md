# Asset Director — Playable Pipeline

## When To Use

Fourth stage. Resolve the **brand assets** that theme the playable — accent palette and app icon — grounded in the real product. Deliverable: the `asset_manifest` artifact. This stage owns the **`no_external_assets`** + **size-budget** half of the `playable_compliance` gate: everything must end up **inlineable** so the build is one self-contained file.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior | `state.artifacts["design"]["scene_plan"]` | theme_slots to fill |
| Tool | `site_harvester` | Grounds palette + icon from the live site (Playwright) |
| Tool | `image_selector` (optional) | Generates an icon/background via `lib/scoring.py` |
| Scoring | `lib/scoring.py` | Route any generated asset (no hardcoded provider) |

## Brand Grounding (preferred)

If the brief carries a `website_url`, harvest the real brand so the playable looks like the product, not a template:

- **Accent palette** — read `theme-color`; if absent, derive a vivid mid-tone dominant color from a phone-viewport screenshot. Compute a lighter `accent_soft` for gradients.
- **App icon** — fetch `apple-touch-icon` / `icon`. **Embed it as a base64 data URI**, downscaling to ≤192px / ≤~200 KB so it never blows the size budget. (The content-factory adapter's `icon_data_uri_from_path` does this.)
- Title/description become copy hints already used by the script stage.

This is best-effort: if Playwright or a browser is unavailable, record a clean **unbranded fallback** palette and proceed — the playable still ships.

## Generated Assets (optional)

If no usable icon/palette exists and you want a branded mark, generate one via `image_selector` → `lib/scoring.py`. Record `selected_provider` + `provider_score` (scoring audit trail). Keep it small and **inline it** as a data URI — a generated asset that survives as an external URL fails the gate.

## The Inlining Rule (gate-critical)

The build MUST be a single self-contained `index.html`. Therefore every asset this stage resolves must be **inlineable**:
- icons/backgrounds → base64 data URIs,
- colors → hex strings,
- fonts → system font stack (no web-font fetch).

Do not pass a `https://…` asset URL forward expecting the build to fetch it at runtime — that breaks offline playback and fails `no_external_assets`.

## Output — `asset_manifest` artifact

Must include:
- `accent`, `accent_soft`, `bg` (hex)
- `icon_data_uri` (or empty → brand-bar uses a gradient tile)
- `brand_grounded` (bool) + `website_theme_color` (or null)
- `screenshots_captured` (count, informational)
- For any generated asset: `selected_provider` + `provider_score`

## Success Criteria
- Schema-valid `asset_manifest`.
- Brand palette + (optional) icon resolved, or a clean unbranded fallback recorded.
- Every asset is inlineable; no runtime external fetch survives.
- Generated assets record the scoring audit trail.

## Common Pitfalls
- Passing a remote icon URL forward instead of embedding it (fails `no_external_assets`).
- Embedding a full-resolution icon and blowing the 2 MB budget — downscale first.
- Hardcoding an image provider instead of routing via `image_selector` → scoring.
- Treating a failed harvest as fatal — degrade to the unbranded fallback and continue.
