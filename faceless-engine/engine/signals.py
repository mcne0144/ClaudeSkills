"""Live topic signals without vidIQ: the YouTube Data API with the same OAuth
credentials the uploader uses, falling back to the archived facelessfinder
breakouts when no credentials exist.

search.list costs one of the 100 daily calls; videos.list and channels.list
cost 1 unit each. One run spends 3 search calls and about 4 units.

Output: state/signals/YYYY-MM-DD.json with rows of
  {title, video_id, channel, subscribers, views, days, views_per_day, views_per_sub, url}
sorted by views_per_sub (a crude breakout score: views relative to audience size).
"""
import sys
from datetime import datetime, timedelta, timezone

from .common import STATE, config, load_json, now_iso, save_json, today


def _search(q, published_after, tok):
    import requests

    r = requests.get("https://www.googleapis.com/youtube/v3/search", headers={"Authorization": f"Bearer {tok}"},
                     params={"part": "snippet", "q": q, "type": "video", "videoDuration": "medium", "order": "viewCount",
                             "publishedAfter": published_after, "maxResults": 25, "relevanceLanguage": "en", "regionCode": "US"}, timeout=30)
    r.raise_for_status()
    return r.json().get("items", [])


def _batch(url, ids, part, tok):
    import requests

    out = {}
    for i in range(0, len(ids), 50):
        r = requests.get(url, headers={"Authorization": f"Bearer {tok}"}, params={"part": part, "id": ",".join(ids[i:i + 50]), "maxResults": 50}, timeout=30)
        r.raise_for_status()
        for it in r.json().get("items", []):
            out[it["id"]] = it
    return out


def from_youtube(queries, days=30, max_subs=300_000):
    from .youtube import access_token

    tok = access_token()
    after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = []
    for q in queries:
        items += _search(q, after, tok)
    vids = list({i["id"]["videoId"] for i in items})
    vinfo = _batch("https://www.googleapis.com/youtube/v3/videos", vids, "statistics,snippet,contentDetails", tok)
    chans = list({v["snippet"]["channelId"] for v in vinfo.values()})
    cinfo = _batch("https://www.googleapis.com/youtube/v3/channels", chans, "statistics", tok)
    rows = []
    for vid, v in vinfo.items():
        subs = int(cinfo.get(v["snippet"]["channelId"], {}).get("statistics", {}).get("subscriberCount", 0) or 0)
        if subs > max_subs or subs == 0:
            continue
        views = int(v["statistics"].get("viewCount", 0))
        pub = datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        age = max(1, (datetime.now(timezone.utc) - pub).days)
        rows.append({"title": v["snippet"]["title"], "video_id": vid, "channel": v["snippet"]["channelTitle"], "subscribers": subs,
                     "views": views, "days": age, "views_per_day": round(views / age), "views_per_sub": round(views / subs, 2),
                     "duration": v["contentDetails"]["duration"], "url": f"https://youtu.be/{vid}"})
    rows.sort(key=lambda r: r["views_per_sub"], reverse=True)
    return rows


def from_facelessfinder(niche_names):
    rep = load_json(STATE / "ff" / "latest.json")
    if not rep:
        return []
    rows = []
    for n in rep["niches"]:
        if n["name"] not in niche_names:
            continue
        for b in n["breakouts"]:
            if b["is_short"]:
                continue
            rows.append({"title": b["title"], "video_id": b["video_id"], "channel": b["channel"], "subscribers": None, "views": b["views"],
                         "days": b["age_days"], "views_per_day": round(b["views"] / max(1, b["age_days"] or 1)) if b["views"] else None,
                         "views_per_sub": None, "multiplier": b["multiplier"], "niche": n["name"], "url": b["url"]})
    rows.sort(key=lambda r: r.get("multiplier") or 0, reverse=True)
    return rows


def main(argv):
    import os

    cfg = config()
    niche = cfg["niche"]["primary"]
    queries = [niche.replace("&", "and")] + [f"{t} explained" for t in cfg["niche"].get("operator_expertise", [])[:2]]
    if all(os.environ.get(k) for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")):
        rows = from_youtube(queries)
        source = "youtube-data-api"
    else:
        rows = from_facelessfinder([niche] + cfg["niche"].get("backups", []))
        source = "facelessfinder-archive"
        rep = load_json(STATE / "ff" / "latest.json") or {}
        if rep.get("staleness", {}).get("stale"):
            print(f"WARNING: signals come from a stale facelessfinder edition (week of {rep.get('week_of')}); set YouTube credentials or use the vidIQ connector for live signals", file=sys.stderr)
    out = {"computed_at": now_iso(), "source": source, "queries": queries, "rows": rows}
    save_json(STATE / "signals" / f"{today()}.json", out)
    print(f"{len(rows)} signal rows from {source} -> state/signals/{today()}.json")
    for r in rows[:15]:
        print(f"  {r['views_per_sub'] if r['views_per_sub'] is not None else r.get('multiplier')!s:>8}  {r['views']!s:>9} views  {r['title'][:80]}  ({r['channel']})")


if __name__ == "__main__":
    main(sys.argv[1:])
