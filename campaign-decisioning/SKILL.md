---
name: campaign-decisioning
description: Run any client customer or ad campaign the way Hightouch AI Decisioning runs one. Use whenever Shannon wants to set up, launch, optimize, or report on a lifecycle campaign (win-back, onboarding, retention, cross-sell, service reminders) or a paid ad campaign (Meta, Google, TikTok) for a Bright Matter client, asks for a holdout or incrementality test, wants the system to pick the best message, offer, channel or send time per customer, or asks "what would Hightouch do here". Also use when a client hands over a customer list and asks what to send to whom.
---

# Campaign Decisioning

A local reproduction of the Hightouch AI Decisioning loop that works for any client and any channel: **collect inputs, decide, deliver, measure, learn.** The marketer defines the audience, the goals, the allowed messages and the guardrails. The engine assigns experiment groups, picks a message, variant, offer and send time per customer, exports a send plan, ingests outcomes, and reports lift against a holdout.

Everything runs from `campaign-decisioning/engine/decisioning.py` (Python 3.9+, standard library only). It never sends anything. The send plan is a CSV a human loads into the client's ESP, SMS tool or ad platform. That hand-off is the guard.

Read `README.md` in this folder for the Hightouch parity table and the data contracts.

## What maps to what

| Hightouch AI Decisioning | Here |
|---|---|
| Agent (audience + goals + messages + guardrails) | one campaign folder with `campaign.json` |
| Parent model and Customer Studio audience | `audience.csv` exported from the client's CRM, Shopify, DMS, BigQuery or a Zapier table |
| Holdout, treatment, customer_managed, hashed and sticky | `assign` (sha256 of user id plus salt, modulo 100, contiguous buckets) |
| Goals with Best to Worst classification and value weighting | `goals[]` with `classification`, `weight_field`, `value_per_conversion` |
| Messages, optimized content, variants | `messages[]` with `variants` per content type (subject, cta, body) |
| Tags, offers with cost | `tags`, `offers[]` with `cost_value` and `cost_multiplier` |
| Eligibility at channel, agent, message and variant level | `eligibility[]` rules at each level |
| Send limits, delivery windows, quiet hours, blackout days, frequency limits | same names in the spec |
| Reinforcement learning across message, variant, channel, timing | Thompson sampling on Beta posteriors per arm, per feature context, pooled to a global estimate |
| Smart suppression | `smart_suppression` percentile cutoff with recency boost and a minimum send probability |
| Feature matrix | `features[]`: the audience columns the model may personalize on |
| Insights: lift, creative, timing, personalization matrix, recommendations | `report` |
| Inspector | `inspect <user_id>` |
| Destinations (Braze, Iterable, SFMC) | per-channel `sendplan_<channel>.csv` plus `audience_<group>.csv` lists for the client's tools |

Not reproduced: Hightouch's warehouse-native SQL execution, its connectors, its content generation, and its localization. Creative comes from Atelier (the `art-director` skill) and the client's own templates.

## Workflow

Work one step at a time. Each step has a hard output. Do not skip to `run` with a spec Shannon has not seen.

### 1. Intake (ask, do not assume)

Collect, in Shannon's words or the client's brief:

- Client, campaign purpose, and the one measurable **best** goal (a purchase, a booking, a renewal). Supporting goals and negative goals (unsubscribe, complaint) come after.
- **Mode.** `lifecycle` when the client can message known people (email, SMS, push). `paid_ads` when the decision is which creative gets budget per segment on Meta, Google or TikTok.
- Where the audience lives and what stable id it has. Ask for the export columns. The id must not change between exports.
- Allowed channels, opt-in fields, quiet hours, frequency rules the client or the law imposes (TCPA for SMS, CASL in Canada, local time quiet hours).
- Offers the client will fund and what each costs.
- Holdout size. Default 20 percent. Below 10 percent means the test will take months to read.
- Attribution window for the best goal (7 days is the default).

If a point is unknown, write it into the spec as an explicit assumption and flag it in the summary. Do not invent opt-in data.

### 2. Scaffold and write the spec

```bash
python3 campaign-decisioning/engine/decisioning.py init clients/<client>/<campaign> --mode lifecycle
```

Edit `campaign.json`. Every `_note` field is documentation; delete or keep them, the engine ignores keys starting with an underscore. Keep ids short and stable: `winback_email_discount`, not `Email 1 (v2 final)`.

Rules of thumb:

