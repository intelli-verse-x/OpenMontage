#!/usr/bin/env python3
"""Brand-swappable luxury product reel engine (OpenMontage).

A self-contained, parametrized generalization of the Maison reel:
FLUX reference stills -> Seedance 2.0 reference-to-video clips ->
ElevenLabs VO + music -> FFmpeg compose (grade, cross-dissolves, Didot
titling, swelling-piano-under-VO) -> 9:16 hero + variants -> optional S3.

Runs from the OpenMontage repo root so `tools.tool_registry` resolves to
OpenMontage's registry. Driven by a JSON spec (see DEFAULT_SPEC / build_spec).

CLI:
    python pipelines_engine/luxury_reel.py --spec spec.json --out report.json
    python pipelines_engine/luxury_reel.py --spec spec.json --phase refs
    python pipelines_engine/luxury_reel.py --print-default-spec      # scaffold
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

# OpenMontage repo root on sys.path (engine lives at <root>/pipelines_engine/)
OM_ROOT = Path(__file__).resolve().parents[1]
if str(OM_ROOT) not in sys.path:
    sys.path.insert(0, str(OM_ROOT))


# ───────────────────────── spec / defaults ──────────────────────────────────

def default_spec() -> Dict[str, Any]:
    """A complete jewelry-reel spec. Swap `brand`, `product`, `palette`,
    `voice_id`, `vo`, `taglines` to retarget another luxury brand."""
    return {
        "brand": "Maison",
        "product": "diamond solitaire engagement ring",
        "product_short": "ring",
        "voice_id": "XB0fDUnXU5powFXDhCwa",  # ElevenLabs warm female (Charlotte)
        "voice_provider": "elevenlabs",
        "aspect": "9:16",
        "fps": 30,
        "also_169": True,
        "palette": {"gold": "E7CFA0", "soft": "F6F1E9", "black": "0a0908"},
        "palette_words": "champagne gold, warm beige and soft white on deep black",
        "music_prompt": (
            "Luxury cinematic solo piano, very soft and intimate, slow tempo, tender and "
            "emotional, warm reverb, sparse notes that gently build and swell toward the middle "
            "then resolve softly; no drums, no vocals; elegant fine-jewelry advertisement underscore."
        ),
        "music_duration": 40,
        "wordmark_tagline": "Crafted only for you",
        "variants": [
            {"id": "endA", "end_line": "Your story. Your ring."},
            {"id": "endB", "end_line": "Created only for you."},
        ],
        "vo": [
            {"key": "vo_b1", "at": 0.8, "text": "Some moments deserve more than a memory."},
            {"key": "vo_b2", "at": 5.3, "text": "A ring is not just a piece of jewelry. It carries a promise, a celebration, a story that belongs only to you."},
            {"key": "vo_b3", "at": 12.8, "text": "At {brand}, every {product_short} is thoughtfully crafted around your vision, your emotions, and your unforgettable moments."},
            {"key": "vo_b5", "at": 31.0, "text": "Because the most beautiful luxury is something created just for you."},
        ],
        "refs": {
            "ref_hand_box": {
                "prompt": (
                    "An elegant young woman's hand with soft natural manicured nails, gently opening a "
                    "champagne-gold ring box lined with warm beige velvet, a single {product} inside "
                    "catching the light. Extreme close-up, shallow depth of field, warm candlelight and "
                    "soft golden key light, deep black background, {palette_words} palette, photorealistic "
                    "skin texture, fine jewelry product photography, Hasselblad medium format, 85mm, f/2.8, "
                    "gentle film grain, intimate luxury mood."
                ),
                "width": 768, "height": 1344,
            },
            "ref_product": {
                "prompt": (
                    "A single {product} resting on champagne-colored silk, macro shot, refracting warm "
                    "light into delicate sparkle, soft studio key light from upper left with gentle rim "
                    "light, deep black background, {palette_words} palette, ultra sharp focus with creamy "
                    "bokeh, high-end fine jewelry catalog photography, 100mm macro, f/4, subtle film grain."
                ),
                "width": 768, "height": 1344,
            },
            "ref_woman": {
                "prompt": (
                    "A natural, radiant young woman in her late twenties with soft glowing skin and minimal "
                    "makeup, loose hair, wearing a soft cream silk blouse, standing near a window in warm "
                    "golden-hour light, a subtle serene smile, looking gently at her own hand off-frame. "
                    "Intimate editorial portrait, shallow depth of field, warm beige and soft white palette, "
                    "soft diffused window light with gentle rim, photorealistic, 85mm, f/1.8, fine film grain, "
                    "luxury campaign mood."
                ),
                "width": 768, "height": 1344,
            },
        },
        "common_tail": (
            " Cinematic luxury commercial, {palette_words} palette, deep black background, warm "
            "candlelight and soft golden studio light, shallow depth of field, slow deliberate camera, "
            "photorealistic skin and metal, fine film grain, 35mm, no text, no logos, elegant and slow."
        ),
        # shots: (key, seconds, refs, prompt) -> trimmed to `seg_seconds` in compose
        "shots": [
            {"key": "clip1_hook", "duration": "5", "seg": 5.0, "refs": ["ref_hand_box"],
             "prompt": "Single continuous shot, slow dolly-in, no cuts, no zoom. The frame begins in near darkness; a soft warm light blooms in. Extreme close-up of an elegant woman's hand gently opening a champagne-gold ring box, revealing a {product} that catches the light."},
            {"key": "clip2_meaning", "duration": "7", "seg": 7.0, "refs": ["ref_woman", "ref_product"],
             "prompt": "Single continuous shot, very slow push-in, no cuts. A radiant young woman stands near a softly lit window in warm golden-hour light, raising her hand to look at the {product} on her finger; light reflects across it; a subtle, serene smile forms."},
            {"key": "clip3_custom", "duration": "10", "seg": 9.0, "refs": ["ref_product"],
             "prompt": "Multi-shot artisan montage, four elegant slow shots, warm intimate lighting. Shot 1 (extreme close-up, slow pan): a hand sketches a design with a fine pencil on cream paper. Shot 2 (close-up, static): a jeweller's hands work delicately under a warm desk lamp. Shot 3 (macro, slow push-in): tweezers place a small stone into a setting. Shot 4 (macro, slow rotate): the {product_short} is polished on a soft wheel, then revealed gleaming."},
            {"key": "clip4_rotate", "duration": "6", "seg": 6.0, "refs": ["ref_product"],
             "prompt": "Single continuous shot, slow 180-degree orbit, no cuts. The finished {product} rotates slowly on champagne silk; a soft highlight travels across it."},
            {"key": "clip5_macro", "duration": "5", "seg": 5.0, "refs": ["ref_product"],
             "prompt": "Single continuous shot, extreme macro, very slow push-in, no cuts. The {product} fills the frame; warm light refracts into delicate moving sparkle against deep black."},
            {"key": "clip6_close", "duration": "7", "seg": 7.0, "refs": ["ref_woman", "ref_hand_box"],
             "prompt": "Single continuous shot, slow gentle move, no cuts. The same radiant young woman, now wearing the {product}, looks down at her hand and then up with a soft, quietly joyful smile in warm light."},
        ],
        "publish": None,   # or {"bucket": "...", "region": "us-east-1", "prefix": "showcase/<brand>"}
        "dry_run": False,
    }


def _fmt(text: str, spec: Dict[str, Any]) -> str:
    return text.format(
        brand=spec["brand"], product=spec["product"],
        product_short=spec.get("product_short", "piece"),
        palette_words=spec.get("palette_words", ""),
    )


# ───────────────────────── tool plumbing ────────────────────────────────────

def _registry():
    from tools.tool_registry import registry
    registry.discover()
    return registry


def _run_tool(reg, name, params, label):
    out = params.get("output_path")
    if out and Path(out).exists():
        print(f"[skip] {label} -> {out}", flush=True)
        return {"success": True, "skipped": True, "output_path": out}
    t = reg._tools.get(name)
    if not t:
        raise RuntimeError(f"tool '{name}' not in OpenMontage registry")
    print(f"[run ] {label} via {name}", flush=True)
    res = t.execute(params)
    ok = getattr(res, "success", False)
    if not ok:
        raise RuntimeError(f"{label} failed: {getattr(res, 'error', 'unknown')}")
    return {"success": True, "data": getattr(res, "data", None), "output_path": out}


# ───────────────────────── phases ───────────────────────────────────────────

def phase_refs(spec, dirs, reg):
    for key, r in spec["refs"].items():
        _run_tool(reg, "image_selector", {
            "prompt": _fmt(r["prompt"], spec),
            "negative_prompt": "text, watermark, logo, cartoon, plastic, oversaturated, harsh white background",
            "width": r.get("width", 768), "height": r.get("height", 1344),
            "preferred_provider": spec.get("image_provider", "flux"),
            "seed": r.get("seed", 7),
            "output_path": str(dirs["img"] / f"{key}.png"),
        }, f"FLUX {key}")


def phase_clips(spec, dirs, reg):
    tail = _fmt(spec["common_tail"], spec)
    for s in spec["shots"]:
        refs = [str(dirs["img"] / f"{r}.png") for r in s.get("refs", [])]
        refs = [p for p in refs if Path(p).exists()]
        params = {
            "prompt": _fmt(s["prompt"], spec) + tail,
            "preferred_provider": "seedance",
            "operation": "reference_to_video" if refs else "text_to_video",
            "aspect_ratio": spec.get("aspect", "9:16"),
            "duration": str(s["duration"]),
            "resolution": spec.get("resolution", "720p"),
            "output_path": str(dirs["vid"] / f"{s['key']}.mp4"),
        }
        if refs:
            params["reference_image_paths"] = refs
        _run_tool(reg, "video_selector", params, f"Seedance {s['key']} ({s['duration']}s)")


def phase_audio(spec, dirs, reg):
    for v in spec["vo"]:
        _run_tool(reg, "tts_selector", {
            "text": _fmt(v["text"], spec),
            "preferred_provider": spec.get("voice_provider", "elevenlabs"),
            "voice_id": spec["voice_id"],
            "model_id": spec.get("voice_model", "eleven_multilingual_v2"),
            "stability": 0.45, "similarity_boost": 0.8, "style": 0.25,
            "output_format": "mp3_44100_128",
            "output_path": str(dirs["aud"] / f"{v['key']}.mp3"),
        }, f"VO {v['key']}")
    _run_tool(reg, "music_gen", {
        "prompt": spec["music_prompt"],
        "duration_seconds": spec.get("music_duration", 40),
        "output_path": str(dirs["mus"] / "score.mp3"),
    }, "Music score")


# ───────────────────────── compose (ffmpeg + PIL) ───────────────────────────

def _sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + r.stderr[-2000:])
    return r


def _dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def _font(size, index=0):
    from PIL import ImageFont
    for p in ("/System/Library/Fonts/Supplemental/Didot.ttc",
              "/System/Library/Fonts/Supplemental/Georgia.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"):
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size, index=index)
            except Exception:
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    continue
    from PIL import ImageFont as _IF
    return _IF.load_default()


def _hexc(c):
    c = c.replace("0x", "").replace("#", "")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))


def _centered(d, text, font, y, fill, W, ls=0, shadow=None):
    w = sum(d.textlength(ch, font=font) for ch in text) + ls * max(0, len(text) - 1)
    x = W / 2 - w / 2
    for dx, dy, col in ([(shadow[0], shadow[1], shadow[2])] if shadow else []) + [(0, 0, fill)]:
        cur = x + dx
        for ch in text:
            d.text((cur, y + dy), ch, font=font, fill=col)
            cur += d.textlength(ch, font=font) + ls


def compose(spec, dirs) -> List[Dict[str, Any]]:
    from PIL import Image, ImageDraw
    W, H = (720, 1280) if spec.get("aspect", "9:16") == "9:16" else (1280, 720)
    fps = spec.get("fps", 30)
    XF = 0.6
    gold = _hexc(spec["palette"]["gold"])
    soft = _hexc(spec["palette"]["soft"])
    work = dirs["work"]; work.mkdir(parents=True, exist_ok=True)

    # 1) graded trimmed segments
    segs = []
    for i, s in enumerate(spec["shots"]):
        src = dirs["vid"] / f"{s['key']}.mp4"
        out = work / f"seg{i+1}.mp4"
        vf = (
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p,"
            "eq=contrast=1.06:saturation=1.05:gamma=1.02:gamma_r=1.04:gamma_b=0.97,"
            "colorbalance=rs=0.03:gs=0.01:bs=-0.05:rm=0.04:bm=-0.04:rh=0.03:bh=-0.03,vignette=PI/5"
        )
        _sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-t", str(s["seg"]),
             "-vf", vf, "-an", "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-crf", "18", "-preset", "medium", str(out)])
        segs.append((out, float(s["seg"])))

    # 2) xfade chain
    body = work / "body.mp4"
    inputs = []
    for sp, _ in segs:
        inputs += ["-i", str(sp)]
    fc, prev, cum = [], "0:v", segs[0][1]
    for i in range(1, len(segs)):
        off = cum - XF
        fc.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]")
        prev = f"x{i}"; cum = cum - XF + segs[i][1]
    _sh(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc),
         "-map", f"[{prev}]", "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "18", "-preset", "medium", str(body)])
    total = _dur(body)

    # 3) audio (built once; shared across end-line variants)
    audio = work / "mix.m4a"
    ain = ["-i", str(dirs["mus"] / "score.mp3")]
    for v in spec["vo"]:
        ain += ["-i", str(dirs["aud"] / f"{v['key']}.mp3")]
    af, vl = [], []
    for idx, v in enumerate(spec["vo"], start=1):
        ms = int(float(v["at"]) * 1000)
        af.append(f"[{idx}:a]adelay={ms}|{ms},volume=1.0[v{idx}]")
        vl.append(f"[v{idx}]")
    af.append("".join(vl) + f"amix=inputs={len(spec['vo'])}:normalize=0[vo]")
    af.append("[0:a]volume=eval=frame:volume='if(between(t,20,31),0.55,0.30)',"
              f"afade=t=in:st=0:d=1.5,afade=t=out:st={total+3.2-2.2:.2f}:d=2.0[mus]")
    af.append("[mus][vo]sidechaincompress=threshold=0.04:ratio=8:attack=15:release=350[dk]")
    af.append("[dk][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[mix]")
    full = total + 3.2  # body + endcard
    _sh(["ffmpeg", "-y", "-loglevel", "error", *ain, "-filter_complex", ";".join(af),
         "-map", "[mix]", "-t", f"{full:.2f}", "-c:a", "aac", "-b:a", "192k", str(audio)])

    # 4) end card image
    cpng = work / "endcard.png"
    img = Image.new("RGBA", (W, H), _hexc(spec["palette"]["black"]) + (255,))
    d = ImageDraw.Draw(img)
    _centered(d, spec["brand"].upper(), _font(92), int(H * 0.40), soft + (255,), W, ls=16)
    _centered(d, spec.get("wordmark_tagline", ""), _font(30), int(H * 0.40) + 150, gold + (255,), W, ls=4)
    img.save(cpng)
    card = work / "endcard.mp4"
    cd = 3.2
    _sh(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", str(cd), "-i", str(cpng),
         "-vf", f"fade=t=in:st=0:d=0.6,fade=t=out:st={cd-0.7:.2f}:d=0.7,format=yuv420p",
         "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
         "-preset", "medium", str(card)])

    # 5) per-variant: title overlay -> dissolve to card -> mux audio
    REND = dirs["rend"]; REND.mkdir(parents=True, exist_ok=True)
    asp_tag = "9x16" if spec.get("aspect") == "9:16" else "16x9"
    outputs = []
    t_in = total - 5.0
    for var in spec["variants"]:
        tpng = work / f"title_{var['id']}.png"
        ti = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(ti)
        _centered(dd, var["end_line"], _font(46), int(H * 0.72), gold + (255,), W, ls=2,
                  shadow=(0, 2, (0, 0, 0, 150)))
        ti.save(tpng)
        titled = work / f"titled_{var['id']}.mp4"
        _sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(body),
             "-loop", "1", "-t", f"{total:.2f}", "-i", str(tpng),
             "-filter_complex",
             f"[1:v]format=rgba,fade=t=in:st={t_in:.2f}:d=1.3:alpha=1[ov];[0:v][ov]overlay=0:0[v]",
             "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
             "-preset", "medium", "-an", str(titled)])
        vfull = work / f"video_{var['id']}.mp4"
        off = _dur(titled) - XF
        _sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(titled), "-i", str(card),
             "-filter_complex",
             f"[0:v][1:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v]",
             "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
             "-preset", "medium", "-an", str(vfull)])
        final = REND / f"{spec['brand'].lower()}_reel_{asp_tag}_{var['id']}.mp4"
        _sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vfull), "-i", str(audio),
             "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-shortest", str(final)])
        outputs.append({"id": var["id"], "aspect": spec.get("aspect"),
                        "end_line": var["end_line"], "file": str(final),
                        "duration": round(_dur(final), 2)})

    # 6) optional 16:9 landscape derived from the hero (first variant)
    if spec.get("also_169") and spec.get("aspect") == "9:16":
        hero = Path(outputs[0]["file"])
        wide = REND / f"{spec['brand'].lower()}_reel_16x9.mp4"
        _sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(hero), "-filter_complex",
             "split=2[bg][fg];[bg]scale=1280:720:force_original_aspect_ratio=increase,"
             "crop=1280:720,boxblur=28:2,eq=brightness=-0.10[bgb];[fg]scale=-1:720[fgs];"
             "[bgb][fgs]overlay=(W-w)/2:0[v]",
             "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", str(wide)])
        outputs.append({"id": "wide", "aspect": "16:9", "file": str(wide),
                        "duration": round(_dur(wide), 2)})
    return outputs


# ───────────────────────── showcase + publish ───────────────────────────────

def build_showcase(spec, dirs, outputs) -> Path:
    import html
    show = dirs["show"]; show.mkdir(parents=True, exist_ok=True)
    import shutil
    for o in outputs:
        shutil.copy2(o["file"], show / Path(o["file"]).name)
    hero = next((o for o in outputs if o["id"] == "endA"), outputs[0])
    cards = "".join(
        f'<div><div class="frame"><span class="badge">{html.escape(o.get("aspect",""))} · {o["id"]}</span>'
        f'<video src="{Path(o["file"]).name}" controls muted loop playsinline></video></div>'
        f'<div class="label"><div class="t">{html.escape(o.get("end_line",o["id"]))}</div></div></div>'
        for o in outputs if o["id"] != hero["id"]
    )
    brand = html.escape(spec["brand"])
    tagline = html.escape(hero.get("end_line", ""))
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{brand} — {tagline}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,400&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<style>
:root{{--black:#0a0908;--gold:#d8b981;--soft:#f6f1e9;--line:rgba(216,185,129,.22)}}
*{{margin:0;box-sizing:border-box}}body{{background:radial-gradient(120% 80% at 50% -10%,#1a1512,var(--black) 55%);color:var(--soft);font-family:'Jost',sans-serif;font-weight:300;text-align:center}}
header{{padding:72px 24px 30px}}.word{{font-family:'Cormorant Garamond',serif;font-weight:500;letter-spacing:.42em;font-size:clamp(40px,9vw,84px);padding-left:.42em}}
.tag{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(18px,3.6vw,26px);color:var(--gold)}}
.rule{{width:70px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:28px auto}}
.frame{{position:relative;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6);background:#000}}
video{{display:block;width:100%;height:auto;background:#000}}
.hero .frame{{width:min(360px,86vw);margin:0 auto}}
.badge{{position:absolute;top:12px;left:12px;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:#0a0908;background:var(--gold);padding:5px 10px;border-radius:2px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:40px 28px;max-width:1100px;margin:30px auto;padding:0 24px}}
.label .t{{font-family:'Cormorant Garamond',serif;font-size:20px;margin-top:12px}}
footer{{padding:40px;font-size:11px;letter-spacing:.25em;text-transform:uppercase;color:#7a7167}}
</style></head><body>
<header><div class="word">{brand}</div><div class="tag">{tagline}</div><div class="rule"></div></header>
<div class="hero"><div class="frame"><span class="badge">Hero</span>
<video src="{Path(hero['file']).name}" controls autoplay muted loop playsinline></video></div></div>
<div class="grid">{cards}</div>
<footer>{brand} · {html.escape(spec.get('wordmark_tagline',''))}</footer>
</body></html>"""
    idx = show / "index.html"
    idx.write_text(page, encoding="utf-8")
    return show


