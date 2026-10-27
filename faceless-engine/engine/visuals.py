"""Visual plan: one asset per scene, chosen in this order.

1. A pre-supplied image or clip the routine dropped in work/<id>/supplied/scene-NN.*
   (AI images from the ElevenLabs or Higgsfield connectors, screenshots, charts).
2. A Pexels stock clip for the scene's keywords, then its fallback keywords,
   skipping anything in state/used_assets.json (never reuse a clip across videos).
3. A rendered text card (Pillow) with the scene's key phrase.

Writes work/<id>/visuals/plan.json and reports the visual mix, which
assemble.py checks so a video is never a slideshow.
Env: PEXELS_API_KEY (free at https://www.pexels.com/api/).
"""
import json
import os
import random
import sys
from pathlib import Path

from .common import ROOT, STATE, WORK, config, load_json, save_json

PEXELS_VIDEOS = "https://api.pexels.com/videos/search"
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"


def _font(path, size):
    from PIL import ImageFont

    for p in (path, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def used_assets():
    return load_json(STATE / "used_assets.json", {"pexels": []})


def mark_used(kind, asset_id, video_id):
    u = used_assets()
    u.setdefault(kind, []).append({"id": asset_id, "video": video_id})
    save_json(STATE / "used_assets.json", u)


def pexels_search(query, key, per_page=12, min_seconds=6):
    import requests

    r = requests.get(PEXELS_VIDEOS, headers={"Authorization": key},
                     params={"query": query, "orientation": "landscape", "per_page": per_page, "size": "medium"}, timeout=30)
    if r.status_code != 200:
        print(f"pexels {r.status_code} for '{query}'", file=sys.stderr)
        return []
    out = []
    for v in r.json().get("videos", []):
        if v.get("duration", 0) < min_seconds:
            continue
        files = [f for f in v.get("video_files", []) if f.get("width", 0) >= 1280 and f.get("file_type") == "video/mp4"]
        if not files:
            continue
        files.sort(key=lambda f: abs(f.get("width", 0) - 1920))
        out.append({"id": v["id"], "url": files[0]["link"], "duration": v["duration"], "width": files[0]["width"],
                    "credit": v.get("user", {}).get("name"), "page": v.get("url")})
    return out


def download(url, dest):
    import requests

    if dest.exists() and dest.stat().st_size > 0:
        return dest
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return dest


def render_card(text, dest, subtitle="", style="dark", size=(1920, 1080)):
    from PIL import Image, ImageDraw

    W, H = size
    img = Image.new("RGB", size, (14, 16, 20) if style == "dark" else (245, 243, 238))
    d = ImageDraw.Draw(img)
    # soft gradient band
    for y in range(H):
        a = int(18 + 22 * y / H)
        d.line([(0, y), (W, y)], fill=(a, a + 2, a + 8) if style == "dark" else (245 - a // 6, 243 - a // 6, 238 - a // 8))
    fg = (240, 240, 236) if style == "dark" else (24, 24, 28)
    accent = (70, 255, 155)
    d.rectangle([120, 440, 160, 640], fill=accent)
    font = _font(FONT_BOLD, 88)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) > W - 420:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    lines = lines[:4]
    y = H // 2 - (len(lines) * 104) // 2
    for ln in lines:
        d.text((200, y), ln, font=font, fill=fg)
        y += 104
    if subtitle:
        d.text((200, y + 24), subtitle[:90], font=_font(FONT_REG, 40), fill=(150, 156, 160))
    img.save(dest, quality=92)
    return dest


def plan(video_id, cfg=None, seed=None):
    cfg = cfg or config()
    work = WORK / video_id
    tl = load_json(work / "audio" / "timeline.json")
    if not tl:
        raise SystemExit("no audio timeline; run voice first")
    out = work / "visuals"
    out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("PEXELS_API_KEY")
    rng = random.Random(seed or video_id)
    used = {str(u["id"]) for u in used_assets().get("pexels", [])}
    supplied = work / "supplied"
    plan_items, mix = [], {"supplied": 0, "stock": 0, "card": 0}
    for s in tl["scenes"]:
        i = s["index"]
        item = {"index": i, "start": s["start"], "duration": s["duration"], "kind": None, "path": None}
        pre = sorted(supplied.glob(f"scene-{i:02}.*")) if supplied.exists() else []
        if pre:
            p = pre[0]
            item.update(kind="video" if p.suffix.lower() in (".mp4", ".mov", ".webm") else "image", path=str(p), source="supplied")
            mix["supplied"] += 1
        elif key and s["kind"] == "scene":
            picked = None
            for q in (s["keywords"], s["fallback"]):
                if not q:
                    continue
                cands = [c for c in pexels_search(q, key) if str(c["id"]) not in used]
                if cands:
                    picked = rng.choice(cands[:6])
                    break
            if picked:
                dest = out / f"scene-{i:02}.mp4"
                download(picked["url"], dest)
                used.add(str(picked["id"]))
                mark_used("pexels", picked["id"], video_id)
                item.update(kind="video", path=str(dest), source="pexels", credit=picked["credit"], page=picked["page"])
                mix["stock"] += 1
        if not item["kind"]:
            phrase = (s["keywords"] or {"hook": "Here is the question", "outro": "What I would do next"}.get(s["kind"], "")).split("|")[0]
            dest = out / f"scene-{i:02}.jpg"
            render_card(phrase.strip().capitalize(), dest, style=cfg["visuals"].get("card_style", "dark"))
            item.update(kind="image", path=str(dest), source="card")
            mix["card"] += 1
        plan_items.append(item)
    total = len(plan_items)
    result = {"video": video_id, "scenes": plan_items, "mix": mix,
              "card_share": round(mix["card"] / total, 2) if total else 1.0}
    save_json(out / "plan.json", result)
    print(f"visual plan: {total} scenes, supplied={mix['supplied']} stock={mix['stock']} cards={mix['card']} card_share={result['card_share']}")
    if result["card_share"] > 0.4:
        print("WARNING: more than 40% text cards. Supply AI images or set PEXELS_API_KEY; a slideshow is not monetizable (docs/POLICY.md).")
    return result
