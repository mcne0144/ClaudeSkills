# Campaign Decisioning

A Hightouch AI Decisioning work-alike for Bright Matter clients. One campaign folder per client campaign; one Python file does the work; nothing leaves the machine until a person uploads a send plan.

```
campaign-decisioning/
  SKILL.md                      the Claude Code skill (how to run a campaign with it)
  engine/decisioning.py         the engine, standard library only
  templates/                    campaign.json templates (lifecycle and paid_ads), audience and outcomes CSV shapes
  examples/dealership-winback/  a worked example; run `simulate` inside it to regenerate everything
```

## Quick start

```bash
python3 engine/decisioning.py init clients/acme/winback
# edit clients/acme/winback/campaign.json, replace audience.csv
python3 engine/decisioning.py validate -c clients/acme/winback
python3 engine/decisioning.py assign   -c clients/acme/winback
python3 engine/decisioning.py run      -c clients/acme/winback      # daily
python3 engine/decisioning.py outcomes -c clients/acme/winback --events events.csv
python3 engine/decisioning.py report   -c clients/acme/winback      # weekly
python3 engine/decisioning.py inspect  -c clients/acme/winback u000123
```

Dry run with synthetic data: `python3 engine/decisioning.py simulate -c <folder> --users 3000 --days 21`.

## How it decides

Each run, for every treatment user:

1. Apply the agent frequency limit and blackout days.
2. For each message: channel eligibility, timeline, message eligibility, channel weekly cap, message send limit, allowed hours (quiet hours and delivery windows in the user's time zone).
3. For each optimized content type, Thompson-sample the eligible variants in the user's feature context and keep the best.
4. Thompson-sample the message's conversion probability, multiply by (value per conversion minus offer cost). That is the expected value.
5. Thompson-sample the allowed hour buckets for the channel and pick a send hour.
6. Keep the highest expected value message, or skip with a reason.
7. Smart suppression ranks the planned sends by expected value with a recency boost and holds back the bottom slice, never below the minimum send probability.

Posteriors are Beta distributions per arm (message, variant, timing bucket) and per context (the combination of `features` values), each pooled with the arm's global estimate so a new context borrows strength until it has its own data.

Learning: positive goals add reward weighted by classification (best 1.0, very_good 0.6, good 0.3), negative goals add failure weight (bad 0.3, very_bad 0.6, worst 1.0), and a matured send without a positive outcome counts as one failure. Holdout events never train the model.

## Data contracts

**audience.csv**: one row per user. Required: the id column named by `user_id_field`. Everything else is optional and becomes available to eligibility rules, features, time zones and `synced_user_columns`.

**events.csv**: `user_id,event,timestamp[,value]`. `event` must match a goal's `event`. Timestamps are ISO 8601; naive timestamps are read as UTC.

**aggregate outcomes (paid ads)**: `segment,creative_id,group,impressions,conversions[,spend,revenue]`. `segment` is the context key as printed in `creative_allocation.csv` (for example `segment=a`).

**eligibility rules**: `{ "field", "op", "value" }` with ops `eq, ne, gt, gte, lt, lte, in, not_in, contains, exists, missing, true, false`. All rules in a list must pass.

## Reading the report

Lift is converters per matured user in treatment minus the same in holdout, with a Newcombe interval and a two-proportion z-test. A user is matured once their first assignment is older than the goal's attribution window. It is incrementality, not attribution, so it will not match the ESP or ad platform dashboard.

Posterior means move before raw rates do; that is the point of them. Below roughly 30 matured users per group the report says so instead of calling a winner.

## Getting data in and out with the tools already connected

| Need | Route |
|---|---|
| Audience export from a client system | Zapier table or action export to CSV; BigQuery query to CSV; Google Drive download |
| Send plan to an ESP or SMS tool | Zapier write action per row, or CSV upload into the destination |
| Ad platform outcomes by creative and segment | Supermetrics query exported to the aggregate CSV shape |
| Competitor creative to inspire variants | Apify Facebook Ads Library scraper, then Atelier for the concept work |
| Creative production | Atelier for direction, Canva or Higgsfield for assets |

## Not in scope

Sending. Warehouse-native execution. Automatic translation. Content generation inside the engine. Each of these is a deliberate hand-off to a person or to another skill.
