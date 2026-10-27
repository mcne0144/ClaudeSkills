# Runbook

How the routines operate the engine. Every routine is a fresh Claude cloud session started by a scheduled task. The prompt for each lives in `routines/` and is the source of truth; the scheduled task's own prompt only says "clone the repo and run this file".

## Repository layout

```
faceless-engine/
  faceless.py            CLI, every verb
  config.json            the channel, niche, cadence, gates, targets
  config.local.json      optional overrides, gitignored
  engine/                parser, scorer, ledger, script gates, voice, visuals, render, upload, analytics
  routines/              the four routine prompts plus LEARNINGS.md (rules the system writes for itself)
  state/                 committed state: ff/ archive, niche_board.json, videos/*.json, scripts/, learnings.json, used_assets.json, uploads.json
  reports/               weekly and monthly reports, committed
  work/                  renders and downloads, gitignored, rebuilt on demand
  assets/music/          royalty-free tracks, committed
  docs/                  research, policy, setup, example script
  tests/                 unit tests and the report fixture
```

Session start for every routine:

```
git clone -b faceless-engine https://github.com/mcne0144/ClaudeSkills
cd ClaudeSkills/faceless-engine
python3 faceless.py doctor
python3 -m unittest tests/test_engine.py
```

Session end for every routine: commit everything under `state/`, `reports/` and `routines/LEARNINGS.md` with a message that names the routine and the date, push to the `faceless-engine` branch, then send the push notification summary.

## Video lifecycle

```
idea -> approved -> scripted -> voiced -> visualized -> assembled -> uploaded -> published -> measured -> archived
                 \-> rejected                                   \-> failed
```

The engine refuses to spend money (voice, render, upload) on a record that was never approved. `faceless.py status` prints the board.

## Routine 1: weekly slate (Monday)

1. `faceless.py scan` then `faceless.py board`. If the scan reports STALE_REPORT, say so in the summary and do not take topics from it.
2. vidIQ: outliers for the niche (long-form, this month, under 300k subscribers, sorted by breakout), rising keywords for the niche (week), trending titles. Read `state/learnings.json` and `routines/LEARNINGS.md`.
3. Write 6 to 8 ideas with `faceless.py new "TITLE" "AI News & Tools" --kind evergreen|timely --angle "..." --source URL --source URL`. Mix per `config.cadence.evergreen_share`. Two slots go to title patterns the channel has not tried.
4. For each idea, score 3 title candidates with vidIQ and record the best in the record's `title_candidates`.
5. Summary for the owner: one line per idea with id, kind, angle, best title score, and the approve command. Nothing is approved by the routine.

## Routine 2: production (Tuesday, Thursday, Saturday)

1. `faceless.py status`. Take the oldest record in `approved`. If there is none, stop and say so.
2. Research: at least three primary sources (vendor docs, papers, filings, official posts) through Exa and Firecrawl. Save notes to `work/<id>/research.md`.
3. Write the script in the format of `docs/examples/sample-script.md`: a hook under 60 words, scenes every 20 to 30 seconds with two visual keyword phrases, an outro, at least six first-person opinion sentences, the sources comment. Framing rule: analysis and opinion from a human editor, never advice; no "you should buy", "you should invest", no medical or legal guidance.
4. `faceless.py script-check PATH` until it passes, then `faceless.py script-save ID PATH`.
5. `faceless.py voice ID`. Without an API key: generate narration through the ElevenLabs connector with the configured voice, download it to `work/<id>/narration.mp3`, run `faceless.py voice ID --from-audio work/<id>/narration.mp3`.
6. Key images: generate 6 to 10 images through the ElevenLabs or Higgsfield image connector, one per argument-carrying scene, landscape, no text in the image, no real people, and save them as `work/<id>/supplied/scene-NN.png` using the scene index from `work/<id>/audio/timeline.json`. Generate a thumbnail image the same way (or with vidIQ generate-thumbnail from the title) and save as `work/<id>/supplied/thumbnail.jpg`.
7. `faceless.py visuals ID`, then `faceless.py assemble ID`. Watch the mix line; if the card share is above 0.4, add images before rendering.
8. Metadata: pick the title from the record's candidates (rescore with vidIQ if the script changed the angle), write a description whose first sentence is specific to this video, add chapters from the timeline, list the sources, add up to 15 tags, save as JSON, `faceless.py metadata ID PATH`.
9. `faceless.py upload ID --dry-run` to inspect, then `faceless.py upload ID`. The video is private and scheduled for the next configured slot.
10. Summary: title, scheduled time, duration, visual mix, ElevenLabs characters used, the YouTube Studio link for the veto window.

## Routine 3: weekly review (Friday)

1. `faceless.py measure` (add `--monetary` once monetized), then `faceless.py report` and `faceless.py progress`.
2. For each video published more than 3 days ago, read retention through vidIQ channel analytics (report `audience_retention` with the video filter). Note where the first drop is and what the script was doing there.
3. Append rules to `routines/LEARNINGS.md` only when the same pattern shows in at least two videos. Each rule names the videos that support it.
4. Summary: the top and bottom video of the week with one sentence each on why, progress against the target in views and (if available) revenue, and two instructions for Monday's slate.

## Routine 4: monthly review (1st of the month)

1. Re-run `faceless.py board`; compare with the stored board; note niches that moved.
2. Compare observed RPM (progress) with the assumed figures in `config.targets`. If observed exists, write it into `config.targets.assumed_rpm_usd.mid` with its source.
3. Decide, for the owner to confirm: keep cadence, raise to 4 or 5 a week (only if median average view percentage is above 40% and views per video are rising), or hold. Say whether the Partner Program thresholds are met.
4. Policy check: any video with a limited-ads icon in Studio, any appeal pending, any script that failed gates more than twice.
5. Write `reports/monthly-YYYY-MM.md` and a push summary ending with the decisions that need a human yes.

## Manual verbs

```
python3 faceless.py approve ID "why"      python3 faceless.py reject ID "why"
python3 faceless.py status                python3 faceless.py progress
python3 faceless.py upload ID --publish-at 2026-11-04T21:00:00Z
```