- Start with **two or three messages that differ in substance** (offer vs no offer, urgent vs caring, product vs value). One message means the model can only learn timing and suppression.
- Two to three variants per optimized content type. More than five per type dilutes learning.
- Tag every message on the same two or three dimensions (`tone`, `offer_type`, `frame`) so the personalization matrix has something to compare.
- Set `features` to two or three audience columns that plausibly change what works (segment, tier, vehicle age, region). More contexts means slower learning per context.

### 3. Creative

Delegate copy and concept work to Atelier (`art-director` skill or subagent) with the message list and tags from the spec. Ask it for variants that differ in frame, not wording. Paste the approved text into `variants[].text`. Keep destination templates in the client's ESP; this engine chooses which template and which variant fields to send, it does not render email.

### 4. Validate and assign

```bash
python3 campaign-decisioning/engine/decisioning.py validate -c clients/<client>/<campaign>
python3 campaign-decisioning/engine/decisioning.py assign   -c clients/<client>/<campaign>
```

`validate` fails on a broken spec and warns about things that will quietly hurt learning. `assign` is idempotent and sticky: users keep their group across exports and audience changes. Before any send, export `out/<run>/suppress_from_customer_managed.csv` and make sure the client's business-as-usual campaigns exclude it. If treatment or holdout users keep receiving the client's regular sends, the lift number is invalid.

### 5. Run

```bash
python3 campaign-decisioning/engine/decisioning.py run -c clients/<client>/<campaign>
```

One run is one decisioning cycle. Daily is the normal cadence. Output lands in `out/<run_id>/`:

- `sendplan_<channel>.csv`: user id, send_at (user local, ISO), message, destination ref, chosen variant text per content type, offer, plus any `synced_user_columns`.
- `audience_treatment.csv`, `audience_holdout.csv`, `audience_customer_managed.csv`, `suppress_from_customer_managed.csv`.
- `summary.json`.

Deliver the plan the way the client's stack allows: upload the CSV to the ESP as a segment with merge fields, push rows through a Zapier table or action, or load into BigQuery for a warehouse-driven send. Say which route was used and who pressed send.

For `paid_ads` the output is `creative_allocation.csv` (segment, creative, budget share) and `customer_list_<group>.csv`. The holdout list goes on every ad set as an exclusion.

### 6. Outcomes

Collect events (purchase, booking, click, unsubscribe) with the same user id and a timestamp, then:

```bash
python3 campaign-decisioning/engine/decisioning.py outcomes -c <folder> --events events.csv
# paid ads, from the platform's segment-level export:
python3 campaign-decisioning/engine/decisioning.py outcomes -c <folder> --aggregate platform_export.csv
```

Events attribute to the most recent send inside the goal's attribution window. Positive goals add successes, negative goals add failures, and matured sends with no outcome count as a failure once. Holdout events are recorded but never train the model; they exist to measure lift.

### 7. Report and the weekly loop

```bash
python3 campaign-decisioning/engine/decisioning.py report -c <folder>
```

Writes `reports/<date>.md` and `.json`. Run it weekly and read it in this order, which is Hightouch's own checklist:

1. Lift vs holdout per goal. Below 30 matured users per group, say so and keep running.
2. Negative outcomes and fatigue signals in creative performance.
3. Timing and personalization tables for one or two test ideas.
4. Recommendations: expand, retire, refresh, coverage gaps. Act on them by editing the spec, never by hand-picking winners.

`inspect <user_id>` answers "why did this person get that" or "why did they get nothing".

### Dry run before a client sees it

```bash
python3 campaign-decisioning/engine/decisioning.py simulate -c <folder> --users 3000 --days 21
```

Generates a synthetic audience if none exists and plays three weeks with hidden true rates, so the spec, exports and report can be reviewed before real data touches it. Label anything from a simulation as simulated.

## Guardrails this skill keeps

- The engine never contacts a destination. A person loads every send plan.
- Holdout is never merged into treatment without Shannon saying so in writing, and never below 10 percent while lift is unproven.
- Opt-in fields come from the client's system. If the audience export lacks them, the channel is not eligible.
- Report lift as incrementality against holdout. It will not match the client's ESP or ad dashboard, and the report says why.
- Never use em dashes in anything written for the client.

## Related

- `art-director`: creative variants, concept cards, critique of the message set.
- `rules-vs-guards-audit`: run it on the finished campaign folder before hand-off to show the client which rules are enforced by the engine and which live in process.
