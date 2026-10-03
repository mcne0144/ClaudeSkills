# Brief: add a Skills page to Bright Matter Brain (Mac app)

Hand this to a Claude Code session opened in the Bright Matter Brain project folder on the Mac. The session can read the app's code; this brief says what to build.

## Goal

A separate menu item and page in Brain, "Skills", where Shannon can:
1. **Browse** every skill (search, filter by source).
2. **View** a skill's description and full instructions.
3. **Pin** skills so favorites sit at the top and persist.
4. **Run** a skill from inside Brain and see the result.

## Data

`brain-skills/skills-index.json` in the ClaudeSkills repo (github.com/mcne0144/ClaudeSkills, branch `claude/art-direction-creative-agent-rfrs30`). Shape:

```json
{ "generated": "2026-10-03", "count": 19,
  "skills": [{ "id": "account:copy-check", "name": "copy-check", "source": "account | claude-skills",
               "description": "...", "needs_connectors": false, "runs_in_brain": true, "body": "full SKILL.md text" }] }
```

- Copy the file into Brain (or fetch it from GitHub) and load it at launch. Re-copy to refresh; the generator reads the account skills synced to Claude Code and ClaudeSkills' own skills.
- 12 skills have `runs_in_brain: true`. 7 have `needs_connectors: true` (Gmail, Drive, Calendar, Docs, and similar): they cannot run inside Brain unless Brain gets those connectors, so their button should say "Open in Claude" and copy a ready prompt (`Use the <name> skill: `) to the clipboard instead of running.
- Pins and run history belong in Brain's own local store (whatever it already uses: SQLite, JSON file, UserDefaults). Pins are a set of skill ids.

## Running a skill

- Send a Claude API request with the skill's `body` as the system prompt (plus a short line: "You are running this skill for Shannon at Bright Matter. Follow it exactly.") and the user's input from a text box as the user message.
- Model `claude-opus-5-5`, `thinking: {type: "adaptive"}`, `output_config: {effort: "high"}`, stream the response into the page, keep the full output in run history with timestamp and input.
- Skills that mention files, scripts or tools they cannot reach inside Brain should say so in the output rather than pretend; do not give Brain shell access for this.
- Use the API key Brain already uses; if it has none, add a field in Brain's settings. Never write the key into the repo.
- Keep skill text and run inputs local; send only the API request.

## UI

- Match Brain's existing menu, spacing and type. Page layout: search box on top; a "Pinned" row; then a grid or list of the rest, each card with name, one-line description, source tag, a pin toggle, and a Run (or "Open in Claude") button.
- Skill detail view: description, full instructions (rendered markdown), Run panel with an input box and the streamed result, and a copy button.
- Empty and error states: no results, index file missing, API error with the message shown.

## Done means

- The Skills menu item opens the page, the index loads, search filters it, pinning persists after relaunch, running `copy-check` on a pasted paragraph returns a result and logs it to history, and a connector skill's button opens Claude with the prompt on the clipboard.
- No em dashes anywhere in the UI copy.
