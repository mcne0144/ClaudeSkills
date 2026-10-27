# faceless-engine

An automated workflow for a faceless YouTube channel, built from the facelessfinder.com weekly briefing, vidIQ signals and YouTube's own monetization rules. Target: about $10,000 a month in ad revenue, with the honest math in `PLAN.md`.

| File | What it is |
|---|---|
| `PLAN.md` | Revenue math with sources, niche decision, the stage-by-stage automation map, schedule, improvement loop, costs, risks |
| `RUNBOOK.md` | How the four scheduled routines operate the engine |
| `SETUP.md` | The human checklist: channel, OAuth, keys, Partner Program |
| `faceless.py` | The CLI; every verb the routines call |
| `engine/` | Parser for the facelessfinder report, niche scorer, video ledger, script gates, ElevenLabs narration with timestamps, Pexels and card visuals, ffmpeg render, YouTube upload and analytics, learnings |
| `routines/` | Prompts for the weekly slate, production run, weekly review, monthly review, plus `LEARNINGS.md` the system writes for itself |
| `docs/` | Policy guardrails and the three research memos (GitHub pipelines, RPM data, forum lessons), plus an example script that passes every gate |
| `tests/` | Unit tests and the archived report fixture |

Quick check:

```
python3 faceless.py doctor
python3 -m unittest tests/test_engine.py
python3 faceless.py scan && python3 faceless.py board
```

Standard library plus `requests` and `Pillow`; `ffmpeg` with libass and libfreetype. Prepared with AI assistance (Claude) on 2026-10-27 and reviewed against the sources named in `docs/`.
