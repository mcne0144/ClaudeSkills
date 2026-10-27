import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
REPORTS = ROOT / "reports"
WORK = Path(os.environ.get("FACELESS_WORK", str(ROOT / "work")))


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with p.open() as f:
        return json.load(f)


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    tmp.replace(p)


def config():
    cfg = load_json(ROOT / "config.json", {})
    local = load_json(ROOT / "config.local.json", {})
    cfg.update(local)
    return cfg


def slugify(text, limit=48):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:limit].rstrip("-") or "untitled"


def human_number(text):
    """'27K' -> 27000, '2.6K' -> 2600, '1.0M' -> 1000000, '460' -> 460."""
    if text is None:
        return None
    t = text.strip().replace(",", "")
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*([KkMmBb]?)$", t)
    if not m:
        return None
    val = float(m.group(1))
    mult = {"": 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[m.group(2).lower()]
    return int(round(val * mult))


def run(cmd, check=True, capture=False, quiet=False):
    if not quiet:
        print("$ " + " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.run([str(c) for c in cmd], check=check, capture_output=capture, text=True)


def ffprobe_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
               "default=noprint_wrappers=1:nokey=1", path], capture=True, quiet=True).stdout.strip()
    return float(out) if out else 0.0


def die(msg, code=2):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(code)
