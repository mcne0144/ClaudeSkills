# ClaudeSkills

Skills, agents and apps for Bright Matter.

## Atelier: the art direction agent

| Path | What it is |
|---|---|
| `art-director/AGENT.md` | Atelier's brief: who it is, how it thinks, how it challenges ideas, Shannon's sourcing and style rules |
| `art-director/knowledge/` | The knowledge base (12 files, about 79,000 words): the Jason Swet and Tommy Geoco studies, Jason's reference network, world art history, design and typography history, visual vocabulary, advertising science, buyer journeys and algorithms, AI production tools, video/web/motion craft, brand building, methods and templates |
| `art-director/SKILL.md` | The Claude Code skill (also symlinked at `.claude/skills/art-director`). Zip the `art-director` folder to upload it as a skill in the Claude app |
| `.claude/agents/art-director.md` | A Claude Code subagent that loads the same brief and knowledge |
| `apps/atelier/` | The installable app (web app you add to your home screen) |

## Rules vs. Guards Audit

| Path | What it is |
|---|---|
| `rules-vs-guards-audit/SKILL.md` | Audits an AI agent or automation build: maps every hard rule to what enforces it (hook, deny list, gate, approval step, or a sentence only), rates the cost if broken, and lists the gaps to close. Also symlinked at `.claude/skills/rules-vs-guards-audit` |

## Campaign Decisioning

| Path | What it is |
|---|---|
| `campaign-decisioning/SKILL.md` | The skill: runs any client lifecycle or paid ad campaign the way Hightouch AI Decisioning does (audience, goals, messages, guardrails in; per-customer decisions, send plans, holdout lift and insights out). Also symlinked at `.claude/skills/campaign-decisioning` |
| `campaign-decisioning/engine/decisioning.py` | The engine. Python standard library only. Verbs: init, validate, assign, run, outcomes, report, inspect, simulate |
| `campaign-decisioning/templates/` | campaign.json templates for lifecycle and paid ads, plus the CSV shapes for audiences and outcomes |
| `campaign-decisioning/examples/dealership-winback/` | A worked example with a sample report from a simulated run |

## Faceless Engine

| Path | What it is |
|---|---|
| `faceless-engine/PLAN.md` | The plan for an automated faceless YouTube channel: sourced revenue math, niche decision from the facelessfinder briefing, the stage-by-stage automation map, schedule, improvement loop |
| `faceless-engine/faceless.py` | The engine CLI: scan, board, ledger, script gates, voice, visuals, render, upload, measure, report |
| `faceless-engine/routines/` | The four scheduled routines (weekly slate, production, weekly review, monthly review) |
| `faceless-engine/SKILL.md` | The Claude Code skill (also symlinked at `.claude/skills/faceless-engine`) |

## Using Atelier

Use it three ways:
1. **Claude Code**: ask for art direction help in this repo and the `art-director` skill loads, or delegate to the `art-director` subagent.
2. **Claude app (web, desktop, mobile)**: upload the zipped `art-director` folder under Settings, Capabilities, Skills.
3. **Atelier app**: see `apps/atelier/README.md`.
