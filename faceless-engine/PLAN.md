# Faceless engine: the plan

Goal as set on 2026-10-27: use facelessfinder.com/report to set up an automated workflow that produces about $10,000 a month in ad revenue, with the routines scheduled and the system improving over time.

This document is the plan. RUNBOOK.md is how the routines operate it. SETUP.md is the human checklist. docs/ holds the research every number here comes from.

## 1. The honest math

Ad revenue is views times RPM. Nothing in this system changes that, so the plan starts from sourced RPM figures and works back to the views the channel has to earn.

### RPM figures used

| Figure | Value | Source and tier |
|---|---|---|
| Education & Science long-form, median | $10.22 (range $2.31 to $19.50) | AIR Media-Tech, 300 channels, Studio data, May 2025 to May 2026. docs/RESEARCH-rpm-and-facelessfinder.md. Tier 2 |
| All niches long-form, median | $2.30 | Same dataset. Tier 2 |
| Business channel, 1M views, US | $4.80 low, $8.00 mid, $12.80 high | vidIQ earnings calculator, run 2026-10-27. Tier 2 estimator |
| Technology channel, 1M views, US | $3.00 low, $5.00 mid, $8.00 high | vidIQ earnings calculator, run 2026-10-27. Tier 2 estimator |
| One faceless AI channel | $9.00 | Creator Studio screenshot, July 2025. Tier 1, single channel |
| One AI news channel | $3.10 | Creator-stated, Q1 2026. Tier 1, single channel |
| Shorts, US audience | $0.33, most niches $0.07 to $0.20 | AIR, 274 channels, Sep 2026. Tier 2 |

Shorts are excluded from the revenue model: at those figures it takes 11,000 to 34,000 Shorts views to earn what 1,000 long-form views earn.

### Views required for $10,000 a month

| Long-form RPM | Monetized views needed per month |
|---|---|
| $3.00 | 3,333,000 |
| $5.00 | 2,000,000 |
| $8.00 | 1,250,000 |
| $10.00 | 1,000,000 |
| $12.80 | 781,000 |

The planning case is $8 RPM (the vidIQ mid figure for a US business and technology audience, inside the AIR science range), so the channel needs about 1.25 million long-form views a month, from a catalog, not from one hit.

### How a catalog gets there

At 3 videos a week the catalog is 13 videos after one month, 39 after three and 78 after six. At 1.25 million views a month across 78 videos, the average video has to earn about 16,000 views a month, with most views on a few winners and a long tail on the rest. That is a normal shape for an explainer channel, and it is not a first-month shape. The forum consensus (docs/RESEARCH-forum-lessons.md) is 20 to 30 uploads before judging and 6 to 12 months to traction. This plan budgets for that and measures from video 10 onward.

What the plan does not promise: that $10,000 a month arrives on a date. It promises a system that produces three policy-safe, sourced, original long-form videos a week with two human touches, measures every one of them, and bends its own topic selection toward what the audience watches. Revenue follows views; views follow retention and packaging; the loop in section 6 is how both improve.

## 2. Niche selection, from the facelessfinder briefing

The briefing (week of 2026-07-05, 40 niches, 1.8K videos scanned) ranks niches by its Rising Index. Run through this engine's scorer (`faceless.py board`), which adds a fit bonus for the operator's expertise and a penalty for niches where an AI-narrated channel would be giving advice on finance, health or legal matters, the top of the board is:

| Rank | Niche | facelessfinder RPM tier | Effort | Rising | CPC | Why it ranks |
|---|---|---|---|---|---|---|
| 1 | AI News & Tools | HIGH | mid | 1.19 | $8.03 | High advertiser demand, 11 outliers, and it is the operator's own field, which is the originality defense the policy asks for. Short shelf life, so it is paired with evergreen explainers |
| 2 | Science Explainers | HIGH | mid | 0.08 | $13.32 | Highest CPC on the board; the AIR dataset puts Education & Science at the top of measured RPM |
| 3 | Tech Explainers | HIGH | mid | 0.15 | $2.49 | Evergreen, adjacent to niche 1, shares the voice and visual system |
| 4 | Animal Facts & Wildlife | HIGH | low | 0.44 | $3.06 | Backup only; measured RPM evidence is weak |

Not chosen despite higher Rising Index: Crypto News (rank 1 on facelessfinder), Stock Market Recaps (rank 2), Side Hustle Ideas, Personal Finance. YouTube's monetization policy names "AI podcast hosts giving financial guidance" as not eligible to monetize (docs/POLICY.md). A synthetic-voice channel in those niches is building on the exact ground YouTube is clearing.

