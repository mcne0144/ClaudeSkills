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

## Using Atelier

Use it three ways:
1. **Claude Code**: ask for art direction help in this repo and the `art-director` skill loads, or delegate to the `art-director` subagent.
2. **Claude app (web, desktop, mobile)**: upload the zipped `art-director` folder under Settings, Capabilities, Skills.
3. **Atelier app**: see `apps/atelier/README.md`.
