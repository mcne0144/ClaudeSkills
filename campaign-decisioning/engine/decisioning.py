#!/usr/bin/env python3
"""
Campaign Decisioning engine.

A local, dependency-free reproduction of the Hightouch AI Decisioning loop:
collect inputs, decide, deliver (as a send plan), measure, learn.

Verbs (run `python3 decisioning.py <verb> --help` for flags):

  init       scaffold a campaign folder from the template
  validate   check a campaign.json before anything runs
  assign     deterministic treatment / holdout / customer_managed assignment
  run        one decisioning cycle: eligibility, guardrails, suppression,
             Thompson sampling, offer-aware expected value, send plan export
  outcomes   ingest outcome events, attribute them to decisions, update the model
  report     lift vs holdout with confidence intervals, creative performance,
             timing heatmap, personalization matrix, recommendations
  inspect    explain the latest decision (or non-decision) for one user
  simulate   synthetic audience and outcomes so a campaign can be dry-run

Everything the engine writes lives under the campaign folder:

  campaign.json          the spec (you edit this)
  audience.csv           one row per user, user_id plus any feature columns
  state/assignments.csv  user_id, bucket, group, first_seen_at, last_seen_at
  state/decisions.csv    every decision ever made (one row per send or skip)
  state/outcomes.csv     every ingested event, with the decision it attributed to
  state/model.json       Beta posteriors per arm and per context
  out/<run_id>/          send plans per channel plus audience exports
  reports/<date>.md      the report, plus a .json twin

Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone, date, time
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

GROUPS = ("treatment", "holdout", "customer_managed")

# Hightouch goal classifications and the reward each carries into the model.
# Positive classes add to successes, negative classes add to failures.
CLASS_REWARD = {
    "best": 1.0,
    "very_good": 0.6,
    "good": 0.3,
    "bad": -0.3,
    "very_bad": -0.6,
    "worst": -1.0,
}

DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# ----------------------------------------------------------------------------
# small utilities
# ----------------------------------------------------------------------------


def die(msg: str, code: int = 2) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(value: str | None, default: datetime | None = None) -> datetime | None:
    if value is None or value == "":
        return default
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%Y %H:%M"):
            try:
                dt = datetime.strptime(v, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"unrecognized timestamp: {value}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        seen: dict[str, None] = {}
        for r in rows:
            for k in r:
                seen.setdefault(k, None)
        fieldnames = list(seen)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def append_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")


def to_float(v, default=0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def truthy(v) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "y", "t")


# ----------------------------------------------------------------------------
# campaign spec
# ----------------------------------------------------------------------------


class Campaign:
    def __init__(self, folder: Path):
        self.folder = folder
        self.spec_path = folder / "campaign.json"
        self.spec = load_json(self.spec_path)
        if self.spec is None:
            die(f"no campaign.json in {folder}")
        self.state = folder / "state"
        self.out = folder / "out"
        self.reports = folder / "reports"
        self.state.mkdir(parents=True, exist_ok=True)

    # -- accessors --------------------------------------------------------
    @property
    def name(self) -> str:
        return self.spec.get("name", self.folder.name)

    @property
    def mode(self) -> str:
        return self.spec.get("mode", "lifecycle")

    @property
    def uid(self) -> str:
        return self.spec.get("user_id_field", "user_id")

    @property
    def features(self) -> list[str]:
        return list(self.spec.get("features", []))

    @property
    def goals(self) -> list[dict]:
        return list(self.spec.get("goals", []))

    @property
    def messages(self) -> list[dict]:
        return [m for m in self.spec.get("messages", []) if m.get("enabled", True)]

    @property
    def channels(self) -> dict[str, dict]:
        return {c["name"]: c for c in self.spec.get("channels", [])}

    @property
    def offers(self) -> dict[str, dict]:
        return {o["id"]: o for o in self.spec.get("offers", [])}

    @property
    def experiment(self) -> dict:
        return self.spec.get("experiment", {})

    @property
    def scheduling(self) -> dict:
        return self.spec.get("scheduling", {})

    @property
    def suppression(self) -> dict:
        return self.spec.get("smart_suppression", {"enabled": False})

    def best_goal(self) -> dict | None:
        for g in self.goals:
            if g.get("classification") == "best" and g.get("decisioning", True):
                return g
        return self.goals[0] if self.goals else None

    def audience_path(self) -> Path:
        src = self.spec.get("audience", {})
        p = src.get("path", "audience.csv")
        return (self.folder / p) if not os.path.isabs(p) else Path(p)

    def load_audience(self) -> list[dict]:
        rows = read_csv(self.audience_path())
        filt = self.spec.get("audience", {}).get("filter", [])
        if filt:
            rows = [r for r in rows if eligible(r, filt)]
        return rows

    def user_tz(self, user: dict):
        tz_field = self.scheduling.get("timezone_field")
        fallback = self.scheduling.get("fallback_timezone", "America/Los_Angeles")
        name = (user.get(tz_field) if tz_field else None) or fallback
        if ZoneInfo is None:
            return timezone.utc
        try:
            return ZoneInfo(name)
        except Exception:
            try:
                return ZoneInfo(fallback)
            except Exception:
                return timezone.utc


# ----------------------------------------------------------------------------
# eligibility rules
# ----------------------------------------------------------------------------


def eligible(row: dict, rules: list[dict]) -> bool:
    """All rules must pass. Rule: {field, op, value}.
    ops: eq, ne, gt, gte, lt, lte, in, not_in, contains, exists, missing, true, false
    """
    for rule in rules or []:
        f = rule.get("field")
        op = rule.get("op", "eq")
        want = rule.get("value")
        have = row.get(f)
        if op == "exists":
            if have in (None, ""):
                return False
            continue
        if op == "missing":
            if have not in (None, ""):
                return False
            continue
        if op == "true":
            if not truthy(have):
                return False
            continue
        if op == "false":
            if truthy(have):
                return False
            continue
        if have is None:
            return False
        if op == "eq" and str(have) != str(want):
            return False
        if op == "ne" and str(have) == str(want):
            return False
        if op in ("gt", "gte", "lt", "lte"):
            a, b = to_float(have, float("nan")), to_float(want, float("nan"))
            if math.isnan(a) or math.isnan(b):
                return False
            if op == "gt" and not a > b:
                return False
            if op == "gte" and not a >= b:
                return False
            if op == "lt" and not a < b:
                return False
            if op == "lte" and not a <= b:
                return False
        if op == "in" and str(have) not in [str(x) for x in (want or [])]:
            return False
        if op == "not_in" and str(have) in [str(x) for x in (want or [])]:
            return False
        if op == "contains" and str(want) not in str(have):
            return False
    return True


# ----------------------------------------------------------------------------
# group assignment (deterministic hash, modulo 100, contiguous buckets)
# ----------------------------------------------------------------------------


def bucket_for(user_id: str, salt: str) -> int:
    h = hashlib.sha256(f"{user_id}|{salt}".encode("utf-8")).hexdigest()
    return int(h, 16) % 100


def group_for(bucket: int, holdout_pct: float, cm_pct: float) -> str:
    # 0..holdout-1 = holdout, next cm_pct = customer_managed, rest = treatment
    if bucket < holdout_pct:
        return "holdout"
    if bucket < holdout_pct + cm_pct:
        return "customer_managed"
    return "treatment"


def cmd_assign(c: Campaign, args) -> dict:
    exp = c.experiment
    salt = exp.get("salt") or c.name
    holdout = float(exp.get("holdout_pct", 20))
    cm = float(exp.get("customer_managed_pct", 0))
    ext_field = exp.get("external_group_field")
    audience = c.load_audience()
    path = c.state / "assignments.csv"
    existing = {r[c.uid]: r for r in read_csv(path)}
    ts = iso(args_now(args))
    counts = defaultdict(int)
    rows = []
    for u in audience:
        uid = u.get(c.uid)
        if not uid:
            continue
        prev = existing.get(uid)
        if prev:
            prev["last_seen_at"] = ts
            rows.append(prev)
            counts[prev["group"]] += 1
            continue
        if ext_field:
            grp = str(u.get(ext_field, "")).strip()
            if grp not in GROUPS:
                die(f"external group field {ext_field} for {uid} is {grp!r}; must be one of {GROUPS}")
            b = -1
        else:
            b = bucket_for(uid, salt)
            grp = group_for(b, holdout, cm)
        rows.append({c.uid: uid, "bucket": b, "group": grp, "first_seen_at": ts, "last_seen_at": ts})
        counts[grp] += 1
    # keep users who fell out of the audience (assignment is sticky)
    seen = {r[c.uid] for r in rows}
    for uid, r in existing.items():
        if uid not in seen:
            rows.append(r)
    write_csv(path, rows, [c.uid, "bucket", "group", "first_seen_at", "last_seen_at"])
    summary = {"assigned": len(audience), "groups": dict(counts), "salt": salt,
               "holdout_pct": holdout, "customer_managed_pct": cm}
    print(json.dumps(summary, indent=2))
    return summary


def load_assignments(c: Campaign) -> dict[str, str]:
    return {r[c.uid]: r["group"] for r in read_csv(c.state / "assignments.csv")}


# ----------------------------------------------------------------------------
# model: Beta posteriors per arm, per context, with shrinkage to the global arm
# ----------------------------------------------------------------------------


class Model:
    """arms[arm_key][context_key] = {"a": successes, "b": failures}
    context_key "*" is the pooled estimate every context shrinks toward."""

    def __init__(self, path: Path):
        self.path = path
        data = load_json(path, {"arms": {}, "version": 1})
        self.arms: dict[str, dict[str, dict]] = data.get("arms", {})

    def save(self):
        save_json(self.path, {"arms": self.arms, "version": 1})

    def cell(self, arm: str, ctx: str) -> dict:
        return self.arms.setdefault(arm, {}).setdefault(ctx, {"a": 0.0, "b": 0.0, "n": 0})

    def update(self, arm: str, ctx: str, reward: float, weight: float = 1.0):
        for key in (ctx, "*"):
            cell = self.cell(arm, key)
            if reward >= 0:
                cell["a"] += reward * weight
                cell["b"] += (1.0 - reward) * weight if reward < 1 else 0.0
            else:
                cell["b"] += (-reward) * weight
            cell["n"] += 1

    def reverse_failure(self, arm: str, ctx: str):
        """A decision marked 'no outcome' turned out to convert late: take the
        failure back before the success is added."""
        for key in (ctx, "*"):
            cell = self.cell(arm, key)
            cell["b"] = max(0.0, cell["b"] - 1.0)
            cell["n"] = max(0, cell["n"] - 1)

    def posterior(self, arm: str, ctx: str, prior_a=1.0, prior_b=1.0, k=10.0) -> tuple[float, float]:
        """Return (alpha, beta). The context cell is pooled with the global cell
        using strength k: with few context observations the global estimate
        dominates, with many the context estimate takes over."""
        g = self.arms.get(arm, {}).get("*", {"a": 0.0, "b": 0.0, "n": 0})
        cx = self.arms.get(arm, {}).get(ctx, {"a": 0.0, "b": 0.0, "n": 0})
        g_tot = g["a"] + g["b"]
        if g_tot > 0:
            g_mean = (g["a"] + prior_a) / (g_tot + prior_a + prior_b)
        else:
            g_mean = prior_a / (prior_a + prior_b)
        # pseudo-observations from the global estimate
        alpha = cx["a"] + prior_a + k * g_mean
        beta = cx["b"] + prior_b + k * (1 - g_mean)
        return alpha, beta

    def mean(self, arm: str, ctx: str) -> float:
        a, b = self.posterior(arm, ctx)
        return a / (a + b)

    def sample(self, arm: str, ctx: str, rng: random.Random) -> float:
        a, b = self.posterior(arm, ctx)
        return rng.betavariate(a, b)

    def stats(self, arm: str, ctx: str = "*") -> dict:
        cell = self.arms.get(arm, {}).get(ctx, {"a": 0.0, "b": 0.0, "n": 0})
        a, b = self.posterior(arm, ctx)
        return {"successes": round(cell["a"], 3), "failures": round(cell["b"], 3), "n": cell["n"],
                "mean": round(a / (a + b), 4)}


def context_key(c: Campaign, user: dict) -> str:
    if not c.features:
        return "*"
    return "|".join(f"{f}={user.get(f, '')}" for f in c.features)


# ----------------------------------------------------------------------------
# guardrails: send history, limits, windows
# ----------------------------------------------------------------------------


DECISION_FIELDS = [
    "decision_id", "run_id", "decided_at", "send_at", "user_id", "group", "context",
    "action", "message_id", "channel", "variants", "offer_id", "hour_bucket",
    "expected_value", "score", "reason", "matured_at", "outcome", "outcome_value",
]


def load_decisions(c: Campaign) -> list[dict]:
    return read_csv(c.state / "decisions.csv")


def sends_by_user(decisions: list[dict]) -> dict[str, list[dict]]:
    by = defaultdict(list)
    for d in decisions:
        if d.get("action") == "send":
            by[d["user_id"]].append(d)
    return by


def count_in_window(sends: list[dict], at: datetime, days: float, pred=lambda d: True) -> int:
    lo = at - timedelta(days=days)
    return sum(1 for d in sends if pred(d) and lo <= parse_ts(d["send_at"]) <= at)


def send_limit_ok(limit: dict | None, sends: list[dict], at: datetime, pred) -> tuple[bool, str]:
    if not limit or limit.get("type", "none") == "none":
        return True, ""
    t = limit.get("type")
    count = int(limit.get("count", 1))
    if t == "static":
        n = sum(1 for d in sends if pred(d))
        if n >= count:
            return False, f"static send limit {count} reached"
    elif t == "time_window":
        n = count_in_window(sends, at, float(limit.get("days", 30)), pred)
        if n >= count:
            return False, f"time window limit {count}/{limit.get('days', 30)}d reached"
    elif t == "min_between":
        # require N other messages since this one was last sent
        last_idx = None
        ordered = sorted(sends, key=lambda d: d["send_at"])
        for i, d in enumerate(ordered):
            if pred(d):
                last_idx = i
        if last_idx is not None and len(ordered) - 1 - last_idx < count:
            return False, f"needs {count} other messages in between"
    return True, ""


def in_timeline(tl: dict | None, at: datetime) -> bool:
    if not tl:
        return True
    start = parse_ts(tl.get("start")) if tl.get("start") else None
    end = parse_ts(tl.get("end")) if tl.get("end") else None
    if start and at < start:
        return False
    if end and at > end:
        return False
    return True


def allowed_hours(c: Campaign, msg: dict, channel: dict, local_day: str) -> list[int]:
    """Hours (0..23, user local) a message may send today after quiet hours,
    channel quiet hours and the message delivery window are applied."""
    hours = set(range(24))
    for qh in (c.scheduling.get("quiet_hours"), channel.get("quiet_hours")):
        if qh:
            s = int(str(qh.get("start", "21:00")).split(":")[0])
            e = int(str(qh.get("end", "08:00")).split(":")[0])
            if s > e:  # overnight
                hours -= set(range(s, 24)) | set(range(0, e))
            else:
                hours -= set(range(s, e))
    dw = msg.get("delivery_windows")
    if dw:
        days = [d.lower()[:3] for d in dw.get("days", DAY_NAMES)]
        if local_day not in days:
            return []
        if dw.get("hours"):
            win = set()
            for lo, hi in dw["hours"]:
                win |= set(range(int(lo), int(hi)))
            hours &= win
    return sorted(hours)


def hour_bucket(h: int) -> str:
    if h < 6:
        return "night"
    if h < 12:
        return "morning"
    if h < 17:
        return "afternoon"
    return "evening"


# ----------------------------------------------------------------------------
# run: the decisioning cycle
# ----------------------------------------------------------------------------


def args_now(args) -> datetime:
    return parse_ts(getattr(args, "now", None), now_utc())


def expected_value(c: Campaign, msg: dict, p: float) -> float:
    """value minus cost, weighted by conversion likelihood (Hightouch offers)."""
    goal = c.best_goal() or {}
    value = to_float(goal.get("value_per_conversion"), 1.0)
    offer = c.offers.get(msg.get("offer", ""), None)
    cost = 0.0
    if offer:
        cost += to_float(offer.get("cost_value"))
        cost += to_float(offer.get("cost_multiplier")) * value
    return p * (value - cost)


def choose_for_user(c: Campaign, user: dict, ctx: str, model: Model, sends: list[dict],
                    at: datetime, rng: random.Random, assignments_group: str) -> dict:
    """Return a decision dict for one treatment user."""
    uid = user[c.uid]
    local = at.astimezone(c.user_tz(user))
    local_day = DAY_NAMES[local.weekday()]
    reasons = []

    # agent-level frequency limit
    fl = c.scheduling.get("frequency_limit")
    if fl and count_in_window(sends, at, float(fl.get("per_days", 7))) >= int(fl.get("max_sends", 3)):
        return skip(uid, assignments_group, ctx, "agent frequency limit reached")
    # blackout days (compare in user local date)
    if local.date().isoformat() in set(c.scheduling.get("blackout_days", [])):
        return skip(uid, assignments_group, ctx, "blackout day")

    candidates = []
    for msg in c.messages:
        mid = msg["id"]
        ch = c.channels.get(msg.get("channel", ""), {})
        if not ch:
            reasons.append(f"{mid}: channel {msg.get('channel')} not configured")
            continue
        if not eligible(user, ch.get("eligibility", [])):
            reasons.append(f"{mid}: channel eligibility failed")
            continue
        if not in_timeline(msg.get("timeline"), at):
            reasons.append(f"{mid}: outside timeline")
            continue
        if not eligible(user, msg.get("eligibility", [])):
            reasons.append(f"{mid}: message eligibility failed")
            continue
        cap = ch.get("max_per_week")
        if cap and count_in_window(sends, at, 7, lambda d, n=ch.get("name"): d["channel"] == n) >= int(cap):
            reasons.append(f"{mid}: channel weekly cap")
            continue
        ok, why = send_limit_ok(msg.get("send_limit"), sends, at, lambda d, m=mid: d["message_id"] == m)
        if not ok:
            reasons.append(f"{mid}: {why}")
            continue
        hours = allowed_hours(c, msg, ch, local_day)
        if not hours:
            reasons.append(f"{mid}: no allowed hours today")
            continue
        # variants: for each optimized content type pick one eligible variant
        chosen_variants = {}
        variant_ok = True
        for ctype, variants in (msg.get("variants") or {}).items():
            elig = []
            for v in variants:
                if not eligible(user, v.get("eligibility", [])):
                    continue
                if not in_timeline(v.get("active"), at):
                    continue
                okv, _ = send_limit_ok(v.get("send_limit"), sends, at,
                                       lambda d, m=mid, ct=ctype, vid=v["id"]: d["message_id"] == m
                                       and f"{ct}={vid}" in (d.get("variants") or ""))
                if not okv:
                    continue
                elig.append(v)
            if not elig:
                variant_ok = False
                reasons.append(f"{mid}: no eligible {ctype} variant")
                break
            best_v, best_s = None, -1.0
            for v in elig:
                s = model.sample(f"variant:{mid}:{ctype}:{v['id']}", ctx, rng)
                if s > best_s:
                    best_v, best_s = v, s
            chosen_variants[ctype] = best_v["id"]
        if not variant_ok:
            continue
        p = model.sample(f"message:{mid}", ctx, rng)
        ev = expected_value(c, msg, p)
        # timing arm: pick the best-sampled allowed hour bucket
        buckets = sorted({hour_bucket(h) for h in hours})
        best_b, best_bs = None, -1.0
        for b in buckets:
            s = model.sample(f"timing:{msg.get('channel')}:{b}", ctx, rng)
            if s > best_bs:
                best_b, best_bs = b, s
        hour = min(h for h in hours if hour_bucket(h) == best_b)
        candidates.append({"msg": msg, "p": p, "ev": ev, "variants": chosen_variants,
                           "bucket": best_b, "hour": hour, "mean": model.mean(f"message:{mid}", ctx)})

    if not candidates:
        return skip(uid, assignments_group, ctx, "; ".join(reasons) or "no eligible message")

    best = max(candidates, key=lambda x: x["ev"])
    msg = best["msg"]
    send_local = local.replace(hour=best["hour"], minute=0, second=0, microsecond=0)
    if send_local < local:
        send_local = send_local + timedelta(days=1)
    vstr = ";".join(f"{k}={v}" for k, v in sorted(best["variants"].items()))
    return {
        "user_id": uid, "group": assignments_group, "context": ctx, "action": "send",
        "message_id": msg["id"], "channel": msg.get("channel"), "variants": vstr,
        "offer_id": msg.get("offer", ""), "hour_bucket": best["bucket"],
        "send_at": iso(send_local), "expected_value": round(best["ev"], 5),
        "score": round(best["mean"], 5), "reason": f"best expected value among {len(candidates)} eligible",
    }


def skip(uid: str, group: str, ctx: str, reason: str) -> dict:
    return {"user_id": uid, "group": group, "context": ctx, "action": "skip", "message_id": "",
            "channel": "", "variants": "", "offer_id": "", "hour_bucket": "", "send_at": "",
            "expected_value": 0.0, "score": 0.0, "reason": reason}


def apply_smart_suppression(c: Campaign, decisions: list[dict], sends_by: dict, at: datetime,
                            rng: random.Random) -> None:
    sup = c.suppression
    if not sup.get("enabled"):
        return
    top_pct = float(sup.get("send_to_top_pct", 80))
    min_p = float(sup.get("min_send_probability", 0.01))
    sends = [d for d in decisions if d["action"] == "send"]
    if len(sends) < 20:
        return  # too little to rank meaningfully
    # recency boost: the longer since the last send, the higher the score
    def adjusted(d):
        last = max((parse_ts(s["send_at"]) for s in sends_by.get(d["user_id"], [])), default=None)
        days = (at - last).days if last else 30
        return float(d["expected_value"]) * (1.0 + min(days, 30) / 30.0)
    ranked = sorted(sends, key=adjusted, reverse=True)
    keep = int(round(len(ranked) * top_pct / 100.0))
    for i, d in enumerate(ranked):
        if i < keep:
            continue
        # boundary users: soft cutoff, never below the minimum send probability
        dist = (i - keep) / max(1, len(ranked) - keep)
        p_send = max(min_p, 0.5 * (1 - dist))
        if rng.random() < p_send:
            continue
        d["action"] = "suppressed"
        d["reason"] = f"smart suppression (bottom {100 - top_pct:.0f}% by predicted impact)"
        d["send_at"] = ""


def cmd_run(c: Campaign, args) -> dict:
    at = args_now(args)
    run_id = at.strftime("%Y%m%dT%H%M%SZ")
    rng = random.Random(f"{c.name}|{run_id}|{args.seed}")
    assignments = load_assignments(c)
    if not assignments:
        die("no assignments yet; run `assign` first")
    model = Model(c.state / "model.json")
    audience = c.load_audience()
    decisions_prev = load_decisions(c)
    by_user = sends_by_user(decisions_prev)
    users_by_id = {u[c.uid]: u for u in audience}

    if c.mode == "paid_ads":
        return run_paid_ads(c, args, at, run_id, rng, assignments, model, audience)

    decisions = []
    counts = defaultdict(int)
    for u in audience:
        uid = u.get(c.uid)
        grp = assignments.get(uid)
        if not grp:
            continue
        ctx = context_key(c, u)
        if grp != "treatment":
            counts[f"{grp}_not_evaluated"] += 1
            continue  # holdout and customer_managed users are never evaluated; inspect shows their group
        d = choose_for_user(c, u, ctx, model, by_user.get(uid, []), at, rng, grp)
        decisions.append(d)
    apply_smart_suppression(c, decisions, by_user, at, rng)

    goal = c.best_goal() or {}
    attr_days = float(goal.get("attribution_days", 7))
    for i, d in enumerate(decisions):
        d["decision_id"] = f"{run_id}-{i:06d}"
        d["run_id"] = run_id
        d["decided_at"] = iso(at)
        d["matured_at"] = iso(parse_ts(d["send_at"]) + timedelta(days=attr_days)) if d["send_at"] else ""
        d["outcome"] = ""
        d["outcome_value"] = ""
        counts[d["action"]] += 1
    out = c.out / run_id
    out.mkdir(parents=True, exist_ok=True)
    skips = [d for d in decisions if d["action"] == "skip"]
    kept = [d for d in decisions if d["action"] != "skip"]
    append_csv(c.state / "decisions.csv", kept, DECISION_FIELDS)
    write_csv(out / "skips.csv", skips, ["user_id", "context", "reason"])
    (c.state / "latest_run").write_text(run_id, encoding="utf-8")

    # exports: one send plan per channel, plus audience lists per group
    plans = defaultdict(list)
    synced_cols = c.spec.get("synced_user_columns") or []
    for d in decisions:
        if d["action"] != "send":
            continue
        u = users_by_id.get(d["user_id"], {})
        msg = next((m for m in c.messages if m["id"] == d["message_id"]), {})
        row = {c.uid: d["user_id"], "send_at": d["send_at"], "message_id": d["message_id"],
               "message_name": msg.get("name", ""), "destination": msg.get("destination", ""),
               "destination_ref": msg.get("destination_ref", ""), "offer_id": d["offer_id"],
               "decision_id": d["decision_id"]}
        for ctype, variants in (msg.get("variants") or {}).items():
            vid = dict(kv.split("=", 1) for kv in d["variants"].split(";") if "=" in kv).get(ctype)
            v = next((x for x in variants if x["id"] == vid), {})
            row[ctype] = v.get("text", "")
        for col in synced_cols:
            row[col] = u.get(col, "")
        plans[d["channel"]].append(row)
    for ch, rows in plans.items():
        write_csv(out / f"sendplan_{ch}.csv", rows)
    for grp in GROUPS:
        ids = [{c.uid: uid} for uid, g in assignments.items() if g == grp and uid in users_by_id]
        write_csv(out / f"audience_{grp}.csv", ids, [c.uid])
    suppress_ids = [{c.uid: uid} for uid, g in assignments.items() if g in ("treatment", "holdout") and uid in users_by_id]
    write_csv(out / "suppress_from_customer_managed.csv", suppress_ids, [c.uid])

    summary = {"run_id": run_id, "decided_at": iso(at), "audience": len(audience),
               "decisions": dict(counts), "sends_by_channel": {k: len(v) for k, v in plans.items()},
               "out": str(out)}
    save_json(out / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return summary


# ----------------------------------------------------------------------------
# paid ads mode: segment x creative allocation
# ----------------------------------------------------------------------------


def run_paid_ads(c, args, at, run_id, rng, assignments, model, audience) -> dict:
    """Decisions are made per segment (context) rather than per user. The bandit
    arms are creatives; the output is a budget share per creative per segment
    (Thompson sampling with many draws) plus customer-list exports per group."""
    draws = int(c.spec.get("paid_ads", {}).get("draws", 2000))
    floor = float(c.spec.get("paid_ads", {}).get("min_share_pct", 5)) / 100.0
    segments = defaultdict(list)
    for u in audience:
        if assignments.get(u.get(c.uid)) == "treatment":
            segments[context_key(c, u)].append(u)
    rows = []
    decisions = []
    for seg, users in segments.items():
        sample_user = users[0]
        creatives = [m for m in c.messages if eligible(sample_user, m.get("eligibility", [])) and in_timeline(m.get("timeline"), at)]
        if not creatives:
            continue
        wins = defaultdict(int)
        for _ in range(draws):
            best, bs = None, -1.0
            for m in creatives:
                s = model.sample(f"message:{m['id']}", seg, rng) * (1.0 - to_float(c.offers.get(m.get("offer", ""), {}).get("cost_multiplier")))
                if s > bs:
                    best, bs = m, s
            wins[best["id"]] += 1
        shares = {mid: wins[mid] / draws for mid in [m["id"] for m in creatives]}
        # floor so every creative keeps exploring
        for mid in shares:
            shares[mid] = max(shares[mid], floor)
        tot = sum(shares.values())
        for m in creatives:
            share = shares[m["id"]] / tot
            rows.append({"segment": seg, "users": len(users), "creative_id": m["id"], "creative_name": m.get("name", ""),
                         "channel": m.get("channel", ""), "destination": m.get("destination", ""),
                         "destination_ref": m.get("destination_ref", ""), "budget_share": round(share, 4),
                         "posterior_mean": round(model.mean(f"message:{m['id']}", seg), 4)})
            decisions.append({"decision_id": f"{run_id}-{len(decisions):06d}", "run_id": run_id, "decided_at": iso(at),
                              "send_at": iso(at), "user_id": f"segment:{seg}", "group": "treatment", "context": seg,
                              "action": "allocate", "message_id": m["id"], "channel": m.get("channel", ""),
                              "variants": "", "offer_id": m.get("offer", ""), "hour_bucket": "",
                              "expected_value": round(share, 4), "score": round(model.mean(f"message:{m['id']}", seg), 4),
                              "reason": f"thompson allocation over {draws} draws", "matured_at": "", "outcome": "", "outcome_value": ""})
    append_csv(c.state / "decisions.csv", decisions, DECISION_FIELDS)
    out = c.out / run_id
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "creative_allocation.csv", rows)
    users_by_id = {u[c.uid]: u for u in audience}
    for grp in GROUPS:
        ids = [{c.uid: uid, **{f: users_by_id[uid].get(f, "") for f in c.features}} for uid, g in assignments.items() if g == grp and uid in users_by_id]
        write_csv(out / f"customer_list_{grp}.csv", ids, [c.uid] + c.features)
    summary = {"run_id": run_id, "mode": "paid_ads", "segments": len(segments), "allocations": len(rows), "out": str(out)}
    save_json(out / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return summary


# ----------------------------------------------------------------------------
# outcomes: attribute events, update posteriors
# ----------------------------------------------------------------------------


def goal_for_event(c: Campaign, event: dict) -> dict | None:
    for g in c.goals:
        if g.get("event") != event.get("event"):
            continue
        if eligible(event, g.get("filter", [])):
            return g
    return None


def cmd_outcomes(c: Campaign, args) -> dict:
    model = Model(c.state / "model.json")
    decisions = load_decisions(c)
    at = args_now(args)
    stats = defaultdict(int)

    if args.aggregate:
        # paid ads: segment,creative_id,impressions,conversions[,spend,revenue][,group]
        for r in read_csv(Path(args.aggregate)):
            seg = r.get("segment", "*")
            cid = r.get("creative_id")
            imp = to_float(r.get("impressions"))
            conv = to_float(r.get("conversions"))
            grp = r.get("group", "treatment")
            if grp == "treatment" and cid:
                cell = model.cell(f"message:{cid}", seg)
                cell["a"] += conv
                cell["b"] += max(0.0, imp - conv)
                cell["n"] += 1
                g = model.cell(f"message:{cid}", "*")
                g["a"] += conv
                g["b"] += max(0.0, imp - conv)
                g["n"] += 1
            append_csv(c.state / "aggregate_outcomes.csv",
                       [{**r, "ingested_at": iso(at)}],
                       ["segment", "creative_id", "group", "impressions", "conversions", "spend", "revenue", "ingested_at"])
            stats["rows"] += 1
        model.save()
        print(json.dumps(dict(stats), indent=2))
        return dict(stats)

    events = read_csv(Path(args.events))
    # index decisions by user, newest first
    by_user = defaultdict(list)
    for d in decisions:
        if d["action"] == "send":
            by_user[d["user_id"]].append(d)
    for lst in by_user.values():
        lst.sort(key=lambda d: d["send_at"], reverse=True)
    assignments = load_assignments(c)
    ingested_path = c.state / "outcomes.csv"
    already = {(r["user_id"], r["event"], r["timestamp"]) for r in read_csv(ingested_path)}
    out_rows = []
    for e in events:
        uid = e.get(c.uid) or e.get("user_id")
        if not uid:
            continue
        key = (uid, e.get("event", ""), e.get("timestamp", ""))
        if key in already:
            stats["duplicate"] += 1
            continue
        g = goal_for_event(c, e)
        if not g:
            stats["unmatched_goal"] += 1
            continue
        ts = parse_ts(e.get("timestamp"), at)
        value = to_float(e.get(g.get("weight_field", "value")), 1.0) if g.get("weight_field") else 1.0
        window = float(g.get("attribution_days", 7))
        attributed = None
        for d in by_user.get(uid, []):
            sent = parse_ts(d["send_at"])
            if sent <= ts <= sent + timedelta(days=window):
                attributed = d
                break
        reward = CLASS_REWARD.get(g.get("classification", "good"), 0.3)
        row = {"user_id": uid, "event": e.get("event"), "timestamp": iso(ts), "goal": g.get("name"),
               "classification": g.get("classification"), "value": value,
               "group": assignments.get(uid, ""), "decision_id": attributed["decision_id"] if attributed else "",
               "message_id": attributed["message_id"] if attributed else "", "ingested_at": iso(at)}
        out_rows.append(row)
        stats["ingested"] += 1
        if attributed and g.get("decisioning", True) and assignments.get(uid) == "treatment":
            ctx = attributed["context"]
            mid = attributed["message_id"]
            if reward > 0 and attributed.get("outcome") == "none":
                for arm in [f"message:{mid}"] + [f"variant:{mid}:{kv.split('=', 1)[0]}:{kv.split('=', 1)[1]}" for kv in (attributed.get("variants") or "").split(";") if "=" in kv] + ([f"timing:{attributed['channel']}:{attributed['hour_bucket']}"] if attributed.get("hour_bucket") else []):
                    model.reverse_failure(arm, ctx)
            model.update(f"message:{mid}", ctx, reward)
            for kv in (attributed.get("variants") or "").split(";"):
                if "=" in kv:
                    ct, vid = kv.split("=", 1)
                    model.update(f"variant:{mid}:{ct}:{vid}", ctx, reward)
            if attributed.get("hour_bucket"):
                model.update(f"timing:{attributed['channel']}:{attributed['hour_bucket']}", ctx, reward)
            if reward > 0:
                attributed["outcome"] = g.get("name")
                attributed["outcome_value"] = value
            stats["attributed"] += 1
        else:
            stats["unattributed"] += 1
    append_csv(ingested_path, out_rows, ["user_id", "event", "timestamp", "goal", "classification", "value",
                                         "group", "decision_id", "message_id", "ingested_at"])

    # matured decisions with no positive outcome count as a failure once
    matured_marked = 0
    for d in decisions:
        if d["action"] != "send" or d.get("outcome") or d.get("matured_at", "") == "":
            continue
        if d.get("outcome") == "":
            m_at = parse_ts(d["matured_at"])
            if m_at <= at and d.get("outcome") != "none":
                ctx = d["context"]
                mid = d["message_id"]
                model.update(f"message:{mid}", ctx, 0.0)
                for kv in (d.get("variants") or "").split(";"):
                    if "=" in kv:
                        ct, vid = kv.split("=", 1)
                        model.update(f"variant:{mid}:{ct}:{vid}", ctx, 0.0)
                if d.get("hour_bucket"):
                    model.update(f"timing:{d['channel']}:{d['hour_bucket']}", ctx, 0.0)
                d["outcome"] = "none"
                matured_marked += 1
    write_csv(c.state / "decisions.csv", decisions, DECISION_FIELDS)
    model.save()
    stats["matured_without_outcome"] = matured_marked
    print(json.dumps(dict(stats), indent=2))
    return dict(stats)


# ----------------------------------------------------------------------------
# report: lift, creative, timing, personalization, recommendations
# ----------------------------------------------------------------------------


def wilson(successes: float, n: float, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    adj = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((centre - adj) / denom, (centre + adj) / denom)


def two_prop_z(s1, n1, s2, n2) -> tuple[float, float]:
    """z statistic and two-sided p-value for p1 - p2."""
    if n1 <= 0 or n2 <= 0:
        return 0.0, 1.0
    p1, p2 = s1 / n1, s2 / n2
    p = (s1 + s2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2)) if 0 < p < 1 else 0.0
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    pval = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, pval


def newcombe_diff_ci(s1, n1, s2, n2, z=1.96) -> tuple[float, float]:
    l1, u1 = wilson(s1, n1, z)
    l2, u2 = wilson(s2, n2, z)
    p1 = s1 / n1 if n1 else 0.0
    p2 = s2 / n2 if n2 else 0.0
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return lo, hi


def pct(x: float) -> str:
    return f"{100 * x:.2f}%"


def report_paid_ads(c: Campaign, at: datetime) -> dict:
    assignments = load_assignments(c)
    audience = {u[c.uid]: u for u in c.load_audience()}
    model = Model(c.state / "model.json")
    agg = read_csv(c.state / "aggregate_outcomes.csv")
    groups = defaultdict(int)
    for uid, g in assignments.items():
        if uid in audience:
            groups[g] += 1
    lines = [f"# {c.name}: paid ads decisioning report", "", f"Generated {iso(at)}. Mode: paid_ads.", "",
             "## Experiment groups (customer lists)", "", "| Group | Users |", "|---|---|"]
    for g in GROUPS:
        lines.append(f"| {g} | {groups.get(g, 0)} |")
    report = {"campaign": c.name, "mode": "paid_ads", "generated_at": iso(at), "groups": dict(groups)}
    conv = defaultdict(float)
    imps = defaultdict(float)
    spend = defaultdict(float)
    rev = defaultdict(float)
    for r in agg:
        key = (r.get("segment", "*"), r.get("creative_id", ""), r.get("group", "treatment"))
        conv[key] += to_float(r.get("conversions"))
        imps[key] += to_float(r.get("impressions"))
        spend[key] += to_float(r.get("spend"))
        rev[key] += to_float(r.get("revenue"))
    # lift: conversions per user in treatment vs holdout, across all segments
    s_t = sum(v for (seg, cid, g), v in conv.items() if g == "treatment")
    s_h = sum(v for (seg, cid, g), v in conv.items() if g == "holdout")
    n_t, n_h = groups.get("treatment", 0), groups.get("holdout", 0)
    r_t = s_t / n_t if n_t else 0.0
    r_h = s_h / n_h if n_h else 0.0
    lo, hi = newcombe_diff_ci(min(s_t, n_t), n_t, min(s_h, n_h), n_h)
    z, p = two_prop_z(min(s_t, n_t), n_t, min(s_h, n_h), n_h)
    report["lift"] = {"treatment": {"users": n_t, "conversions": s_t, "rate": r_t}, "holdout": {"users": n_h, "conversions": s_h, "rate": r_h},
                      "abs_lift": r_t - r_h, "ci": (lo, hi), "p_value": p,
                      "spend_treatment": sum(v for (seg, cid, g), v in spend.items() if g == "treatment"),
                      "revenue_treatment": sum(v for (seg, cid, g), v in rev.items() if g == "treatment"),
                      "revenue_holdout": sum(v for (seg, cid, g), v in rev.items() if g == "holdout")}
    lines += ["", "## Lift vs holdout (conversions per list member)", "", "| Group | Users | Conversions | Rate |", "|---|---|---|---|",
              f"| treatment | {n_t} | {s_t:.0f} | {pct(r_t)} |", f"| holdout | {n_h} | {s_h:.0f} | {pct(r_h)} |", "",
              f"Absolute lift {pct(r_t - r_h)} (95% CI {pct(lo)} to {pct(hi)}). p = {p:.3f}. "
              + ("Holdout rows missing: add aggregate rows with group=holdout to measure lift." if n_h and s_h == 0 and not any(g == "holdout" for (_, _, g) in conv) else ""), ""]
    inc_rev = report["lift"]["revenue_treatment"] - report["lift"]["revenue_holdout"] * (n_t / n_h if n_h else 0)
    if report["lift"]["spend_treatment"]:
        lines += [f"Spend {report['lift']['spend_treatment']:.2f}. Incremental revenue (treatment minus holdout scaled to treatment size) {inc_rev:.2f}. Incremental ROAS {inc_rev / report['lift']['spend_treatment']:.2f}.", ""]
    # creative performance per segment
    lines += ["## Creative performance by segment", "", "| Segment | Creative | Impressions | Conv | Rate | 95% CI | Posterior | Spend | Revenue |", "|---|---|---|---|---|---|---|---|---|"]
    rows = []
    for (seg, cid, g), n in sorted(imps.items()):
        if g != "treatment" or not cid:
            continue
        k = (seg, cid, g)
        rate = conv[k] / n if n else 0.0
        ci = wilson(conv[k], n)
        rows.append({"segment": seg, "creative_id": cid, "impressions": n, "conversions": conv[k], "rate": rate, "ci": ci,
                     "posterior_mean": model.mean(f"message:{cid}", seg), "spend": spend[k], "revenue": rev[k]})
        lines.append(f"| {seg} | {cid} | {n:.0f} | {conv[k]:.0f} | {pct(rate)} | {pct(ci[0])} to {pct(ci[1])} | {pct(model.mean(f'message:{cid}', seg))} | {spend[k]:.2f} | {rev[k]:.2f} |")
    report["creative_performance"] = rows
    # latest allocation
    latest = (c.state / "latest_run").read_text(encoding="utf-8").strip() if (c.state / "latest_run").exists() else None
    if latest and (c.out / latest / "creative_allocation.csv").exists():
        alloc = read_csv(c.out / latest / "creative_allocation.csv")
        lines += ["", f"## Current budget allocation (run {latest})", "", "| Segment | Creative | Budget share | Posterior |", "|---|---|---|---|"]
        for r in alloc:
            lines.append(f"| {r['segment']} | {r['creative_name'] or r['creative_id']} | {100 * to_float(r['budget_share']):.1f}% | {pct(to_float(r['posterior_mean']))} |")
        report["allocation"] = alloc
    recs = []
    by_seg = defaultdict(list)
    for r in rows:
        by_seg[r["segment"]].append(r)
    for seg, rs in by_seg.items():
        rs.sort(key=lambda r: r["rate"], reverse=True)
        if len(rs) > 1 and rs[0]["impressions"] >= 2000 and rs[-1]["impressions"] >= 2000 and rs[-1]["ci"][1] < rs[0]["ci"][0]:
            recs.append(f"{seg}: retire or rework '{rs[-1]['creative_id']}' (upper bound {pct(rs[-1]['ci'][1])} is below the leader's lower bound {pct(rs[0]['ci'][0])}).")
    if not recs:
        recs.append("Not enough impressions per creative per segment for a confident call. Keep the minimum share floor so every creative keeps learning.")
    report["recommendations"] = recs
    lines += ["", "## Recommendations", ""] + [f"- {r}" for r in recs] + ["",
              "## How to read this", "", "Lift is conversions per list member in treatment against holdout, where the holdout list is excluded from every ad set. It is incrementality, not platform attribution. Posterior means pool each segment with the creative's global estimate.", ""]
    c.reports.mkdir(parents=True, exist_ok=True)
    stem = at.strftime("%Y-%m-%d")
    (c.reports / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")
    save_json(c.reports / f"{stem}.json", report)
    print("\n".join(lines))
    return report


def cmd_report(c: Campaign, args) -> dict:
    at = args_now(args)
    if c.mode == "paid_ads":
        return report_paid_ads(c, at)
    assignments_rows = read_csv(c.state / "assignments.csv")
    assignments = {r[c.uid]: r["group"] for r in assignments_rows}
    first_seen = {r[c.uid]: parse_ts(r["first_seen_at"]) for r in assignments_rows}
    decisions = load_decisions(c)
    outcomes = read_csv(c.state / "outcomes.csv")
    model = Model(c.state / "model.json")
    audience = {u[c.uid]: u for u in c.load_audience()}
    report: dict = {"campaign": c.name, "mode": c.mode, "generated_at": iso(at), "goals": []}
    lines = [f"# {c.name}: decisioning report", "", f"Generated {iso(at)}. Mode: {c.mode}.", ""]

    # eligible and group sizes
    groups = defaultdict(int)
    for uid, g in assignments.items():
        if uid in audience:
            groups[g] += 1
    report["groups"] = dict(groups)
    lines += ["## Experiment groups", "", "| Group | Users |", "|---|---|"]
    for g in GROUPS:
        lines.append(f"| {g} | {groups.get(g, 0)} |")
    lines.append("")

    # lift per goal: converters / users in group, among users assigned long enough to mature
    converters = defaultdict(set)
    value_by = defaultdict(float)
    for o in outcomes:
        if CLASS_REWARD.get(o.get("classification", ""), 0) > 0 or o.get("classification") in CLASS_REWARD:
            converters[(o["goal"], o["group"])].add(o["user_id"])
            value_by[(o["goal"], o["group"])] += to_float(o.get("value"))
    lines += ["## Lift vs holdout (incrementality)", ""]
    for g in c.goals:
        name = g.get("name")
        window = float(g.get("attribution_days", 7))
        mature = {uid for uid, fs in first_seen.items() if uid in audience and fs + timedelta(days=window) <= at}
        n_t = sum(1 for uid in mature if assignments[uid] == "treatment")
        n_h = sum(1 for uid in mature if assignments[uid] == "holdout")
        n_c = sum(1 for uid in mature if assignments[uid] == "customer_managed")
        s_t = len(converters[(name, "treatment")] & mature)
        s_h = len(converters[(name, "holdout")] & mature)
        s_c = len(converters[(name, "customer_managed")] & mature)
        r_t = s_t / n_t if n_t else 0.0
        r_h = s_h / n_h if n_h else 0.0
        r_c = s_c / n_c if n_c else 0.0
        lo, hi = newcombe_diff_ci(s_t, n_t, s_h, n_h)
        z, p = two_prop_z(s_t, n_t, s_h, n_h)
        rel = (r_t - r_h) / r_h if r_h > 0 else None
        entry = {"goal": name, "classification": g.get("classification"), "window_days": window,
                 "treatment": {"users": n_t, "converters": s_t, "rate": r_t, "ci": wilson(s_t, n_t)},
                 "holdout": {"users": n_h, "converters": s_h, "rate": r_h, "ci": wilson(s_h, n_h)},
                 "customer_managed": {"users": n_c, "converters": s_c, "rate": r_c},
                 "abs_lift": r_t - r_h, "abs_lift_ci": (lo, hi), "rel_lift": rel, "z": z, "p_value": p,
                 "value_treatment": value_by[(name, "treatment")], "value_holdout": value_by[(name, "holdout")]}
        report["goals"].append(entry)
        verdict = "not yet significant"
        if n_t >= 30 and n_h >= 30 and p < 0.05:
            verdict = "significant at 95%" + (" (treatment is worse)" if r_t < r_h else "")
        elif n_t < 30 or n_h < 30:
            verdict = "too few matured users; keep running"
        lines += [f"### {name} ({g.get('classification')}, {window:.0f}-day window)", "",
                  "| Group | Matured users | Converters | Rate | 95% CI |", "|---|---|---|---|---|",
                  f"| treatment | {n_t} | {s_t} | {pct(r_t)} | {pct(entry['treatment']['ci'][0])} to {pct(entry['treatment']['ci'][1])} |",
                  f"| holdout | {n_h} | {s_h} | {pct(r_h)} | {pct(entry['holdout']['ci'][0])} to {pct(entry['holdout']['ci'][1])} |"]
        if n_c:
            lines.append(f"| customer_managed | {n_c} | {s_c} | {pct(r_c)} | |")
        negative_goal = CLASS_REWARD.get(g.get("classification", ""), 0) < 0
        label = "Difference (treatment minus holdout, lower is better)" if negative_goal else "Absolute lift"
        lines += ["", f"{label} {pct(r_t - r_h)} (95% CI {pct(lo)} to {pct(hi)}). "
                  + (f"Relative {'change' if negative_goal else 'lift'} {100 * rel:.1f}%. " if rel is not None else "")
                  + f"p = {p:.3f}. {verdict}.", ""]

    # sends summary
    sends = [d for d in decisions if d["action"] == "send"]
    by_action = defaultdict(int)
    for d in decisions:
        by_action[d["action"]] += 1
    report["decisions"] = dict(by_action)
    lines += ["## Sends", "", "| Action | Count |", "|---|---|"]
    for k, v in sorted(by_action.items()):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    # creative performance
    lines += ["## Creative performance", ""]
    perf = []
    for m in c.messages:
        mid = m["id"]
        ms = [d for d in sends if d["message_id"] == mid]
        matured = [d for d in ms if d.get("outcome") in ("none",) or (d.get("outcome") not in ("", None))]
        conv = [d for d in ms if d.get("outcome") not in ("", "none", None)]
        neg = sum(1 for o in outcomes if o.get("message_id") == mid and CLASS_REWARD.get(o.get("classification", ""), 0) < 0)
        rate = len(conv) / len(matured) if matured else 0.0
        st = model.stats(f"message:{mid}")
        row = {"message_id": mid, "name": m.get("name", ""), "channel": m.get("channel", ""), "tags": m.get("tags", {}),
               "sends": len(ms), "matured": len(matured), "conversions": len(conv), "rate": rate,
               "negative_outcomes": neg, "posterior_mean": st["mean"], "ci": wilson(len(conv), len(matured))}
        perf.append(row)
    perf.sort(key=lambda r: r["posterior_mean"], reverse=True)
    report["creative_performance"] = perf
    lines += ["| Message | Channel | Sends | Matured | Conv | Rate | 95% CI | Posterior | Bad outcomes |", "|---|---|---|---|---|---|---|---|---|"]
    for r in perf:
        lines.append(f"| {r['name'] or r['message_id']} | {r['channel']} | {r['sends']} | {r['matured']} | {r['conversions']} | {pct(r['rate'])} | {pct(r['ci'][0])} to {pct(r['ci'][1])} | {pct(r['posterior_mean'])} | {r['negative_outcomes']} |")
    lines.append("")

    # variant performance
    vperf = []
    for m in c.messages:
        for ctype, variants in (m.get("variants") or {}).items():
            for v in variants:
                arm = f"variant:{m['id']}:{ctype}:{v['id']}"
                st = model.stats(arm)
                token = f"{ctype}={v['id']}"
                vs = [d for d in sends if d["message_id"] == m["id"] and token in (d.get("variants") or "")]
                conv = sum(1 for d in vs if d.get("outcome") not in ("", "none", None))
                vperf.append({"message_id": m["id"], "type": ctype, "variant_id": v["id"], "text": v.get("text", ""),
                              "tags": v.get("tags", {}), "sends": len(vs), "conversions": conv, "posterior_mean": st["mean"]})
    if vperf:
        report["variant_performance"] = vperf
        lines += ["## Variant performance", "", "| Message | Type | Variant | Sends | Conv | Posterior |", "|---|---|---|---|---|---|"]
        for r in sorted(vperf, key=lambda r: (r["message_id"], r["type"], -r["posterior_mean"])):
            lines.append(f"| {r['message_id']} | {r['type']} | {r['variant_id']}: {r['text'][:50]} | {r['sends']} | {r['conversions']} | {pct(r['posterior_mean'])} |")
        lines.append("")

    # timing heatmap: day of week x hour bucket conversion rate
    heat = defaultdict(lambda: [0, 0])
    for d in sends:
        if d.get("outcome") in ("", None):
            continue
        day = DAY_NAMES[parse_ts(d["send_at"]).weekday()]
        key = (day, d.get("hour_bucket", ""))
        heat[key][1] += 1
        if d["outcome"] != "none":
            heat[key][0] += 1
    if heat:
        buckets = ["morning", "afternoon", "evening", "night"]
        lines += ["## Timing (conversion rate by send day and time of day, user local)", "",
                  "| Day | " + " | ".join(buckets) + " |", "|---|" + "---|" * len(buckets)]
        report["timing"] = {}
        for day in DAY_NAMES:
            cells = []
            for b in buckets:
                s, n = heat.get((day, b), [0, 0])
                cells.append(f"{pct(s / n)} (n={n})" if n else "")
                report["timing"][f"{day}:{b}"] = {"conversions": s, "matured": n}
            lines.append(f"| {day} | " + " | ".join(cells) + " |")
        lines.append("")

    # personalization matrix: feature value x message tag value
    if c.features:
        lines += ["## Personalization matrix (conversion rate by user feature and creative tag)", ""]
        report["personalization"] = []
        tag_keys = sorted({k for m in c.messages for k in (m.get("tags") or {})})
        for feat in c.features:
            for tk in tag_keys:
                cells = defaultdict(lambda: [0, 0])
                for d in sends:
                    if d.get("outcome") in ("", None):
                        continue
                    u = audience.get(d["user_id"], {})
                    m = next((x for x in c.messages if x["id"] == d["message_id"]), {})
                    tv = (m.get("tags") or {}).get(tk)
                    if tv is None:
                        continue
                    key = (str(u.get(feat, "")), str(tv))
                    cells[key][1] += 1
                    if d["outcome"] != "none":
                        cells[key][0] += 1
                if not cells:
                    continue
                fvals = sorted({k[0] for k in cells})
                tvals = sorted({k[1] for k in cells})
                lines += [f"### {feat} x {tk}", "", "| " + feat + " | " + " | ".join(tvals) + " |", "|---|" + "---|" * len(tvals)]
                for fv in fvals:
                    row = []
                    for tv in tvals:
                        s, n = cells.get((fv, tv), [0, 0])
                        row.append(f"{pct(s / n)} (n={n})" if n else "")
                        report["personalization"].append({"feature": feat, "feature_value": fv, "tag": tk, "tag_value": tv,
                                                          "conversions": s, "matured": n})
                    lines.append(f"| {fv} | " + " | ".join(row) + " |")
                lines.append("")

    # recommendations (rules, mirroring Hightouch's categories)
    recs = []
    if perf:
        top = perf[0]
        if top["matured"] >= 50 and top["rate"] > 0:
            recs.append(f"Expand the winner: '{top['name'] or top['message_id']}' leads at {pct(top['rate'])} on {top['matured']} matured sends. Add variants in the same tone or offer type.")
        for r in perf:
            if r["matured"] >= 100 and r["ci"][1] < (top["ci"][0] if top["matured"] >= 50 else 1.0):
                recs.append(f"Retire or rework '{r['name'] or r['message_id']}': its upper bound {pct(r['ci'][1])} sits below the leader's lower bound {pct(top['ci'][0])}.")
            if r["sends"] >= 200 and r["negative_outcomes"] / max(1, r["sends"]) > 0.02:
                recs.append(f"Fatigue signal on '{r['name'] or r['message_id']}': {r['negative_outcomes']} negative outcomes on {r['sends']} sends. Tighten its send limit or refresh the content.")
        tag_cov = defaultdict(int)
        for m in c.messages:
            for k, v in (m.get("tags") or {}).items():
                tag_cov[(k, str(v))] += 1
        singles = [f"{k}={v}" for (k, v), n in tag_cov.items() if n == 1]
        if singles and len(c.messages) > 1:
            recs.append("Coverage gaps: only one message carries each of " + ", ".join(singles[:6]) + ". The model cannot separate the tag from the message until a second one exists.")
    for g in report["goals"]:
        if g["treatment"]["users"] >= 30 and g["holdout"]["users"] < 30:
            recs.append(f"Holdout for '{g['goal']}' has {g['holdout']['users']} matured users. Keep at least 10% in holdout until lift is significant.")
    if not recs:
        recs.append("Not enough matured data for a recommendation yet. Keep running; most agents need two weeks of sends.")
    report["recommendations"] = recs
    lines += ["## Recommendations", ""] + [f"- {r}" for r in recs] + [""]
    lines += ["## How to read this", "",
              "Lift compares converters per matured user in treatment against holdout; it is incrementality, not last-touch attribution, so it will not match an ESP or ad platform dashboard. "
              "Posterior means are the model's current belief after pooling each context with the global estimate; they move before raw rates do. "
              "Confidence intervals are Wilson intervals; the lift interval is Newcombe's method.", ""]

    c.reports.mkdir(parents=True, exist_ok=True)
    stem = at.strftime("%Y-%m-%d")
    (c.reports / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")
    save_json(c.reports / f"{stem}.json", report)
    print("\n".join(lines))
    print(f"\nwrote {c.reports / (stem + '.md')} and .json", file=sys.stderr)
    return report


# ----------------------------------------------------------------------------
# inspect
# ----------------------------------------------------------------------------


def cmd_inspect(c: Campaign, args) -> dict:
    uid = args.user
    assignments = load_assignments(c)
    decisions = [d for d in load_decisions(c) if d["user_id"] == uid]
    outcomes = [o for o in read_csv(c.state / "outcomes.csv") if o["user_id"] == uid]
    user = next((u for u in c.load_audience() if u.get(c.uid) == uid), None)
    salt = c.experiment.get("salt") or c.name
    latest = (c.state / "latest_run").read_text(encoding="utf-8").strip() if (c.state / "latest_run").exists() else None
    latest_skip = None
    if latest:
        latest_skip = next((r["reason"] for r in read_csv(c.out / latest / "skips.csv") if r["user_id"] == uid), None)
    result = {"user_id": uid, "in_audience": user is not None, "group": assignments.get(uid),
              "latest_run": latest, "latest_run_skip_reason": latest_skip,
              "bucket": bucket_for(uid, salt), "context": context_key(c, user) if user else None,
              "decisions": decisions[-5:], "outcomes": outcomes[-10:]}
    if user:
        result["channel_eligibility"] = {n: eligible(user, ch.get("eligibility", [])) for n, ch in c.channels.items()}
        result["message_eligibility"] = {m["id"]: eligible(user, m.get("eligibility", [])) and in_timeline(m.get("timeline"), args_now(args)) for m in c.messages}
    print(json.dumps(result, indent=2, default=str))
    return result


# ----------------------------------------------------------------------------
# validate
# ----------------------------------------------------------------------------


def cmd_validate(c: Campaign, args) -> dict:
    errors, warnings = [], []
    s = c.spec
    if not s.get("name"):
        errors.append("name is required")
    if c.mode not in ("lifecycle", "paid_ads"):
        errors.append("mode must be lifecycle or paid_ads")
    exp = c.experiment
    h, cm = float(exp.get("holdout_pct", 20)), float(exp.get("customer_managed_pct", 0))
    if h + cm >= 100:
        errors.append("holdout_pct + customer_managed_pct must be under 100")
    if h == 0:
        warnings.append("holdout_pct is 0: lift cannot be measured")
    if not exp.get("salt"):
        warnings.append("experiment.salt is unset; the campaign name is used. Set a salt so assignments survive a rename.")
    if not c.goals:
        errors.append("at least one goal is required")
    best = [g for g in c.goals if g.get("classification") == "best"]
    if len(best) != 1:
        warnings.append(f"expected exactly one goal classified 'best', found {len(best)}")
    for g in c.goals:
        if g.get("classification") not in CLASS_REWARD:
            errors.append(f"goal {g.get('name')}: classification must be one of {sorted(CLASS_REWARD)}")
        if not g.get("event"):
            errors.append(f"goal {g.get('name')}: event is required")
    if not c.messages:
        errors.append("at least one enabled message is required")
    ids = [m.get("id") for m in c.messages]
    if len(ids) != len(set(ids)):
        errors.append("message ids must be unique")
    for m in c.messages:
        if m.get("channel") not in c.channels:
            errors.append(f"message {m.get('id')}: channel {m.get('channel')!r} is not in channels")
        if m.get("offer") and m["offer"] not in c.offers:
            errors.append(f"message {m.get('id')}: offer {m['offer']!r} is not in offers")
        for ctype, variants in (m.get("variants") or {}).items():
            vids = [v.get("id") for v in variants]
            if len(vids) != len(set(vids)):
                errors.append(f"message {m.get('id')}: duplicate {ctype} variant ids")
            if len(variants) < 2:
                warnings.append(f"message {m.get('id')}: only one {ctype} variant, nothing to learn there")
    if c.mode == "lifecycle" and len(c.messages) < 2:
        warnings.append("a single message means the agent only learns timing and suppression; add a second message to learn creative")
    ap = c.audience_path()
    if not ap.exists():
        errors.append(f"audience file not found: {ap}")
    else:
        rows = read_csv(ap)
        if not rows:
            errors.append("audience file is empty")
        else:
            cols = set(rows[0].keys())
            if c.uid not in cols:
                errors.append(f"audience is missing the id column {c.uid!r}")
            for f in c.features:
                if f not in cols:
                    errors.append(f"feature {f!r} is not a column in the audience file")
            ref_fields = set()
            for ch in c.channels.values():
                for r in ch.get("eligibility", []):
                    ref_fields.add(r.get("field"))
            for m in c.messages:
                for r in m.get("eligibility", []):
                    ref_fields.add(r.get("field"))
            for f in ref_fields - cols - {None}:
                warnings.append(f"eligibility references {f!r}, which is not an audience column; every user fails that rule")
            ids_seen = [r[c.uid] for r in rows if c.uid in r]
            if len(ids_seen) != len(set(ids_seen)):
                errors.append("audience has duplicate user ids")
    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2))
    if errors:
        sys.exit(1)
    return result


# ----------------------------------------------------------------------------
# init and simulate
# ----------------------------------------------------------------------------


def cmd_init(args) -> None:
    folder = Path(args.folder)
    if folder.exists() and any(folder.iterdir()):
        die(f"{folder} exists and is not empty")
    folder.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent.parent
    tpl = here / "templates" / ("campaign.paid_ads.json" if args.mode == "paid_ads" else "campaign.template.json")
    shutil.copy(tpl, folder / "campaign.json")
    shutil.copy(here / "templates" / "audience.template.csv", folder / "audience.csv")
    (folder / "state").mkdir()
    print(f"scaffolded {folder}. Edit campaign.json and replace audience.csv, then run validate, assign, run.")


def cmd_simulate(c: Campaign, args) -> None:
    """Generate a synthetic audience when none exists, then play `days` of
    daily runs with synthetic outcomes drawn from hidden per-message rates.
    This is for dry runs and demos; the report will say 'simulated'."""
    rng = random.Random(args.seed)
    ap = c.audience_path()
    if not ap.exists() or args.users:
        n = args.users or 2000
        feats = c.features or ["segment"]
        rows = []
        for i in range(n):
            row = {c.uid: f"u{i:06d}"}
            for f in feats:
                row[f] = rng.choice(["a", "b", "c"]) if f == "segment" else rng.choice(["low", "mid", "high"])
            for ch in c.channels.values():
                for r in ch.get("eligibility", []):
                    if r.get("op") in ("true", "eq"):
                        row[r["field"]] = r.get("value", "true") if rng.random() < 0.85 else "false"
            for m in c.messages:
                for r in m.get("eligibility", []):
                    if r.get("field") not in row:
                        row[r["field"]] = r.get("value", "true") if rng.random() < 0.6 else "other"
            rows.append(row)
        write_csv(ap, rows)
        print(f"wrote synthetic audience with {n} users to {ap}")
    # hidden truth: message rates differ by context so personalization shows up
    base = c.best_goal() or {}
    neg = next((g for g in c.goals if CLASS_REWARD.get(g.get("classification", ""), 0) < 0), None)
    truth = {}
    for m in c.messages:
        truth[m["id"]] = {"*": rng.uniform(0.02, 0.08)}
    start = args_now(args) - timedelta(days=args.days)
    class A:  # tiny namespace to reuse command functions
        pass
    a = A()
    a.now = iso(start)
    a.seed = args.seed
    cmd_assign(c, a)
    audience = {u[c.uid]: u for u in c.load_audience()}
    assignments = load_assignments(c)
    organic = float(args.organic)
    for day in range(args.days):
        at = start + timedelta(days=day)
        a.now = iso(at)
        if c.mode == "lifecycle":
            summary = cmd_run(c, a)
        # generate outcomes: every user has the same organic daily chance; a send
        # adds the message's hidden incremental rate on top (that is the lift)
        decisions = load_decisions(c)
        events = []
        for uid, g in assignments.items():
            if uid in audience and rng.random() < organic:
                events.append({c.uid: uid, "event": base.get("event"), "timestamp": iso(at + timedelta(hours=rng.uniform(0, 24))), "value": round(rng.uniform(20, 120), 2)})
        for d in decisions:
            if d["run_id"] != summary["run_id"] or d["action"] != "send":
                continue
            u = audience[d["user_id"]]
            ctx = context_key(c, u)
            tr = truth[d["message_id"]]
            if ctx not in tr:
                tr[ctx] = max(0.005, tr["*"] * rng.uniform(0.5, 1.6))
            p = tr[ctx]
            if d.get("hour_bucket") == "evening":
                p *= 1.2
            if rng.random() < p:
                events.append({c.uid: d["user_id"], "event": base.get("event"), "timestamp": iso(parse_ts(d["send_at"]) + timedelta(hours=rng.uniform(1, 48))), "value": round(rng.uniform(20, 120), 2)})
            elif neg and rng.random() < 0.004:
                events.append({c.uid: d["user_id"], "event": neg.get("event"), "timestamp": iso(parse_ts(d["send_at"]) + timedelta(hours=1)), "value": ""})
        ev_path = c.state / f"sim_events_day{day:03d}.csv"
        write_csv(ev_path, events, [c.uid, "event", "timestamp", "value"])
        a.events = str(ev_path)
        a.aggregate = None
        # ingest with the clock moved forward so attribution windows can mature
        a.now = iso(at + timedelta(days=1))
        cmd_outcomes(c, a)
    a.now = iso(args_now(args) + timedelta(days=float(base.get("attribution_days", 7))))
    cmd_outcomes_mature_only(c, a)
    cmd_report(c, a)
    print("\nsimulated run complete (synthetic data). Hidden true rates:", json.dumps({k: round(v['*'], 4) for k, v in truth.items()}), file=sys.stderr)


def cmd_outcomes_mature_only(c: Campaign, a) -> None:
    empty = c.state / "sim_events_empty.csv"
    write_csv(empty, [], [c.uid, "event", "timestamp", "value"])
    a.events = str(empty)
    a.aggregate = None
    cmd_outcomes(c, a)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="decisioning", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="verb", required=True)

    sp = sub.add_parser("init", help="scaffold a campaign folder")
    sp.add_argument("folder")
    sp.add_argument("--mode", choices=["lifecycle", "paid_ads"], default="lifecycle")

    def common(sp):
        sp.add_argument("--campaign", "-c", default=".", help="campaign folder (default: cwd)")
        sp.add_argument("--now", help="override the clock (ISO timestamp), for replays and tests")

    sp = sub.add_parser("validate", help="check campaign.json and audience.csv"); common(sp)
    sp = sub.add_parser("assign", help="assign experiment groups"); common(sp)
    sp = sub.add_parser("run", help="one decisioning cycle"); common(sp)
    sp.add_argument("--seed", default="0")
    sp = sub.add_parser("outcomes", help="ingest outcome events"); common(sp)
    sp.add_argument("--events", help="CSV with user_id,event,timestamp[,value]")
    sp.add_argument("--aggregate", help="paid ads CSV with segment,creative_id,impressions,conversions")
    sp = sub.add_parser("report", help="write the report"); common(sp)
    sp = sub.add_parser("inspect", help="explain one user's decisions"); common(sp)
    sp.add_argument("user")
    sp = sub.add_parser("simulate", help="dry run with synthetic data"); common(sp)
    sp.add_argument("--days", type=int, default=21)
    sp.add_argument("--users", type=int, default=0, help="generate a synthetic audience of this size")
    sp.add_argument("--organic", type=float, default=0.01, help="daily organic conversion probability")
    sp.add_argument("--seed", default="0")

    args = p.parse_args(argv)
    if args.verb == "init":
        cmd_init(args)
        return
    c = Campaign(Path(args.campaign))
    if args.verb == "validate":
        cmd_validate(c, args)
    elif args.verb == "assign":
        cmd_assign(c, args)
    elif args.verb == "run":
        cmd_run(c, args)
    elif args.verb == "outcomes":
        if not args.events and not args.aggregate:
            die("outcomes needs --events or --aggregate")
        cmd_outcomes(c, args)
    elif args.verb == "report":
        cmd_report(c, args)
    elif args.verb == "inspect":
        cmd_inspect(c, args)
    elif args.verb == "simulate":
        cmd_simulate(c, args)


if __name__ == "__main__":
    main()
