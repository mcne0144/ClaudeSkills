"""Per-video state. One JSON file per video under state/videos/.

Statuses move forward only:
  idea -> approved -> scripted -> voiced -> visualized -> assembled -> uploaded -> published -> measured -> archived
Side exits: rejected, failed (with .error). A stage is re-runnable: each verb
checks for its artifact before doing paid work.
"""
import sys
from pathlib import Path

from .common import STATE, load_json, now_iso, save_json, slugify, today

VIDEOS = STATE / "videos"
ORDER = ["idea", "approved", "scripted", "voiced", "visualized", "assembled",
         "uploaded", "published", "measured", "archived"]
EXITS = {"rejected", "failed"}


def path_for(video_id):
    return VIDEOS / f"{video_id}.json"


def new(title, niche, angle="", source_urls=None, kind="evergreen", slug=None):
    vid = f"{today()}-{slug or slugify(title)}"
    if path_for(vid).exists():
        n = 2
        while path_for(f"{vid}-{n}").exists():
            n += 1
        vid = f"{vid}-{n}"
    rec = {
        "id": vid,
        "status": "idea",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "niche": niche,
        "kind": kind,
        "working_title": title,
        "title_candidates": [title],
        "title": None,
        "angle": angle,
        "sources": source_urls or [],
        "artifacts": {},
        "youtube": {},
        "metrics": [],
        "history": [{"at": now_iso(), "status": "idea", "note": "created"}],
    }
    save(rec)
    return rec


def load(video_id):
    rec = load_json(path_for(video_id))
    if rec is None:
        raise FileNotFoundError(f"no video record {video_id}")
    return rec


def save(rec):
    rec["updated_at"] = now_iso()
    save_json(path_for(rec["id"]), rec)
    return rec


def set_status(rec, status, note=""):
    if status not in ORDER and status not in EXITS:
        raise ValueError(f"unknown status {status}")
    if status in ORDER and rec["status"] in ORDER and ORDER.index(status) < ORDER.index(rec["status"]):
        raise ValueError(f"{rec['id']}: cannot move backwards {rec['status']} -> {status}")
    rec["status"] = status
    rec["history"].append({"at": now_iso(), "status": status, "note": note})
    return save(rec)


def set_artifact(rec, key, path):
    rec["artifacts"][key] = str(path)
    return save(rec)


def all_records():
    VIDEOS.mkdir(parents=True, exist_ok=True)
    recs = [load_json(p) for p in sorted(VIDEOS.glob("*.json"))]
    return [r for r in recs if r]


def by_status(status):
    return [r for r in all_records() if r["status"] == status]


def next_in(status):
    recs = by_status(status)
    return recs[0] if recs else None


def board():
    recs = all_records()
    counts = {s: 0 for s in ORDER + sorted(EXITS)}
    for r in recs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["status      count", "-----------------"]
    for s, c in counts.items():
        if c:
            lines.append(f"{s:<11} {c}")
    lines.append("")
    for r in recs[-15:]:
        lines.append(f"{r['id']:<60} {r['status']:<11} {r.get('title') or r['working_title']}")
    return "\n".join(lines)


def main(argv):
    if not argv or argv[0] == "board":
        print(board())
        return
    if argv[0] == "new":
        title = argv[1]
        niche = argv[2] if len(argv) > 2 else "unset"
        rec = new(title, niche)
        print(rec["id"])
        return
    if argv[0] == "set":
        rec = load(argv[1])
        set_status(rec, argv[2], " ".join(argv[3:]))
        print(f"{rec['id']} -> {rec['status']}")
        return
    if argv[0] == "show":
        import json
        print(json.dumps(load(argv[1]), indent=2))
        return
    print("usage: ledger board | new TITLE NICHE | set ID STATUS [note] | show ID", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
