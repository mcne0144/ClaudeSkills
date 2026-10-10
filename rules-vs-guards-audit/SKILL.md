---
name: rules-vs-guards-audit
description: Audit an AI agent or automation build to show which of its rules are enforced in code and which are held by a sentence only, ranked by what each rule costs if broken. Use whenever Shannon asks to audit, harden, red-team, or review the guardrails of a client AI build, a Claude Code project, an agent, a custom GPT, or a Zapier, Make, or n8n workflow, or asks "where could this break", "is this safe to hand off", or "what is actually stopping it from doing X".
---

# Rules vs. Guards Audit

An AI system's rules come in two kinds. Some are **guarded**: code physically stops the action. Others are **held by a sentence only**: the rule is written in a prompt and the model usually follows it, but nothing stops it if it drifts, gets confused, or gets tricked. This audit maps every rule to its enforcement and puts the costliest unguarded rules at the top.

The deliverable has two readers. The client sees a clear table of where their system is protected and where it is running on trust. Shannon gets the technical fix list.

## Step 1: Find the rules

Collect every hard rule (anything phrased as never, always, must, only, do not). Look in:

- `CLAUDE.md`, `AGENTS.md`, system prompts, agent briefs, skill files, custom GPT instructions
- Workflow descriptions and notes in Zapier, Make, n8n
- Client requirements docs, SOPs, and compliance notes the build is supposed to honor
- Ask the builder or client for rules that live only in someone's head. Those are sentence only by definition.

Number each rule. If the source already numbers them, keep its numbering.

## Step 2: Find the guards

A guard is anything that blocks or catches the action without relying on the model's judgment. Look for:

- **Claude Code:** `.claude/settings.json` permissions (deny, ask, allow lists), hooks (PreToolUse, PostToolUse, Stop) and the scripts they call in `.claude/hooks/`
- **Gate or validation scripts:** output checks, schema validation, linters, tests that run before anything ships
- **Access scope:** API keys or OAuth scopes that make the action impossible (a read-only Gmail scope guards "never send" better than any prompt)
- **Human approval steps:** draft-only modes, approval queues, manual review before send
- **Workflow tools:** filters, paths, and conditions in Zapier, Make, n8n; disabled actions
- **Routing:** fast paths or escalation rules that hand specific cases to a human

## Step 3: Map and classify

For each rule, record which guards cover it and assign one status:

- **Guarded:** code blocks every path to breaking it
- **Partial:** code covers some paths (for example, sending is blocked in Gmail but not in Slack)
- **Sentence only:** nothing but the prompt holds it

Also flag:

- **Orphan guards:** code that enforces something no written rule explains. Fine, but document it.
- **Fail-open guards:** a guard that lets the action through when it errors. A missing error handler can make one failure break many places at once.
- **Rules on both lists:** costly and sentence only. These are the headline finding.

## Step 4: Rate the cost if broken

- **Critical:** irreversible external action (sends, payments, deletes, publishes), safety, medical, legal, or compliance exposure
- **High:** corrupts data or test baselines, damages client trust, hard to undo
- **Medium:** wrong output a human would likely catch before harm
- **Low:** style or formatting

## Step 5: Recommend a fix for each gap

Work down from Critical and sentence only. For each gap, name the kind of guard that fits:

- Deny list entry or removed permission scope (cheapest, strongest)
- Pre-action hook that inspects the action and blocks it
- Output gate that checks the result before it leaves
- Human approval step
- **Judgment rules:** some rules (for example, "never make a clinical call") cannot be checked with a simple pattern. Say so plainly. Options are a second-model reviewer, a classifier, a narrower tool set so the agent cannot act on the judgment, or routing those cases to a human. Do not pretend a keyword match solves a judgment rule.

Only test a guard by trying to trip it if Shannon or the client explicitly asks, and never against live systems that can send, pay, or delete.

## Output

Lead with one line: total rules, how many guarded, partial, and sentence only, and how many Critical gaps.

Then the table:

| # | Rule (plain language) | Cost if broken | Enforced by | Status |
|---|---|---|---|---|

Then **Gaps to close**, ordered by cost, each with its recommended fix in one or two sentences.

Then **Technical notes** for Shannon or the builder: file paths, fail-open guards, orphan guards, anything that needs a code change.

Keep the client-facing part short and decisive. Write rules in plain language a GM or practice manager would understand. No em dashes anywhere.