def publish(spec, show_dir) -> Optional[Dict[str, Any]]:
    pub = spec.get("publish")
    if not pub:
        return None
    import importlib.util
    cf_pub = pub.get("cf_publish_module",
                     "/Users/devashishbadlani/dev/content-factory/pipelines/games/v5/publish_s3.py")
    if not Path(cf_pub).exists():
        print(f"[publish] helper not found at {cf_pub}; skipping")
        return None
    spec_m = importlib.util.spec_from_file_location("cf_publish_s3", cf_pub)
    mod = importlib.util.module_from_spec(spec_m)
    sys.modules["cf_publish_s3"] = mod
    spec_m.loader.exec_module(mod)
    res = mod.publish_landing(
        landing_dir=show_dir, extras={"publish": {"prefix": pub.get("prefix", "")}},
        brand_url=pub.get("public_url", "https://brand.local"), publish=True,
        cli_bucket=pub["bucket"], region=pub.get("region", "us-east-1"),
        out_dir=show_dir.parent / "artifacts",
    )
    return res.as_dict()


# ───────────────────────── orchestration ────────────────────────────────────

def _dirs(out_dir: Path) -> Dict[str, Path]:
    d = {"root": out_dir, "img": out_dir / "assets/images", "vid": out_dir / "assets/video",
         "aud": out_dir / "assets/audio", "mus": out_dir / "assets/music",
         "work": out_dir / "assets/work", "rend": out_dir / "renders",
         "show": out_dir / "showcase", "art": out_dir / "artifacts"}
    for p in d.values():
        p.mkdir(parents=True, exist_ok=True)
    return d