Decision: one channel, niche AI News & Tools, with a 60/40 split between evergreen explainers (how agents work, what a model actually does, why a tool failed) and timely pieces (a release, a policy, a lawsuit) that are framed as analysis with a stated point of view, never as advice. Science and Tech Explainers are the configured backups and the candidate for a second channel once the first is in the Partner Program.

Note on the data source: the facelessfinder briefing has not refreshed since 2026-07-05 (docs/RESEARCH-rpm-and-facelessfinder.md). The engine flags it stale and takes live topic signals from vidIQ (outliers, rising keywords, trending). If facelessfinder resumes, the weekly scan archives every edition and the scorer reports week-over-week deltas.

## 3. Format

- Long-form, 8 to 12 minutes, 1080p30, burned-in captions, synthetic narration (ElevenLabs "Brian", resonant and comforting, chosen for long listening).
- One idea per video, a hook under 60 words, at least six first-person point-of-view sentences, at least three cited sources, no banned filler phrases, no reuse of structure between scripts. All of this is enforced in code by `faceless.py script-check`.
- Visuals: a mix of AI-generated images with motion, stock footage, and a small number of designed text cards. The renderer refuses to build a video that is more than half text cards, because an image slideshow is named as non-monetizable.
- Every video gets its own thumbnail and a unique first sentence in its description. The uploader refuses duplicates.
- Published on Tuesday, Thursday and Saturday at 3 pm Central, scheduled through the API as private with a publish time, so a human can pull any video before it goes live.

## 4. The pipeline, stage by stage

