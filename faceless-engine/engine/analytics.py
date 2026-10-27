"""Measure published videos, keep learnings, write the weekly report, and show
progress against the revenue target.

Snapshots go into each video record's `metrics` list. Learnings aggregate in
state/learnings.json: title patterns, hook styles and topic kinds ranked by
average view percentage and views per day, so the weekly routine can bias
the next slate toward what this channel's audience actually watches.
"""
import json
import re
import statistics
import sys
from datetime import date, datetime, timedelta

from .common import REPORTS, STATE, config, load_json, now_iso, save_json, today
from . import ledger

PATTERNS = {
    "why": re.compile(r"^why\b", re.I), "how": re.compile(r"^how\b", re.I), "what_happened": re.compile(r"what (happened|actually)", re.I),
    "number": re.compile(r"\b\d+\b"), "question": re.compile(r"\?$"), "vs": re.compile(r"\bvs\.?\b", re.I),
    "i_tested": re.compile(r"\bI (tested|tried|ran|built)\b", re.I), "nobody": re.compile(r"nobody|no one|secret|hidden", re.I),
}


def title_patterns(title):
    return [k for k, rx in PATTERNS.items() if rx.search(title or "")]


def measure(cfg=None, monetary=None):
    from . import youtube

    cfg = cfg or config()
    recs = [r for r in ledger.all_records() if r.get("youtube", {}).get("video_id") and r["status"] in ("uploaded", "published", "measured")]
    if not recs:
        print("nothing to measure")
        return []
    ids = [r["youtube"]["video_id"] for r in recs]
    stats = youtube.video_stats(ids)
    end = today()
    start = (date.today() - timedelta(days=28)).isoformat()
    rows = {}
    try:
        for row in youtube.analytics(start, end, monetary=bool(monetary)):
            rows[row["video"]] = row
    except SystemExit as e:
        print(f"analytics unavailable ({e}); keeping public stats only", file=sys.stderr)
    out = []
    for r in recs:
        yid = r["youtube"]["video_id"]
        v = stats.get(yid, {})
        st = v.get("statistics", {})
        status = v.get("status", {})
        pub_at = v.get("snippet", {}).get("publishedAt")
        snap = {"at": now_iso(), "views": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0)), "comments": int(st.get("commentCount", 0)),
                "privacy": status.get("privacyStatus"), "analytics_28d": rows.get(yid)}
        r["metrics"].append(snap)
        if status.get("privacyStatus") == "public" and r["status"] == "uploaded":
            ledger.set_status(r, "published", f"public since {pub_at}")
        elif r["status"] in ("published", "measured") and len(r["metrics"]) >= 2:
            ledger.set_status(r, "measured", "snapshot") if r["status"] == "published" else ledger.save(r)
        else:
            ledger.save(r)
        out.append((r["id"], snap["views"], (rows.get(yid) or {}).get("averageViewPercentage")))
    update_learnings(cfg)
    for vid, views, avp in out:
        print(f"{vid:<60} views={views:<8} avg_view_pct={avp}")
    return out


def update_learnings(cfg=None):
    recs = [r for r in ledger.all_records() if r.get("metrics")]
    buckets = {}
    for r in recs:
        last = r["metrics"][-1]
        a = last.get("analytics_28d") or {}
        avp = a.get("averageViewPercentage")
        views = last.get("views", 0)
        pub = r.get("youtube", {}).get("publish_at")
        days = max(1, (datetime.utcnow() - datetime.strptime(pub[:10], "%Y-%m-%d")).days) if pub else 1
        vpd = views / days
        keys = [f"pattern:{p}" for p in title_patterns(r.get("title") or r["working_title"])] + [f"kind:{r.get('kind')}", f"niche:{r.get('niche')}"]
        for k in keys:
            b = buckets.setdefault(k, {"n": 0, "views_per_day": [], "avg_view_pct": []})
            b["n"] += 1
            b["views_per_day"].append(vpd)
            if avp is not None:
                b["avg_view_pct"].append(float(avp))
    learn = {"updated_at": now_iso(), "videos_measured": len(recs), "buckets": {}}
    for k, b in buckets.items():
        learn["buckets"][k] = {"n": b["n"], "views_per_day_median": round(statistics.median(b["views_per_day"]), 1),
                              "avg_view_pct_median": round(statistics.median(b["avg_view_pct"]), 1) if b["avg_view_pct"] else None}
    ranked = sorted(learn["buckets"].items(), key=lambda kv: kv[1]["views_per_day_median"], reverse=True)
    learn["ranked"] = [k for k, _ in ranked]
    save_json(STATE / "learnings.json", learn)
    return learn


