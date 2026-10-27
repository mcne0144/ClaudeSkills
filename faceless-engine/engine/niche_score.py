"""Rank the facelessfinder niches for THIS operator and THIS policy climate.

Inputs: state/ff/latest.json (and history for trend), config.json weights.
Output: state/niche_board.json and a markdown table on stdout.

Score = weighted sum of normalized rpm tier, rising index, outliers, cpc, seed
demand and (inverse) effort, plus a fit bonus for niches that overlap the
operator's expertise, minus a policy penalty for niches where an AI-narrated
channel gives advice on finance, health or legal matters (see docs/POLICY.md),
minus a shelf-life penalty for pure news niches. Trend across archived weeks
is reported, not scored, until there are at least three weeks of data.
"""
import re
import sys

from .common import STATE, config, load_json, now_iso, save_json
from .ff_report import history

SENSITIVE = re.compile(r"crypto|stock|finance|side hustle|money|longevity|health|weight loss|fitness|legal|law", re.I)
NEWSY = re.compile(r"news|recap", re.I)
RPM_SCORE = {"HIGH": 1.0, "MID": 0.5, "LOW": 0.1, None: 0.3}
EFFORT_SCORE = {"low": 1.0, "mid": 0.6, "high": 0.2, None: 0.5}


def _norm(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return lambda v: 0.0
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return lambda v: 0.5 if v is not None else 0.0
    return lambda v: (v - lo) / (hi - lo) if v is not None else 0.0


def score(report, cfg=None, weeks=None):
    cfg = cfg or config()
    w = cfg["niche_scoring"]["weights"]
    fit_terms = [t.lower() for t in cfg["niche"].get("operator_expertise", [])]
    avoid = set(cfg["niche"].get("avoid", []))
    niches = report["niches"]
    n_rising = _norm([n["rising"] for n in niches])
    n_out = _norm([n["outliers"] for n in niches])
    n_cpc = _norm([n["cpc"] for n in niches])
    n_seed = _norm([n["seed_demand_per_month"] for n in niches])
    trend = {}
    if weeks and len(weeks) >= 2:
        prev = {n["name"]: n for n in weeks[-2]["niches"]}
        for n in niches:
            p = prev.get(n["name"])
            if p and p["rising"] is not None and n["rising"] is not None:
                trend[n["name"]] = round(n["rising"] - p["rising"], 2)
    rows = []
    for n in niches:
        base = (
            w["rpm_tier"] * RPM_SCORE.get(n["rpm_tier"], 0.3)
            + w["rising"] * n_rising(n["rising"])
            + w["outliers"] * n_out(n["outliers"])
            + w["cpc"] * n_cpc(n["cpc"])
            + w["seed_demand"] * n_seed(n["seed_demand_per_month"])
            + w["effort"] * EFFORT_SCORE.get(n["effort"], 0.5)
        )
        flags = []
        name_l = n["name"].lower()
        fit = any(t in name_l for t in fit_terms)
        if fit:
            base += cfg["niche_scoring"]["fit_bonus"]
            flags.append("fit")
        policy = bool(SENSITIVE.search(n["name"])) or n["name"] in avoid
        if policy:
            base -= cfg["niche_scoring"]["policy_penalty"]
            flags.append("policy-risk")
        if NEWSY.search(n["name"]):
            base -= cfg["niche_scoring"]["shelf_life_penalty_for_news"]
            flags.append("short-shelf-life")
        rows.append({
            "name": n["name"], "ff_rank": n["rank"], "score": round(base, 3),
            "rpm_tier": n["rpm_tier"], "effort": n["effort"], "rising": n["rising"],
            "outliers": n["outliers"], "cpc": n["cpc"], "seed_demand_per_month": n["seed_demand_per_month"],
            "rising_delta_vs_prev_week": trend.get(n["name"]), "flags": flags,
            "breakout_titles": [b["title"] for b in n["breakouts"][:5]],
        })
    rows.sort(key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return {"computed_at": now_iso(), "week_of": report.get("week_of"), "weeks_of_history": len(weeks or []), "rows": rows}


def markdown(board, top=15):
    lines = [f"Niche board for week of {board['week_of']} (history: {board['weeks_of_history']} weeks)", "",
             "| # | Niche | Score | RPM | Effort | Rising | Outliers | CPC | Seed/mo | Flags |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in board["rows"][:top]:
        lines.append(f"| {r['rank']} | {r['name']} | {r['score']:.2f} | {r['rpm_tier']} | {r['effort']} | {r['rising']} | {r['outliers']} | {r['cpc']} | {r['seed_demand_per_month']} | {', '.join(r['flags'])} |")
    return "\n".join(lines)


def main(argv):
    report = load_json(STATE / "ff" / "latest.json")
    if not report:
        print("no report; run scan first", file=sys.stderr)
        sys.exit(2)
    board = score(report, weeks=history())
    save_json(STATE / "niche_board.json", board)
    print(markdown(board))


if __name__ == "__main__":
    main(sys.argv[1:])
