"""Narration: one ElevenLabs request per scene so scene durations are exact.

Env: ELEVENLABS_API_KEY. Output under work/<video>/audio/:
  scene-NN.mp3, narration.mp3, timeline.json (scene start/end seconds),
  words.json (word timings), captions.srt

If the routine produced the voice track through the ElevenLabs connector
instead (no API key in the container), pass --from-audio narration.mp3 and the
scene timeline is estimated from character counts. Captions are then
estimated too; the API path is better.
"""
import base64
import json
import re
import sys
import time
from pathlib import Path

from .common import WORK, config, ffprobe_duration, run, save_json
from .script_tools import parse

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps"
GAP = 0.35  # seconds of silence between scenes


def _request(text, prev, nxt, cfg, key):
    import requests

    v = cfg["voice"]
    body = {
        "text": text,
        "model_id": v.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": {"stability": v.get("stability", 0.5), "similarity_boost": v.get("similarity_boost", 0.75),
                           "style": v.get("style", 0.2), "use_speaker_boost": True},
    }
    if prev:
        body["previous_text"] = prev[-600:]
    if nxt:
        body["next_text"] = nxt[:600]
    for attempt in range(4):
        r = requests.post(API.format(voice=v["voice_id"]), headers={"xi-api-key": key, "accept": "application/json"},
                          json=body, params={"output_format": "mp3_44100_128"}, timeout=180)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"ElevenLabs failed after retries: {r.status_code} {r.text[:200]}")


def words_from_alignment(al, offset):
    chars = al["characters"]
    starts = al["character_start_times_seconds"]
    ends = al["character_end_times_seconds"]
    words, cur, s0 = [], "", None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if cur:
                words.append({"w": cur, "s": round(s0 + offset, 3), "e": round(e_prev + offset, 3)})
                cur, s0 = "", None
            continue
        if s0 is None:
            s0 = s
        cur += c
        e_prev = e
    if cur:
        words.append({"w": cur, "s": round(s0 + offset, 3), "e": round(e_prev + offset, 3)})
    return words


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def build_srt(words, max_words=7, max_seconds=2.8):
    lines, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["e"] - cur[0]["s"] > max_seconds or w["s"] - cur[-1]["e"] > 0.8):
            lines.append(cur)
            cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    out = []
    for i, line in enumerate(lines, 1):
        text = " ".join(x["w"] for x in line)
        out.append(f"{i}\n{srt_time(line[0]['s'])} --> {srt_time(line[-1]['e'] + 0.05)}\n{text}\n")
    return "\n".join(out)


def concat_audio(parts, out, gap=GAP):
    """Concat mp3 parts with a silence gap, re-encoded once."""
    inputs, filt = [], []
    for i, p in enumerate(parts):
        inputs += ["-i", p]
    n = len(parts)
    pad = "".join(f"[{i}:a]apad=pad_dur={gap}[a{i}];" for i in range(n))
    chain = "".join(f"[a{i}]" for i in range(n))
    filt = f"{pad}{chain}concat=n={n}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[out]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", filt, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "160k", out])


def synthesize(video_id, script_path, out_dir=None, cfg=None):
    import os

    cfg = cfg or config()
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set. Either set it or generate narration with the ElevenLabs connector and pass --from-audio.")
    doc = parse(Path(script_path).read_text())
    scenes = [s for s in doc["scenes"] if s["text"].strip()]
    out_dir = Path(out_dir or WORK / video_id / "audio")
    out_dir.mkdir(parents=True, exist_ok=True)
    parts, timeline, words = [], [], []
    t = 0.0
    for i, s in enumerate(scenes):
        mp3 = out_dir / f"scene-{i:02}.mp3"
        meta = out_dir / f"scene-{i:02}.json"
        if not mp3.exists() or not meta.exists():
            prev = scenes[i - 1]["text"] if i else ""
            nxt = scenes[i + 1]["text"] if i + 1 < len(scenes) else ""
            res = _request(s["text"], prev, nxt, cfg, key)
            mp3.write_bytes(base64.b64decode(res["audio_base64"]))
            save_json(meta, res["alignment"])
            print(f"voiced scene {i} ({len(s['text'])} chars)", file=sys.stderr)
        al = json.loads(meta.read_text())
        dur = ffprobe_duration(mp3)
        words += words_from_alignment(al, t)
        timeline.append({"index": i, "kind": s["kind"], "keywords": s["keywords"], "fallback": s["fallback"],
                         "start": round(t, 3), "end": round(t + dur, 3), "duration": round(dur + GAP, 3), "chars": len(s["text"])})
        t += dur + GAP
        parts.append(str(mp3))
    narration = out_dir / "narration.mp3"
    concat_audio(parts, str(narration))
    total = ffprobe_duration(narration)
    save_json(out_dir / "timeline.json", {"total_seconds": round(total, 3), "scenes": timeline})
    save_json(out_dir / "words.json", words)
    (out_dir / "captions.srt").write_text(build_srt(words))
    chars = sum(len(s["text"]) for s in scenes)
    print(f"narration {total/60:.1f} min, {len(scenes)} scenes, {chars} chars (ElevenLabs bills per character)")
    return out_dir


def timeline_from_audio(video_id, script_path, audio_path, out_dir=None):
    """Estimate scene boundaries proportionally to character counts."""
    doc = parse(Path(script_path).read_text())
    scenes = [s for s in doc["scenes"] if s["text"].strip()]
    out_dir = Path(out_dir or WORK / video_id / "audio")
    out_dir.mkdir(parents=True, exist_ok=True)
    narration = out_dir / "narration.mp3"
    if Path(audio_path).resolve() != narration.resolve():
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", audio_path, "-c:a", "libmp3lame", "-b:a", "160k", str(narration)])
    total = ffprobe_duration(narration)
    chars = sum(len(s["text"]) for s in scenes)
    t, timeline, words = 0.0, [], []
    for i, s in enumerate(scenes):
        dur = total * len(s["text"]) / chars
        timeline.append({"index": i, "kind": s["kind"], "keywords": s["keywords"], "fallback": s["fallback"],
                         "start": round(t, 3), "end": round(t + dur, 3), "duration": round(dur, 3), "chars": len(s["text"]), "estimated": True})
        toks = re.findall(r"\S+", s["text"])
        per = dur / max(1, len(toks))
        for k, w in enumerate(toks):
            words.append({"w": w, "s": round(t + k * per, 3), "e": round(t + (k + 1) * per, 3)})
        t += dur
    save_json(out_dir / "timeline.json", {"total_seconds": round(total, 3), "scenes": timeline, "estimated": True})
    save_json(out_dir / "words.json", words)
    (out_dir / "captions.srt").write_text(build_srt(words))
    print(f"timeline estimated from {audio_path}: {total/60:.1f} min, {len(scenes)} scenes")
    return out_dir