def progress(cfg=None):
    cfg = cfg or config()
    t = cfg["targets"]
    recs = [r for r in ledger.all_records() if r.get("metrics")]
    total_views_28d = 0
    revenue_28d = 0.0
    have_revenue = False
    for r in recs:
        a = (r["metrics"][-1].get("analytics_28d") or {})
        total_views_28d += int(a.get("views", 0) or 0)
        if a.get("estimatedRevenue") is not None:
            have_revenue = True
            revenue_28d += float(a["estimatedRevenue"])
    lines = [f"Target: ${t['monthly_ad_revenue_usd']:,} per month in ad revenue", ""]
    rpm = t["assumed_rpm_usd"]
    lines.append(f"Assumed long-form RPM (source: {t['assumed_rpm_source']}): low ${rpm['low']}, mid ${rpm['mid']}, high ${rpm['high']}")
    for k, v in rpm.items():
        lines.append(f"  at ${v} RPM the target needs {int(t['monthly_ad_revenue_usd'] / v * 1000):,} monetized views per month ({k})")
    lines.append("")
    lines.append(f"Published videos with metrics: {len(recs)}")
    lines.append(f"Views in the last 28 days (Analytics API): {total_views_28d:,}")
    if have_revenue:
        observed = revenue_28d / total_views_28d * 1000 if total_views_28d else 0
        lines.append(f"Estimated revenue, last 28 days: ${revenue_28d:,.2f} (observed RPM ${observed:.2f})")
        if observed:
            lines.append(f"At the observed RPM the target needs {int(t['monthly_ad_revenue_usd'] / observed * 1000):,} views per month")
    else:
        lines.append("Revenue: not available until the channel is in the Partner Program (docs/POLICY.md thresholds)")
    return "\n".join(lines)


def weekly_report(cfg=None):
    cfg = cfg or config()
    learn = load_json(STATE / "learnings.json", {})
    recs = ledger.all_records()
    week = date.today().isocalendar()
    path = REPORTS / f"weekly-{week[0]}-W{week[1]:02}.md"
    lines = [f"# Weekly report, {today()}", "", "## Pipeline", "", "```", ledger.board(), "```", "", "## Progress", "", "```", progress(cfg), "```", ""]
    measured = [r for r in recs if r.get("metrics")]
    if measured:
        lines += ["## Videos, last snapshot", "", "| Video | Title | Views | Avg view % | Views/day |", "|---|---|---|---|---|"]
        for r in sorted(measured, key=lambda r: r["metrics"][-1].get("views", 0), reverse=True):
            m = r["metrics"][-1]
            a = m.get("analytics_28d") or {}
            pub = r.get("youtube", {}).get("publish_at", "")[:10]
            days = max(1, (date.today() - date.fromisoformat(pub)).days) if pub else 1
            lines.append(f"| {r['id']} | {r.get('title') or r['working_title']} | {m.get('views', 0)} | {a.get('averageViewPercentage', '')} | {m.get('views', 0) / days:.0f} |")
        lines.append("")
    if learn.get("buckets"):
        lines += ["## What is working (median views per day by title pattern, kind and niche)", "", "| Bucket | n | Views/day median | Avg view % median |", "|---|---|---|---|"]
        for k in learn["ranked"][:12]:
            b = learn["buckets"][k]
            lines.append(f"| {k} | {b['n']} | {b['views_per_day_median']} | {b['avg_view_pct_median']} |")
        lines.append("")
    lines += ["## Notes for the next slate", "", "- Fill in by the weekly review routine: which hooks held past 30 seconds, which titles earned clicks, what to stop.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))
    print(f"wrote {path}")
    return path
