"""Script quality gates and scene splitting.

A script file is markdown with this shape (the routine writes it):

    # TITLE
    <!-- angle: one sentence -->
    <!-- sources: url1 | url2 | url3 -->
    ## HOOK
    narration...
    ## SCENE: visual keywords | fallback keywords
    narration...
    ## SCENE: ...
    narration...
    ## OUTRO
    narration...

Gates (config.quality_gates): length in the target window, a hook under N
words before the first scene break, enough first-person point-of-view
sentences, at least N sources, no banned phrases, and low n-gram similarity
to every previous script in state/scripts/ so the channel never ships a
template. All gates are deterministic; the routine fixes the script and reruns.
"""
import re
import sys
from pathlib import Path

from .common import STATE, config, load_json, save_json

POV = re.compile(r"\b(I|I'm|I've|I'd|my|we|we're|our|in my (?:view|experience|testing)|here's what I think|I disagree|I tested|I ran|I would|I wouldn't)\b")
SENT = re.compile(r"(?<=[.!?])\s+")


def parse(text):
    title = ""
    angle = ""
    sources = []
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        title = m.group(1).strip()
    m = re.search(r"<!--\s*angle:\s*(.*?)-->", text, re.S)
    if m:
        angle = m.group(1).strip()
    m = re.search(r"<!--\s*sources:\s*(.*?)-->", text, re.S)
    if m:
        sources = [s.strip() for s in m.group(1).split("|") if s.strip()]
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    parts = re.split(r"^##\s+", body, flags=re.M)
    scenes = []
    for part in parts[1:]:
        head, _, narration = part.partition("\n")
        head = head.strip()
        narration = re.sub(r"^#.*$", "", narration, flags=re.M).strip()
        if head.upper().startswith("HOOK"):
            kind, kw = "hook", ""
        elif head.upper().startswith("OUTRO"):
            kind, kw = "outro", ""
        else:
            kind = "scene"
            kw = head.split(":", 1)[1].strip() if ":" in head else head
        primary, _, fallback = kw.partition("|")
        scenes.append({"kind": kind, "keywords": primary.strip(), "fallback": fallback.strip(), "text": narration})
    return {"title": title, "angle": angle, "sources": sources, "scenes": scenes}


def words(text):
    return re.findall(r"[A-Za-z0-9']+", text)


def shingles(text, n=5):
    w = [x.lower() for x in words(text)]
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def similarity(a, b):
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def previous_scripts(exclude=None):
    d = STATE / "scripts"
    d.mkdir(parents=True, exist_ok=True)
    out = []
    for p in sorted(d.glob("*.md")):
        if exclude and p.name == Path(exclude).name:
            continue
        out.append((p.name, p.read_text()))
    return out


def check(text, path=None, cfg=None):
    cfg = cfg or config()
    g = cfg["quality_gates"]
    f = cfg["format"]
    doc = parse(text)
    narration = "\n".join(s["text"] for s in doc["scenes"])
    n_words = len(words(narration))
    minutes = n_words / f["words_per_minute"]
    problems, notes = [], []
    if not doc["title"]:
        problems.append("missing '# TITLE' line")
    if not doc["scenes"]:
        problems.append("no '## HOOK' / '## SCENE:' sections found")
    if minutes < f["target_minutes_min"]:
        problems.append(f"too short: {n_words} words is {minutes:.1f} min at {f['words_per_minute']} wpm; target {f['target_minutes_min']} to {f['target_minutes_max']} min")
    if minutes > f["target_minutes_max"] + 1:
        problems.append(f"too long: {n_words} words is {minutes:.1f} min; target {f['target_minutes_min']} to {f['target_minutes_max']} min")
    hook = next((s for s in doc["scenes"] if s["kind"] == "hook"), None)
    if not hook:
        problems.append("no '## HOOK' section")
    elif len(words(hook["text"])) > g["hook_max_words"]:
        problems.append(f"hook is {len(words(hook['text']))} words; keep it under {g['hook_max_words']}")
    pov = sum(1 for s in SENT.split(narration) if POV.search(s))
    if pov < g["min_pov_sentences"]:
        problems.append(f"only {pov} first-person point-of-view sentences; need at least {g['min_pov_sentences']} (this is the originality defense under the generic-or-repetitive-content policy)")
    if len(doc["sources"]) < g["require_sources"]:
        problems.append(f"{len(doc['sources'])} sources listed; need at least {g['require_sources']} in the '<!-- sources: a | b | c -->' comment")
    low = narration.lower()
    for phrase in g["banned_phrases"]:
        if phrase.lower() in low:
            problems.append(f"banned phrase: '{phrase}'")
    if "\u2014" in text:
        problems.append("em dash found; rewrite the sentence")
    scene_count = sum(1 for s in doc["scenes"] if s["kind"] == "scene")
    expected = max(1, int(minutes * 60 / f["scene_seconds_target"]) // 3)
    if scene_count < expected:
        notes.append(f"{scene_count} scenes for {minutes:.1f} min; more scene breaks (about every 20 to 30 seconds) keep visuals moving")
    worst = (None, 0.0)
    for name, prev in previous_scripts(exclude=path):
        s = similarity(narration, "\n".join(x["text"] for x in parse(prev)["scenes"]))
        if s > worst[1]:
            worst = (name, s)
    if worst[0] and worst[1] > g["max_similarity_to_previous"]:
        problems.append(f"too similar to previous script {worst[0]} (5-gram Jaccard {worst[1]:.2f} > {g['max_similarity_to_previous']}); rewrite, do not template")
    return {"ok": not problems, "problems": problems, "notes": notes, "words": n_words, "minutes": round(minutes, 1),
            "scenes": scene_count, "pov_sentences": pov, "sources": len(doc["sources"]), "max_similarity": round(worst[1], 3), "title": doc["title"]}


def tts_chunks(doc, max_chars=4500):
    """Narration chunks for TTS, each a run of whole scenes under max_chars."""
    chunks, cur = [], []
    size = 0
    for s in doc["scenes"]:
        t = s["text"].strip()
        if not t:
            continue
        if size + len(t) + 2 > max_chars and cur:
            chunks.append("\n\n".join(cur))
            cur, size = [], 0
        cur.append(t)
        size += len(t) + 2
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def main(argv):
    if not argv:
        print("usage: script-check PATH", file=sys.stderr)
        sys.exit(2)
    path = Path(argv[0])
    res = check(path.read_text(), path=str(path))
    for k in ("title", "words", "minutes", "scenes", "pov_sentences", "sources", "max_similarity"):
        print(f"{k}: {res[k]}")
    for n in res["notes"]:
        print("note: " + n)
    for p in res["problems"]:
        print("PROBLEM: " + p)
    print("RESULT: " + ("PASS" if res["ok"] else "FAIL"))
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
