"""YouTube Data API v3 and YouTube Analytics API, with plain requests.

Env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (see docs/SETUP.md).
Verbs: auth-url, auth-exchange CODE, upload VIDEO_ID, stats, analytics.

Quota facts (developers.google.com/youtube/v3/getting-started#quota, 2026-10-15):
100 videos.insert per project per day, 10,000 units for everything else, an
upload costs 1 unit. The engine caps itself at 90 uploads a day.
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .common import STATE, WORK, config, load_json, now_iso, save_json, today
from . import ledger

TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/yt-analytics.readonly", "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"]
REDIRECT = "http://localhost:8765/"
UPLOAD_CAP = 90


def _creds():
    cid, sec, rt = (os.environ.get(k) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"))
    if not (cid and sec and rt):
        raise SystemExit("YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN must be set (docs/SETUP.md step 4)")
    return cid, sec, rt


def auth_url():
    cid = os.environ.get("YT_CLIENT_ID") or "YOUR_CLIENT_ID"
    from urllib.parse import urlencode

    return AUTH_URL + "?" + urlencode({"client_id": cid, "redirect_uri": REDIRECT, "response_type": "code",
                                       "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent"})


def auth_exchange(code):
    import requests

    cid, sec = os.environ.get("YT_CLIENT_ID"), os.environ.get("YT_CLIENT_SECRET")
    r = requests.post(TOKEN_URL, data={"code": code, "client_id": cid, "client_secret": sec, "redirect_uri": REDIRECT,
                                       "grant_type": "authorization_code"}, timeout=30)
    r.raise_for_status()
    return r.json()


def access_token():
    import requests

    cid, sec, rt = _creds()
    r = requests.post(TOKEN_URL, data={"client_id": cid, "client_secret": sec, "refresh_token": rt, "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"token refresh failed: {r.status_code} {r.text[:200]}. If the consent screen is in Testing mode the refresh token expires after 7 days; set it to Production.")
    return r.json()["access_token"]


def _uploads_today():
    u = load_json(STATE / "uploads.json", {})
    return u.get(today(), 0)


def _count_upload():
    u = load_json(STATE / "uploads.json", {})
    u[today()] = u.get(today(), 0) + 1
    save_json(STATE / "uploads.json", u)


def first_sentence(text):
    return re.split(r"(?<=[.!?])\s", text.strip(), 1)[0].strip().lower()


def uniqueness_checks(rec, description, thumb_hash):
    from .assemble import hamming

    problems = []
    fs = first_sentence(description)
    for other in ledger.all_records():
        if other["id"] == rec["id"]:
            continue
        od = other.get("youtube", {}).get("description")
        if od and first_sentence(od) == fs:
            problems.append(f"description first sentence duplicates {other['id']}")
        oh = other.get("youtube", {}).get("thumbnail_ahash")
        if oh and thumb_hash and hamming(oh, thumb_hash) < 6:
            problems.append(f"thumbnail nearly identical to {other['id']} (hamming {hamming(oh, thumb_hash)})")
    return problems


def next_publish_slot(cfg):
    """Next configured publish day/time after now, as RFC3339 UTC."""
    from zoneinfo import ZoneInfo

    tz = ZoneInfo(cfg["cadence"]["timezone"])
    hh, mm = (int(x) for x in cfg["cadence"]["publish_time_local"].split(":"))
    days = {d: i for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])}
    wanted = {days[d] for d in cfg["cadence"]["publish_days"]}
    taken = {r["youtube"].get("publish_at") for r in ledger.all_records() if r.get("youtube", {}).get("publish_at")}
    now = datetime.now(tz)
    for i in range(1, 60):
        cand = (now + timedelta(days=i)).replace(hour=hh, minute=mm, second=0, microsecond=0)
        iso = cand.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if cand.weekday() in wanted and iso not in taken:
            return iso
    raise RuntimeError("no publish slot found")


def upload(video_id, cfg=None, publish_at=None, dry_run=False):
    import requests

    cfg = cfg or config()
    rec = ledger.load(video_id)
    pub = cfg["publishing"]
    if rec["status"] not in ("assembled", "uploaded"):
        raise SystemExit(f"{video_id} is '{rec['status']}', not 'assembled'; the render must exist and the record must have been approved")
    if not rec["history"] or not any(h["status"] == "approved" for h in rec["history"]):
        raise SystemExit(f"{video_id} was never approved; refusing to upload (publishing.require_human_approval)")
    work = WORK / video_id
    final = Path(rec["artifacts"].get("final", work / "final.mp4"))
    meta = load_json(work / "metadata.json")
    if not final.exists() or not meta:
        raise SystemExit("need final.mp4 and metadata.json (title, description, tags)")
    description = meta["description"].rstrip() + "\n\n" + cfg["channel"]["description_footer"]
    thumb_hash = (work / "thumbnail.ahash").read_text().strip() if (work / "thumbnail.ahash").exists() else None
    problems = uniqueness_checks(rec, description, thumb_hash)
    if problems:
        raise SystemExit("packaging not unique: " + "; ".join(problems))
    if _uploads_today() >= UPLOAD_CAP:
        raise SystemExit(f"upload cap {UPLOAD_CAP}/day reached")
    publish_at = publish_at or next_publish_slot(cfg)
    body = {
        "snippet": {"title": meta["title"][:100], "description": description[:5000], "tags": meta.get("tags", [])[: pub["tags_max"]],
                    "categoryId": pub["category_id"], "defaultLanguage": cfg["channel"]["language"]},
        "status": {"privacyStatus": "private", "publishAt": publish_at, "selfDeclaredMadeForKids": pub["made_for_kids"],
                   "containsSyntheticMedia": pub["contains_synthetic_media"], "license": "youtube", "embeddable": True},
    }
    if dry_run:
        print(json.dumps(body, indent=2))
        return body
    tok = access_token()
    h = {"Authorization": f"Bearer {tok}"}
    size = final.stat().st_size
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", params={"uploadType": "resumable", "part": "snippet,status"},
                      headers={**h, "Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Length": str(size),
                               "X-Upload-Content-Type": "video/mp4"}, json=body, timeout=60)
    r.raise_for_status()
    session = r.headers["Location"]
    with open(final, "rb") as f:
        r = requests.put(session, headers={**h, "Content-Type": "video/mp4", "Content-Length": str(size)}, data=f, timeout=3600)
    if r.status_code not in (200, 201):
        raise SystemExit(f"upload failed {r.status_code}: {r.text[:300]}")
    yt_id = r.json()["id"]
    _count_upload()
    thumb = work / "thumbnail.jpg"
    if thumb.exists():
        with open(thumb, "rb") as f:
            tr = requests.post("https://www.googleapis.com/upload/youtube/v3/thumbnails/set", params={"videoId": yt_id},
                               headers={**h, "Content-Type": "image/jpeg"}, data=f, timeout=120)
        if tr.status_code != 200:
            print(f"thumbnail set failed {tr.status_code}: {tr.text[:200]} (channel may need phone verification for custom thumbnails)", file=sys.stderr)
    rec["youtube"] = {"video_id": yt_id, "url": f"https://youtu.be/{yt_id}", "publish_at": publish_at, "uploaded_at": now_iso(),
                      "title": body["snippet"]["title"], "description": description, "thumbnail_ahash": thumb_hash, "privacy": "private until publishAt"}
    rec["title"] = body["snippet"]["title"]
    ledger.set_status(rec, "uploaded", f"scheduled for {publish_at}")
    print(f"uploaded {yt_id} scheduled {publish_at}")
    return rec


def video_stats(yt_ids):
    import requests

    tok = access_token()
    r = requests.get("https://www.googleapis.com/youtube/v3/videos", params={"part": "statistics,status,snippet", "id": ",".join(yt_ids)},
                     headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    r.raise_for_status()
    return {v["id"]: v for v in r.json().get("items", [])}


def analytics(start, end, metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares",
              dimensions="video", filters=None, sort="-views", max_results=50, monetary=False):
    import requests

    tok = access_token()
    if monetary:
        metrics += ",estimatedRevenue,estimatedAdRevenue,cpm,playbackBasedCpm,monetizedPlaybacks"
    params = {"ids": "channel==MINE", "startDate": start, "endDate": end, "metrics": metrics, "dimensions": dimensions,
              "sort": sort, "maxResults": max_results}
    if filters:
        params["filters"] = filters
    r = requests.get("https://youtubeanalytics.googleapis.com/v2/reports", params=params, headers={"Authorization": f"Bearer {tok}"}, timeout=60)
    if r.status_code != 200:
        raise SystemExit(f"analytics {r.status_code}: {r.text[:300]}")
    data = r.json()
    cols = [c["name"] for c in data.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in data.get("rows", [])]
