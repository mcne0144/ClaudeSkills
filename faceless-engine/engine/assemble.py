"""Assemble the final video with ffmpeg.

Inputs: work/<id>/audio/{narration.mp3,captions.srt,timeline.json},
        work/<id>/visuals/plan.json, optional assets/music/*.mp3
Output: work/<id>/final.mp4 (1080p30, yuv420p, faststart), thumbnail.jpg, thumbnail.ahash

Every scene becomes a normalized clip of exactly its narration duration (stock
clips loop or trim, stills get a Ken Burns move so nothing is static), scenes
are joined with 0.5 s crossfades, captions are burned in, and music is ducked
under the narration with a sidechain compressor.
"""
import json
import random
import sys
from pathlib import Path

from .common import ROOT, WORK, config, ffprobe_duration, load_json, run, save_json
from .visuals import _font, FONT_BOLD

FADE = 0.5


def _scene_clip(item, dest, w, h, fps, rng):
    d = item["duration"] + FADE  # extra so xfade overlap never starves
    if item["kind"] == "video":
        run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", item["path"], "-t", f"{d:.3f}",
             "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},setsar=1",
             "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", dest], quiet=True)
    else:
        frames = int(d * fps)
        z_from, z_to = (1.0, 1.12) if rng.random() < 0.5 else (1.12, 1.0)
        x = rng.choice(["iw/2-(iw/zoom/2)", "iw/2-(iw/zoom/2)+(on/{f})*40".format(f=frames)])
        y = rng.choice(["ih/2-(ih/zoom/2)", "ih/2-(ih/zoom/2)-(on/{f})*30".format(f=frames)])
        z = f"{z_from}+({z_to}-{z_from})*on/{frames}"
        run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", item["path"], "-t", f"{d:.3f}",
             "-vf", f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps},setsar=1",
             "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", dest], quiet=True)
    return dest


def _xfade_concat(clips, durations, dest):
    if len(clips) == 1:
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", clips[0], "-t", f"{durations[0]:.3f}", "-c", "copy", dest], quiet=True)
        return dest
    inputs = []
    for c in clips:
        inputs += ["-i", c]
    filt, prev, offset = [], "[0:v]", 0.0
    for i in range(1, len(clips)):
        offset += durations[i - 1] - (FADE if i > 1 else 0)
        offset_i = sum(durations[:i]) - FADE * i
        out = f"[v{i}]"
        filt.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={offset_i:.3f}{out}")
        prev = out
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", prev,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", dest], quiet=True)
    return dest


def _mux(video, narration, srt, music, dest, cfg, total):
    m = cfg["music"]
    args = ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", narration]
    fc = []
    if music and m.get("enabled"):
        args += ["-stream_loop", "-1", "-i", music]
        fc.append(f"[2:a]volume={m['volume']},atrim=0:{total:.3f},afade=t=out:st={max(0, total-3):.3f}:d=3[m]")
        fc.append("[m][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=600[md]")
        fc.append("[1:a][md]amix=inputs=2:duration=first:dropout_transition=2,alimiter=limit=0.95[a]")
    else:
        fc.append("[1:a]alimiter=limit=0.95[a]")
    vf = ""
    if srt and cfg["format"].get("captions"):
        style = "FontName=Inter,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H66000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48,Bold=1"
        vf = f"subtitles='{srt}':force_style='{style}'"
    fc.insert(0, f"[0:v]{vf}[v]" if vf else "[0:v]null[v]")
    args += ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
             "-movflags", "+faststart", dest]
    run(args, quiet=True)
    return dest


def average_hash(path, size=8):
    from PIL import Image

    img = Image.open(path).convert("L").resize((size, size))
    px = list(img.getdata())
    avg = sum(px) / len(px)
    return "".join("1" if p > avg else "0" for p in px)


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def thumbnail(video, title_text, dest, at=None, w=1280, h=720):
    from PIL import Image, ImageDraw, ImageFilter

    frame = Path(dest).with_suffix(".frame.jpg")
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{at or 12:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={w}:{h}", str(frame)], quiet=True)
    img = Image.open(frame).convert("RGB")
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    img = Image.blend(img, dark, 0.35)
    d = ImageDraw.Draw(img)
    font = _font(FONT_BOLD, 96)
    words, lines, cur = title_text.upper().split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) > w - 160:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        lines.append(cur)
    lines = lines[:3]
    y = h - 80 - len(lines) * 108
    for ln in lines:
        for dx, dy in ((-4, -4), (4, 4), (-4, 4), (4, -4)):
            d.text((80 + dx, y + dy), ln, font=font, fill=(0, 0, 0))
        d.text((80, y), ln, font=font, fill=(255, 230, 60))
        y += 108
    img.save(dest, quality=90, optimize=True)
    while Path(dest).stat().st_size > 2_000_000:
        img = img.resize((int(img.width * 0.9), int(img.height * 0.9)))
        img.save(dest, quality=85, optimize=True)
    return dest


def build(video_id, title=None, cfg=None, music=None):
    cfg = cfg or config()
    work = WORK / video_id
    tl = load_json(work / "audio" / "timeline.json")
    vp = load_json(work / "visuals" / "plan.json")
    if not tl or not vp:
        raise SystemExit("need audio/timeline.json and visuals/plan.json first (voice, visuals)")
    if vp["card_share"] > 0.5:
        raise SystemExit(f"refusing to render: {vp['card_share']:.0%} of scenes are text cards; that is a slideshow (docs/POLICY.md). Supply images or stock.")
    w, h = (int(x) for x in cfg["format"]["resolution"].split("x"))
    fps = cfg["format"]["fps"]
    clips_dir = work / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(video_id)
    clips, durs = [], []
    for item in vp["scenes"]:
        dest = clips_dir / f"scene-{item['index']:02}.mp4"
        if not dest.exists():
            _scene_clip(item, str(dest), w, h, fps, rng)
        clips.append(str(dest))
        durs.append(item["duration"])
    joined = work / "joined.mp4"
    _xfade_concat(clips, durs, str(joined))
    total = tl["total_seconds"]
    music_path = music
    if music_path is None:
        tracks = sorted((ROOT / "assets" / "music").glob("*.mp3"))
        music_path = str(rng.choice(tracks)) if tracks else None
    srt = work / "audio" / "captions.srt"
    final = work / "final.mp4"
    _mux(str(joined), str(work / "audio" / "narration.mp3"), str(srt) if srt.exists() else None, music_path, str(final), cfg, total)
    thumb = work / "thumbnail.jpg"
    supplied_thumb = next(iter(sorted((work / "supplied").glob("thumbnail.*"))), None) if (work / "supplied").exists() else None
    if supplied_thumb:
        from PIL import Image

        Image.open(supplied_thumb).convert("RGB").resize((1280, 720)).save(thumb, quality=90, optimize=True)
    else:
        thumbnail(str(joined), title or video_id, str(thumb), at=min(12, total / 3))
    (work / "thumbnail.ahash").write_text(average_hash(thumb))
    save_json(work / "render.json", {"video": video_id, "seconds": round(ffprobe_duration(final), 2), "scenes": len(clips),
                                     "mix": vp["mix"], "music": music_path, "captions": srt.exists()})
    print(f"rendered {final} ({ffprobe_duration(final)/60:.1f} min)")
    return final
