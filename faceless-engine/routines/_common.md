# Common rules for every faceless-engine routine

Work autonomously. No one is watching this run and no one will answer a question, so decide and record the decision in the summary.

Start:

```
git clone -b faceless-engine https://github.com/mcne0144/ClaudeSkills
cd ClaudeSkills/faceless-engine
python3 faceless.py doctor
python3 -m unittest tests/test_engine.py
```

If the clone fails because the branch was merged, clone the default branch and work in `faceless-engine/` there. If the GitHub connector is needed to attach the repo, use it.

Rules:

- The engine refuses to spend money on anything not approved by a human. Never work around a refusal; report it.
- Never use em dashes anywhere: scripts, descriptions, reports, commit messages. Rewrite the sentence.
- Name the source for every figure. Blank beats plausible; never estimate a number a source did not give.
- Policy (docs/POLICY.md): no advice framing on finance, health or legal matters; analysis with a stated point of view only. No reused clips, no scrolling text, no slideshows. Every video has its own thumbnail and a unique first sentence in its description.
- Read `routines/LEARNINGS.md` before writing anything creative; it holds rules the channel learned from its own data.

Finish:

```
git add state reports routines/LEARNINGS.md config.json
git commit -m "<routine name> <YYYY-MM-DD>"
git push origin faceless-engine
```

Then send the summary. Keep it short and scannable, lead with what needs the owner, and include every approve or reject command the owner might want to run.
