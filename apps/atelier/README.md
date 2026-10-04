# Atelier (app)

Bright Matter's art direction agent as an installable app. It runs in the browser, installs to the iPhone, Android or desktop home screen like a native app, and talks to Claude with your own Anthropic API key.

## What it does

- **Studio**: chat with Atelier. Modes: Consult, Challenge, Brand, Campaign, Avatar, 3D, Critique, Research, Lens, Vocabulary. Attach images (critique an ad, a logo, a site screenshot) or PDFs (brand guidelines, briefs).
- **Knowledge tools**: Atelier searches and reads the bundled knowledge base (`../../art-director/knowledge/`, about 74,000 words) and uses live web search and page reading for anything current, citing sources.
- **Library**: browse and search the knowledge base yourself.
- **Lenses**: draw a perspective card (an era, a world culture, an audience, a discipline) and throw it at a brief.
- **Vocabulary**: a 205-term flashcard drill, with "examples from Atelier" on any term.
- **Sessions**: saved on the device, grouped by project, exportable to Markdown or JSON.

## Model and API behavior

- Claude Opus 5.5 by default (Sonnet 5.5 selectable), adaptive thinking with a visible thinking summary, effort selectable (default high).
- Server-side refusal fallbacks are on (`fallbacks: "default"`), so a declined turn is retried on Anthropic's recommended fallback model.
- The system prompt (agent brief, catalog and three core files) is prompt-cached; the other files load on demand through the `search_knowledge` and `read_knowledge` tools.
- History is append-only so thinking blocks replay unchanged.

## Your API key

Paste a key from console.anthropic.com in Settings. It is stored only in this browser's local storage and sent only to `api.anthropic.com`. Because the key lives in the browser, use a key with a monthly spend limit, and don't host a build of this app with a key baked in.

## Run it

```bash
npm install
npm run dev       # local development
npm run build     # production build into dist/
npm run preview   # serve the build on localhost:4173
```

## Put it on your phone

1. Deploy `dist/` to any static host. On Netlify: New site from Git, pick this repo, set the base directory to `apps/atelier` (the `netlify.toml` here does the rest).
2. Open the site on your phone. iPhone: Share, then Add to Home Screen. Android: menu, then Install app.
3. Add your API key in Settings once on each device.

## Updating Atelier's knowledge

Edit `art-director/AGENT.md` or any file in `art-director/knowledge/`, then rebuild. The Claude Code skill (`.claude/skills/art-director`) reads the same files, so both stay in sync.