def run(spec: Dict[str, Any], out_dir: str, phase: str = "all") -> Dict[str, Any]:
    out = Path(out_dir).resolve()
    dirs = _dirs(out)
    (dirs["art"] / "spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")

    if spec.get("dry_run"):
        return {"status": "dry_run", "brand": spec["brand"], "out_dir": str(out),
                "planned_shots": [s["key"] for s in spec["shots"]],
                "planned_variants": [v["id"] for v in spec["variants"]],
                "publish_target": spec.get("publish")}

    reg = _registry()
    if phase in ("all", "refs"):
        phase_refs(spec, dirs, reg)
    if phase in ("all", "clips"):
        phase_clips(spec, dirs, reg)
    if phase in ("all", "audio"):
        phase_audio(spec, dirs, reg)
    report: Dict[str, Any] = {"status": "ok", "brand": spec["brand"], "out_dir": str(out)}
    if phase in ("all", "compose"):
        outputs = compose(spec, dirs)
        show = build_showcase(spec, dirs, outputs)
        report["outputs"] = outputs
        report["showcase_dir"] = str(show)
        pub = publish(spec, show)
        if pub:
            report["publish"] = pub
            if pub.get("s3_website_url"):
                report["website_url"] = pub["s3_website_url"] + "/index.html"
    (dirs["art"] / "render_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def _main():
    ap = argparse.ArgumentParser(description="Luxury reel engine")
    ap.add_argument("--spec", help="Path to spec JSON")
    ap.add_argument("--out", help="Output dir (default: projects/<brand>-reel)")
    ap.add_argument("--report", help="Write report JSON to this path")
    ap.add_argument("--phase", default="all",
                    choices=["all", "refs", "clips", "audio", "compose"])
    ap.add_argument("--print-default-spec", action="store_true")
    a = ap.parse_args()
    if a.print_default_spec:
        print(json.dumps(default_spec(), indent=2)); return
    spec = json.loads(Path(a.spec).read_text()) if a.spec else default_spec()
    out = a.out or str(OM_ROOT / "projects" / f"{spec['brand'].lower()}-reel")
    try:
        rep = run(spec, out, phase=a.phase)
    except Exception:
        traceback.print_exc(); sys.exit(1)
    if a.report:
        Path(a.report).write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    _main()
