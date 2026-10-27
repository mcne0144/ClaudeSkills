#!/usr/bin/env python3
"""faceless: the deterministic half of the faceless YouTube pipeline.

  scan                         fetch + parse the facelessfinder briefing, archive, flag staleness
  board                        rank niches for this operator (state/niche_board.json)
  signals                      live breakout rows via the YouTube Data API, else the archived facelessfinder breakouts
  status                       pipeline board from the ledger
  new "TITLE" NICHE [--kind evergreen|timely] [--angle "..."] [--source URL ...]
  approve ID [note]            human gate; nothing downstream runs without it
  reject ID [note]
  script-check PATH            quality gates (length, hook, point of view, sources, similarity, banned phrases)
  script-save ID PATH          copy a passing script into state/scripts/ and mark scripted
  voice ID [--from-audio MP3]  ElevenLabs narration per scene, or timeline from supplied audio
  visuals ID                   per-scene assets (supplied, Pexels, cards) and the mix check
  assemble ID                  ffmpeg render + thumbnail
  metadata ID PATH.json        attach {title, description, tags}
  upload ID [--dry-run] [--publish-at RFC3339]
  measure [--monetary]         pull stats for uploaded videos, update learnings
  report                       write reports/weekly-YYYY-Www.md
  progress                     revenue math against the target
  doctor                       check tools, keys and config
  yt-auth-url | yt-auth-exchange CODE
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import analytics, assemble, ff_report, ledger, niche_score, script_tools, signals, tts, visuals, youtube  # noqa: E402
from engine.common import ROOT, STATE, WORK, config, load_json, save_json  # noqa: E402


def _flag(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        val = argv[i + 1]
        del argv[i:i + 2]
        return val
    return default


def _flag_all(argv, name):
    out = []
    while name in argv:
        i = argv.index(name)
        out.append(argv[i + 1])
        del argv[i:i + 2]
    return out


def _bool(argv, name):
    if name in argv:
        argv.remove(name)
        return True
    return False


def cmd_doctor(argv):
    import os

    ok = True
    for tool in ("ffmpeg", "ffprobe"):
        print(f"{tool:<22} {'ok' if shutil.which(tool) else 'MISSING'}")
        ok = ok and bool(shutil.which(tool))
    try:
        import PIL  # noqa: F401
        import requests  # noqa: F401
        print(f"{'python deps':<22} ok (Pillow, requests)")
    except ImportError as e:
        print(f"{'python deps':<22} MISSING {e}")
        ok = False
    for k, why in (("ELEVENLABS_API_KEY", "narration via API (else use the connector + --from-audio)"),
                   ("PEXELS_API_KEY", "stock footage (else supply images)"),
                   ("YT_CLIENT_ID", "upload"), ("YT_CLIENT_SECRET", "upload"), ("YT_REFRESH_TOKEN", "upload and analytics")):
        print(f"{k:<22} {'set' if os.environ.get(k) else 'not set'}  ({why})")
    cfg = config()
    print(f"{'channel':<22} {cfg['channel']['name']} {cfg['channel'].get('youtube_channel_id') or '(no channel id yet)'}")
    print(f"{'niche':<22} {cfg['niche']['primary']}")
    print(f"{'font':<22} {'ok' if Path(visuals.FONT_BOLD).exists() else 'Inter missing, DejaVu fallback'}")
    music = list((ROOT / 'assets' / 'music').glob('*.mp3'))
    print(f"{'music tracks':<22} {len(music)} (drop royalty-free mp3s in assets/music/)")
    rep = load_json(STATE / "ff" / "latest.json")
    if rep:
        st = ff_report.staleness(rep)
        print(f"{'facelessfinder':<22} week_of {rep.get('week_of')} stale={st['stale']}")
    else:
        print(f"{'facelessfinder':<22} no report archived yet (run scan)")
    print("RESULT: " + ("ok" if ok else "problems"))


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    if cmd == "scan":
        return ff_report.main(args)
    if cmd == "board":
        return niche_score.main(args)
    if cmd == "status":
        print(ledger.board())
        return
    if cmd == "signals":
        return signals.main(args)
    if cmd == "new":
        kind = _flag(args, "--kind", "evergreen")
        angle = _flag(args, "--angle", "")
        sources = _flag_all(args, "--source")
        rec = ledger.new(args[0], args[1] if len(args) > 1 else config()["niche"]["primary"], angle=angle, source_urls=sources, kind=kind)
        print(rec["id"])
        return
    if cmd in ("approve", "reject"):
        rec = ledger.load(args[0])
        ledger.set_status(rec, "approved" if cmd == "approve" else "rejected", " ".join(args[1:]) or cmd)
        print(f"{rec['id']} -> {rec['status']}")
        return
    if cmd == "script-check":
        return script_tools.main(args)
    if cmd == "script-save":
        rec = ledger.load(args[0])
        if rec["status"] not in ("approved", "scripted"):
            sys.exit(f"{rec['id']} must be approved before a script is saved (status {rec['status']})")
        res = script_tools.check(Path(args[1]).read_text(), path=args[1])
        if not res["ok"]:
            sys.exit("script fails gates: " + "; ".join(res["problems"]))
        dest = STATE / "scripts" / f"{rec['id']}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(args[1], dest)
        rec["title"] = rec.get("title") or res["title"]
        ledger.set_artifact(rec, "script", dest)
        ledger.set_status(rec, "scripted", f"{res['words']} words, {res['minutes']} min")
        print(f"saved {dest}")
        return
    if cmd == "voice":
        rec = ledger.load(args[0])
        if rec["status"] not in ("scripted", "voiced"):
            sys.exit(f"{rec['id']} must be scripted first (status {rec['status']})")
        script = rec["artifacts"]["script"]
        audio = _flag(args, "--from-audio")
        out = tts.timeline_from_audio(rec["id"], script, audio) if audio else tts.synthesize(rec["id"], script)
        ledger.set_artifact(rec, "narration", out / "narration.mp3")
        ledger.set_status(rec, "voiced", "estimated timeline" if audio else "elevenlabs per scene")
        return
    if cmd == "visuals":
        rec = ledger.load(args[0])
        if rec["status"] not in ("voiced", "visualized"):
            sys.exit(f"{rec['id']} must be voiced first (status {rec['status']})")
        res = visuals.plan(rec["id"])
        ledger.set_artifact(rec, "visual_plan", WORK / rec["id"] / "visuals" / "plan.json")
        ledger.set_status(rec, "visualized", f"mix {res['mix']}")
        return
    if cmd == "assemble":
        rec = ledger.load(args[0])
        if rec["status"] not in ("visualized", "assembled"):
            sys.exit(f"{rec['id']} must be visualized first (status {rec['status']})")
        final = assemble.build(rec["id"], title=rec.get("title") or rec["working_title"])
        ledger.set_artifact(rec, "final", final)
        ledger.set_artifact(rec, "thumbnail", final.parent / "thumbnail.jpg")
        ledger.set_status(rec, "assembled", "rendered")
        return
    if cmd == "metadata":
        rec = ledger.load(args[0])
        meta = json.loads(Path(args[1]).read_text())
        for k in ("title", "description", "tags"):
            if k not in meta:
                sys.exit(f"metadata missing {k}")
        save_json(WORK / rec["id"] / "metadata.json", meta)
        rec["title"] = meta["title"]
        ledger.save(rec)
        print("metadata attached")
        return
    if cmd == "upload":
        dry = _bool(args, "--dry-run")
        at = _flag(args, "--publish-at")
        return youtube.upload(args[0], publish_at=at, dry_run=dry)
    if cmd == "measure":
        return analytics.measure(monetary=_bool(args, "--monetary"))
    if cmd == "report":
        return analytics.weekly_report()
    if cmd == "progress":
        print(analytics.progress())
        return
    if cmd == "doctor":
        return cmd_doctor(args)
    if cmd == "yt-auth-url":
        print(youtube.auth_url())
        return
    if cmd == "yt-auth-exchange":
        print(json.dumps(youtube.auth_exchange(args[0]), indent=2))
        return
    sys.exit(f"unknown command {cmd}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv[1:])
