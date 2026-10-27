"""Fetch and parse the facelessfinder.com weekly niche briefing.

The report is server-rendered HTML. Each niche is an <li> holding a <details>
block: name, RPM tier, effort, the three metrics (rising, outliers, cpc), a line
with freshness and seed demand, and a list of breakout videos with multipliers.

Usage:
  python faceless.py scan                 # fetch, parse, archive to state/ff/
  python faceless.py scan --file x.html   # parse a saved page
"""
import html as html_lib
import re
import sys
from pathlib import Path

from .common import STATE, human_number, load_json, now_iso, save_json

REPORT_URL = "https://www.facelessfinder.com/report"
UA = "Mozilla/5.0 (compatible; faceless-engine/1.0; +https://github.com/mcne0144/ClaudeSkills)"

_TAG = re.compile(r"<[^>]+>")


def _text(fragment):
    return html_lib.unescape(_TAG.sub("", fragment)).strip()


def fetch(url=REPORT_URL, timeout=30):
    import requests  # local import so parsing works without network deps

    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    r.raise_for_status()
    return r.text


def parse_age_days(token):
    m = re.match(r"^(\d+)\s*([dwmy])$", token.strip())
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    return n * {"d": 1, "w": 7, "m": 30, "y": 365}[unit]


def parse_breakout(li):
    mult = re.search(r">([0-9.]+)x<", li)
    href = re.search(r'href="([^"]+)"', li)
    if not href:
        return None
    anchor = re.search(r"<a [^>]*>(.*?)</a>", li, re.S)
    body = anchor.group(1) if anchor else ""
    meta = re.search(r"<span[^>]*>(.*?)</span>", body, re.S)
    title = _text(body[: meta.start()] if meta else body)
    parts = [p.strip() for p in _text(meta.group(1)).split("·")] if meta else []
    parts = [p for p in parts if p]
    channel = views = age = None
    is_short = False
    for p in parts:
        if p.upper() == "SHORTS":
            is_short = True
        elif p.endswith("views"):
            views = human_number(p[:-5])
        elif parse_age_days(p) is not None:
            age = parse_age_days(p)
        elif channel is None:
            channel = p
    url = html_lib.unescape(href.group(1))
    vid = re.search(r"[?&]v=([A-Za-z0-9_-]{6,})", url)
    return {
        "multiplier": float(mult.group(1)) if mult else None,
        "url": url,
        "video_id": vid.group(1) if vid else None,
        "title": title,
        "channel": channel,
        "views": views,
        "age_days": age,
        "is_short": is_short,
    }


def parse_html(page):
    page = page.replace("<!-- -->", "")
    out = {"source": REPORT_URL, "fetched_at": now_iso(), "niches": []}
    m = re.search(r"WEEK OF\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", page)
    out["week_of"] = m.group(1) if m else None
    m = re.search(r">([0-9.,KkMm]+)\s*VIDEOS SCANNED<", page)
    out["videos_scanned"] = human_number(m.group(1)) if m else None
    m = re.search(r">([0-9,]+)\s*NICHES TRACKED<", page)
    out["niches_tracked"] = int(m.group(1).replace(",", "")) if m else None
    m = re.search(r"STATUS:\s*([A-Z ]+)<", page)
    out["status"] = m.group(1).strip() if m else None

    ol = re.search(r"<ol[^>]*>(.*)</ol>", page, re.S)
    body = ol.group(1) if ol else page
    blocks = re.split(r'<li class="border border-line bg-panel-2">', body)[1:]
    for rank, block in enumerate(blocks, 1):
        name = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        rpm = re.search(r">(HIGH|MID|LOW) RPM<", block)
        effort = re.search(r">(low|mid|high)\s*effort<", block)
        metrics = dict(re.findall(r"<dt[^>]*>(\w+)</dt><dd[^>]*>([^<]*)</dd>", block))
        fresh = re.search(r"freshness\s*([0-9.]+)\s*%", block)
        seed = re.search(r"seed demand\s*([0-9.]+[KkMm]?)\s*/mo", block)
        ul = re.search(r"<ul[^>]*>(.*?)</ul>", block, re.S)
        items = re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S) if ul else []
        breakouts = [b for b in (parse_breakout(i) for i in items) if b]
        cpc = metrics.get("cpc", "").replace("$", "").strip()
        out["niches"].append({
            "rank": rank,
            "name": _text(name.group(1)) if name else f"niche-{rank}",
            "rpm_tier": rpm.group(1) if rpm else None,
            "effort": effort.group(1) if effort else None,
            "rising": float(metrics["rising"]) if metrics.get("rising") else None,
            "outliers": int(metrics["outliers"]) if metrics.get("outliers", "").isdigit() else None,
            "cpc": float(cpc) if cpc else None,
            "freshness_pct": float(fresh.group(1)) if fresh else None,
            "seed_demand_per_month": human_number(seed.group(1)) if seed else None,
            "breakouts": breakouts,
        })
    return out


STALE_AFTER_DAYS = 14


def staleness(report, reference=None):
    """Days since the report's week_of, and whether that exceeds STALE_AFTER_DAYS."""
    from datetime import date, datetime

    if not report.get("week_of"):
        return {"days": None, "stale": True, "reason": "no week_of parsed"}
    week = datetime.strptime(report["week_of"], "%Y-%m-%d").date()
    ref = reference or date.today()
    days = (ref - week).days
    return {"days": days, "stale": days > STALE_AFTER_DAYS,
            "reason": f"week_of {report['week_of']} is {days} days old" if days > STALE_AFTER_DAYS else "fresh"}


def archive(report):
    week = report.get("week_of") or "unknown"
    save_json(STATE / "ff" / f"{week}.json", report)
    save_json(STATE / "ff" / "latest.json", report)
    return STATE / "ff" / f"{week}.json"


def history():
    """All archived weeks, oldest first."""
    files = sorted(p for p in (STATE / "ff").glob("*.json") if p.name != "latest.json")
    return [load_json(p) for p in files]


def main(argv):
    url = REPORT_URL
    file = None
    for i, a in enumerate(argv):
        if a == "--file":
            file = argv[i + 1]
        if a == "--url":
            url = argv[i + 1]
    page = Path(file).read_text() if file else fetch(url)
    report = parse_html(page)
    if not report["niches"]:
        print("ERROR: parsed zero niches; the page layout may have changed. Saved raw page to state/ff/unparsed.html", file=sys.stderr)
        (STATE / "ff").mkdir(parents=True, exist_ok=True)
        (STATE / "ff" / "unparsed.html").write_text(page)
        sys.exit(3)
    path = archive(report)
    st = staleness(report)
    report["staleness"] = st
    save_json(path, report)
    save_json(STATE / "ff" / "latest.json", report)
    print(f"week_of={report['week_of']} niches={len(report['niches'])} saved={path.relative_to(STATE.parent)} stale={st['stale']} ({st['reason']})")
    if st["stale"]:
        print("STALE_REPORT: use the facelessfinder taxonomy and tiers for niche selection only; take topics from vidIQ outliers and rising keywords.")
    for n in report["niches"][:10]:
        print(f"  {n['rank']:>2}. {n['name']:<36} {n['rpm_tier'] or '?':<4} {n['effort'] or '?':<4} rising={n['rising']} outliers={n['outliers']} cpc={n['cpc']}")


if __name__ == "__main__":
    main(sys.argv[1:])