| Stage | What happens | Who does it | Automated today |
|---|---|---|---|
| Scan | Fetch and parse the facelessfinder briefing, archive it, flag staleness | `faceless.py scan` | Yes |
| Niche board | Score the 40 niches for this operator and the policy climate | `faceless.py board` | Yes |
| Topic signals | vidIQ outliers under 300k subscribers, rising keywords, trending titles in the niche; without vidIQ, `faceless.py signals` reads the YouTube Data API or the archived breakouts | Weekly routine via the vidIQ connector, else the engine | Yes |
| Slate | 6 to 8 idea records with angle, kind (evergreen or timely), sources, scored title candidates | Weekly routine, `faceless.py new` | Yes |
| Approval of the slate | Read the slate, approve or reject each idea | Human, one touch a week; `faceless.py approve` | No, by design |
| Research | Primary sources for the chosen idea (docs, papers, filings, the operator's own notes) | Production routine via Exa and Firecrawl | Yes |
| Script | Markdown script with hook, scenes with visual keywords, outro, sources, point of view | Production routine (Claude) | Yes |
| Script gates | Length, hook, point of view count, sources, similarity, banned phrases, em dashes | `faceless.py script-check` | Yes |
| Voice | One ElevenLabs request per scene with timestamps, narration.mp3, captions.srt, timeline | `faceless.py voice` (API key) or the ElevenLabs connector plus `--from-audio` | Yes |
| Key images | 6 to 10 AI images for the scenes that carry the argument | Production routine via the ElevenLabs or Higgsfield connector, dropped into `work/<id>/supplied/` | Yes |
| Stock footage | Pexels clip per remaining scene, never reused across videos | `faceless.py visuals` (Pexels key) | Yes |
| Render | Scene clips, Ken Burns on stills, crossfades, captions, ducked music, thumbnail | `faceless.py assemble` | Yes |
| Packaging | Title candidates scored by vidIQ, description with chapters and sources, tags | Production routine, `faceless.py metadata` | Yes |
| Thumbnail | Generated through vidIQ or an AI image, scored, dropped into `supplied/thumbnail.jpg` | Production routine | Yes |
| Upload | Resumable upload, private, scheduled publish time, synthetic-media flag, uniqueness checks, quota cap | `faceless.py upload` | Yes, once OAuth exists |
| Veto window | Review scheduled uploads in YouTube Studio before publish time | Human, optional | No, by design |
| Measure | Public stats and Analytics API per video, snapshots in the ledger | `faceless.py measure` in the Friday routine | Yes |
| Learn | Median views per day and average view percentage by title pattern, kind and niche | `faceless.py measure` updates `state/learnings.json` | Yes |
| Weekly report | Pipeline board, progress against target, what is working, notes for the next slate | `faceless.py report` plus the Friday routine's reading of it | Yes |
| Monthly review | Re-score niches, compare observed RPM to assumed, decide cadence and second channel | Monthly routine with a human decision at the end | Partly |

Human work that remains, and why it stays human: creating the channel and the Google Cloud OAuth client (SETUP.md), approving the weekly slate, pulling a scheduled video if it reads wrong, applying to the Partner Program when the thresholds are met, and the monthly go or no-go on cadence. The forum record of the January 2026 demonetization wave is clear that fully unattended pipelines are the ones that get caught (docs/RESEARCH-forum-lessons.md). Two touches a week is the price of staying monetized.

## 5. Schedule

All times America/Chicago. Each routine is a Claude scheduled task that starts a fresh session, clones this repo, runs its prompt from `routines/`, commits state back, and sends a push notification with a short report. The four tasks exist and are enabled (ids in SETUP.md step 7); they need their connectors attached from the claude.ai scheduled tasks UI, which the scheduler would not accept from this session.

| When | Routine | Prompt file | Output |
|---|---|---|---|
| Monday 06:40 | Weekly niche scan and slate | routines/weekly-slate.md | `state/ff/`, `state/niche_board.json`, 6 to 8 idea records, slate summary for approval |
| Tuesday, Thursday, Saturday 05:40 | Production run | routines/produce.md | One rendered, packaged, scheduled video per run from the approved queue |
| Friday 07:40 | Analytics review | routines/weekly-review.md | Metrics snapshots, `state/learnings.json`, `reports/weekly-*.md`, notes for next slate |
| 1st of the month 08:40 | Strategy review | routines/monthly-review.md | `reports/monthly-*.md` with the cadence and niche decisions for a human to confirm |

Why these times: production runs sit a day and a half before each publish slot (Tue, Thu, Sat at 15:00), so there is always a veto window.

## 6. How it gets better with time

1. Learnings feed the slate. `state/learnings.json` ranks title patterns, idea kinds and niches by median views per day and average view percentage. The weekly slate prompt reads it and biases the next 6 to 8 ideas toward the top buckets while reserving two slots for new patterns, so the channel explores as well as exploits.
2. Retention notes become rules. The Friday review reads each video's retention curve (Analytics API, or vidIQ channel analytics once the channel is connected) and appends concrete hook and pacing rules to `routines/LEARNINGS.md`, which the production prompt loads. Rules that do not hold up are removed in the monthly review.
3. The facelessfinder archive accumulates. Every scan is archived under `state/ff/<week>.json`; the scorer reports rising deltas once there are two editions and will weight trend once there are three.
4. The script gates ratchet. The similarity ceiling and point-of-view floor live in `config.json`; the monthly review tightens them if any video draws a policy flag and loosens nothing.
5. Observed RPM replaces assumed RPM. Once the channel is monetized, `faceless.py progress` computes the real RPM from the Analytics API and restates the views target from it.
6. The stock ledger prevents drift. `state/used_assets.json` guarantees no Pexels clip repeats across videos, which is both a quality measure and a defense against the "templated visuals" finding.

## 7. Costs

| Item | Cost | Source |
|---|---|---|
| ElevenLabs narration | A 1,300-word script is about 7,500 characters. Creator plan, $22 a month for 100,000 characters, covers about 13 videos; Pro, $99 for 500,000, covers about 65 | https://elevenlabs.io/pricing, read 2026-10-27 |
| Pexels stock footage | Free with attribution not required (Pexels license); API key free | https://www.pexels.com/api/ |
| vidIQ credits | 2,000 renewable a month on the connected plan (read 2026-10-27). A production run spends roughly 20 to 50 credits (titles 5, outliers 5, a thumbnail 22) | vidIQ balance call |
| YouTube Data API | Free; 100 uploads a day per project | docs/POLICY.md |
| Claude scheduled tasks | Run on the account's plan; four routines a week plus three production runs | |
| Music | Royalty-free tracks dropped into `assets/music/` (none shipped; Pixabay Music and the YouTube Audio Library are free for this use) | |

## 8. Risks and what the engine does about them

| Risk | Mitigation |
|---|---|
| Generic or repetitive content finding | Script similarity gate, point-of-view floor, unique packaging checks, visual mix check, human slate approval |
| AI persona on a sensitive topic | Niche avoid list and scorer penalty; production prompt forbids advice framing; analysis is stated as the editor's opinion with sources |
| Reused content | No clip compilations; stock is B-roll under original narration; every claim is sourced |
| facelessfinder goes away | It is one input of four; vidIQ and Exa carry the live signals; the archive keeps what was learned |
| OAuth token expiry | Consent screen must be in Production (SETUP.md); `doctor` reports token refresh failures with the cause |
| Cost runaway | Voice and render only run on approved records; upload cap of 90 a day in code; ElevenLabs is per character with a known ceiling per video |
| Zero views for months | Expected. The plan measures from video 10, keeps a 30-video budget before judging, and the Friday review reports honestly rather than flattering |
