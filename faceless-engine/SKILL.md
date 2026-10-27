---
name: faceless-engine
description: Run the faceless YouTube content engine. Use whenever Shannon wants to scan faceless niches, build or approve a video slate, produce a long-form narrated video (script, voice, visuals, render, upload), review channel analytics, or check progress toward the ad revenue target. Also use when a scheduled routine names a file under faceless-engine/routines/.
---

# Faceless engine

A pipeline that turns a niche briefing into scheduled, policy-safe, long-form YouTube videos, with a human approving the weekly slate and the engine doing the labor.

Read in this order the first time: `PLAN.md` (the math and the decisions), `RUNBOOK.md` (how the routines operate it), `docs/POLICY.md` (what keeps it monetizable), `SETUP.md` (what only the owner can do).

## Verbs

```
python3 faceless.py doctor | scan | board | status | progress
python3 faceless.py new "TITLE" NICHE --kind evergreen|timely --angle "..." --source URL
python3 faceless.py approve ID | reject ID
python3 faceless.py script-check PATH | script-save ID PATH
python3 faceless.py voice ID [--from-audio MP3] | visuals ID | assemble ID
python3 faceless.py metadata ID PATH.json | upload ID [--dry-run]
python3 faceless.py measure [--monetary] | report
```

## Rules that bind every session

- Nothing paid (voice, render, upload) runs on a record a human did not approve. Do not work around a refusal.
- Scripts are analysis with a stated point of view, never advice on money, health or law.
- No em dashes anywhere. Name the source for every figure. Blank beats plausible.
- Commit `state/`, `reports/` and `routines/LEARNINGS.md` at the end of every run and push to the `faceless-engine` branch.

## Routines

`routines/weekly-slate.md` (Monday), `routines/produce.md` (Tue, Thu, Sat), `routines/weekly-review.md` (Friday), `routines/monthly-review.md` (1st). Each is a Claude scheduled task that starts a fresh session and runs the file.
