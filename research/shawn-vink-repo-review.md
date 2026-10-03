# Repo review: Shawn Vink's "Githubs I use and have taken inspiration from"

Prepared for Shannon McNeil, Bright Matter. Research date: 2026-10-03. Source list: Shawn Vink (Greenway Auto), email of 2026-08-12.

## Summary

Of the 26 repos, three earn a place in the stack now or soon, a handful are worth mining for patterns, and most are either developer infrastructure Bright Matter does not need or duplicates of tools already connected. Shawn's headline pick, `bradautomates/claude-video` (the `/watch` skill), is a real fit: it gives Claude Code timestamped frames and transcripts from local footage and social URLs, which is exactly the gap between your raw-footage and trend-watch skills and the YouTube-only video reading you get from vidIQ. Run it on its local engine so client footage never leaves your machine. The second strong fit is `AgriciDaniel/claude-seo`, from the same author and marketplace as the claude-ads plugin you already trust; it covers local SEO and multi-location audits, which nothing in the current stack does. The database engines (turso, paradedb, tantivy) are serious, well-run projects, but HQ's SQLite does not need them: SQLite already ships full-text search (FTS5) if HQ ever needs search. The Firecrawl plugin, cc-websearch and mcpscraper-sdk duplicate Firecrawl MCP, Exa and Apify. Agent harnesses (harness, safe-agentic-workflow, prime-agent, thesis-writer-rig) are mostly ideas to borrow, not things to install. Note: the Firecrawl account used for this research reported low credits; top it up before relying on it for client work.

## At a glance

Stars, dates and licenses are what each repo's GitHub page showed when read on 2026-10-03. "Exa snapshot" means the figure came from Exa's read of the page rather than Firecrawl's, and Exa's numbers can lag by weeks. "Not visible" means the page read did not show the value.

| # | Repo | What it is, in plain words | Stars | Last activity | License | Verdict |
|---|---|---|---|---|---|---|
| 1 | bradautomates/claude-video | `/watch` skill: turns a video file or URL into timestamped frames plus transcript for Claude | 18k | 2026-09-25 (release 0.3.2) | MIT | ADOPT NOW |
| 2 | tursodatabase/turso | SQLite-compatible database engine rewritten in Rust, pre-1.0 | 24.5k | 2026-10-01 | MIT | SKIP |
| 3 | paradedb/paradedb | Postgres extension for search (BM25, vector, hybrid) | 9.3k | 2026-10-01 | AGPL-3.0 | SKIP |
| 4 | quickwit-oss/tantivy | Rust full-text search library (a Lucene alternative) | 16.2k | 2026-10-02 | MIT | SKIP |
| 5 | firecrawl/firecrawl-claude-plugin | Firecrawl CLI wrapped as a Claude Code skill | 231 | 2026-09-30 | AGPL-3.0 (per README) | SKIP |
| 6 | zilliztech/claude-context | Semantic code search MCP backed by a cloud vector database | 12.6k | 2026-07-14 | MIT | SKIP |
| 7 | Djarvur/cc-websearch | DuckDuckGo-based replacement for Claude Code's built-in web search and fetch | 25 | 2026-09-29 | MIT | SKIP |
| 8 | PrimeIntellect-ai/prime-agent | A separate, self-improving coding and research agent (competes with Claude Code) | 21.5k | 2026-10-02 | MIT | SKIP |
| 9 | virgiliojr94/book-to-skill | Converts a book, PDF or doc folder into a structured Claude skill | 33.3k | 2026-09-29 | MIT | TRIAL |
| 10 | VilovietaSEO/mcpscraper-sdk | Thin client for a hosted, paid scraping and lead-data service | 1 | 2026-09-30 | MIT (SDK only) | SKIP |
| 11 | naveen-annam/creativly.ai-brand-video-remotion | Example 57-second brand video built in Remotion with Claude Code | 84 | 2026-02-21 | MIT | BORROW IDEAS |
| 12 | codes30/pixovid | Self-hosted AI image/video generation and face-swap web app template | 161 | 2026-07-02 | not visible | SKIP |
| 13 | eliquid/awesome-online-reputation-management-seo | Link list of reputation-management tools and articles | 25 | 2020-06-06 | not visible | SKIP |
| 14 | AgriciDaniel/dataforseo-brain | Obsidian knowledge vault explaining the DataForSEO API and its costs | 56 | 2026-07-08 | MIT | BORROW IDEAS |
| 15 | seotesting-com/gsc-mcp-server | Google Search Console MCP server for Claude Desktop | 9 | 2025-03-18 | not visible | SKIP |
| 16 | bybren-llc/safe-agentic-workflow | Template harness of skills, commands and agent roles built on SAFe agile | 419 | 2026-07-20 (v2.11.1) | MIT plus attribution NOTICE | BORROW IDEAS |
| 17 | AI-Captains-Academy/aeo-audit | Claude Code rig that produces AEO/SEO audit reports and cold outreach | 17 | 2026-02-26 (single commit) | license file present, type not shown | BORROW IDEAS |
| 18 | jordanurbs/thesis-writer-rig | Multi-agent harness for academic thesis writing | 6 | 2026-06-26 (single commit) | MIT | SKIP |
| 19 | DanieleSalatti/AgenticDesignPatterns | Fork that points to Antonio Gulli's book "Agentic Design Patterns" | 851 | 2025-09-07 | not visible | SKIP |
| 20 | revfactory/harness | Meta-skill that designs an agent team and its skills for a project | 9.1k | 2026-09-28 | Apache-2.0 | TRIAL |
| 21 | StarTrail-org/PixelRAG | Research code: search documents as screenshots; ships a "screenshot this page" Claude skill | not visible | 2026-10-01 | Apache-2.0 | SKIP |
| 22 | ericosiu/ai-marketing-skills | Large collection of marketing, sales, content and video skills from Single Grain | 3.6k | 2026-09-22 | MIT | BORROW IDEAS |
| 23 | AgriciDaniel/claude-blog | Blog writing, SEO and refresh skill suite with a quality gate | 2,011 (Exa snapshot) | 2026-09-11 (release v2.2.0, 2026-08-25) | MIT | TRIAL |
| 24 | AgriciDaniel/claude-ads | Paid-media audit and planning skill across 12 ad platforms | 8,495 (Exa snapshot) | not visible | MIT | ALREADY IN USE (keep) |
| 25 | AgriciDaniel/claude-seo | SEO audit skill: technical, local, schema, AI-search (GEO/AEO) | 16,121 (Exa snapshot) | 2026-09-29 (v2.3.0) | MIT | ADOPT NOW |
| 26 | vibevoice-community/VibeVoice | Community fork of Microsoft's long-form, multi-speaker text-to-speech model | 1.6k | 2026-08-29 | MIT | SKIP |

## ADOPT NOW

**1. bradautomates/claude-video (`/watch`)**
- Why: gives Claude Code eyes and ears on video. A local file or URL becomes deduplicated, timestamped frames plus a transcript (native captions first, then optional WhisperX locally or Groq/OpenAI in the cloud). vidIQ covers YouTube; this covers raw store footage, TikTok and Instagram URLs, and competitor ads. Shawn's "make it do magic" is plausible here.
- Plug-in: install as a Claude Code plugin (`/plugin marketplace add bradautomates/claude-video`). Call it from the `raw-footage-plan` skill for shot logs and from `trend-watch` to actually watch the top Greenway-rooftop videos instead of reading captions.
- Risks: needs Python 3.10+, FFmpeg and current yt-dlp (plus Deno for YouTube) on the machine. The default "auto" engine uses Gemini whenever a `GEMINI_API_KEY` is present, and the README says local files are then uploaded to Google's Files API and deleted after the answer. Force `--engine local` for client footage. Optional browser-cookie flags let yt-dlp act as you on logged-in sites; do not use them on client accounts. Does not work in Claude Chat or Cowork (README). Solo maintainer.
- First step: install on your local Claude Code, set `WATCH_ENGINE=local`, and run it on one Avenues clip from `greenway-avenues-creative-rebuild` to compare against the current raw-footage-plan output.

**25. AgriciDaniel/claude-seo**
- Why: SEO, local SEO and reputation for multi-location clients is a core work type with no dedicated tool in the stack. The suite covers technical SEO, E-E-A-T, schema, GEO/AEO, local SEO and maps, Google APIs and PDF/Excel reporting. Same author and community marketplace as claude-ads, which you already run, so the trust and install path are known.
- Plug-in: add from the same ai-marketing-hub marketplace as claude-ads. Feed outputs into the Monday briefings and the Gingerwolfe agency audit; keep any changes flowing through HQ as the only publish path.
- Risks: optional extensions (DataForSEO, Firecrawl, Ahrefs, Google APIs and others per the page) each need their own keys and may cost money. The README's parallel-agent audits (up to 15 agents, maintainer claim) can burn tokens on large sites. The results screenshot in the README is a maintainer claim, not independent proof.
- First step: run a read-only audit of one Greenway rooftop site with no paid extensions, and compare the local-SEO findings to what Gingerwolfe reported.

**24. AgriciDaniel/claude-ads (already enabled)**
- Why: keep it. The README says it is read-only by default and that live account changes stay disabled until approval, verification, audit and rollback gates pass.
- Plug-in: already in ClaudeSkills via the ai-marketing-hub-claude-ads marketplace.
- Risks: confirm live-write capabilities stay off for Greenway accounts; last commit date was not visible on the page read.
- First step: none beyond updating the marketplace when convenient.

## TRIAL

**9. virgiliojr94/book-to-skill**
- Why: turns a book or document folder into a skill with a core SKILL.md, per-chapter files, glossary, patterns and cheatsheet that load on demand. The README explicitly pitches brand books and voice guidelines, which maps to Atelier's knowledge base and to client brand standards. Claim (maintainer): 24x to 51x fewer tokens than loading the whole book.
- Plug-in: run it on a Greenway brand guide or the Bright Matter brand folder (`bright-matter-brand`), then let Atelier and copy-check load the result.
- Risks: PDF extraction needs `pdftotext` or Docling locally. The converter can publish the generated skill to GitHub (private by default per README); keep that off for anything licensed or client-confidential. Converting copyrighted books is fine for private reference, not for sharing.
- First step: convert one brand guide, then ask Atelier three questions you already know the answers to and check accuracy.

**23. AgriciDaniel/claude-blog**
- Why: full blog lifecycle (briefs, drafts, schema, refresh, content decay from GSC exports) with a 100-point quality gate that blocks drafts scoring under 90 (maintainer description). Useful for rooftop-level local content and for Bright Matter's own blog.
- Plug-in: drafts land as artifact folders; route them into HQ for review and publishing rather than any direct CMS push.
- Risks: Python 3.11+; image generation uses Gemini and Google API features need their own credentials. Self-scored quality is not the same as client approval. Watch for overlap with claude-seo commands.
- First step: draft one post for a single Greenway store and run it through copy-check before anyone sees it.

**20. revfactory/harness**
- Why: you say "build a harness for this project" and it proposes an agent team (pipeline, fan-out, producer-reviewer, supervisor and other patterns) and generates the skills. variant-studio is planned but not built, which is the ideal moment to try it. Claim (maintainer, v1, author-run, n=15): quality up 60 percent; the README itself says to run your own pilot.
- Plug-in: run in a scratch branch of variant-studio only, and compare its proposed team against PLAN.md.
- Risks: it writes agents and skills into the project; review every generated file. Apache-2.0, small maintainer.
- First step: one session on a throwaway branch; keep only what improves PLAN.md.

## BORROW IDEAS

**22. ericosiu/ai-marketing-skills**
- Why: the most marketing-relevant collection on the list. Worth reading: Autoresearch (50+ variants scored by an expert panel, then evolved), Content Ops quality gate, Shortform Idea Grill (hook scoring), Video Content Engine, Client Report Generator.
- Plug-in: copy the expert-panel scoring and variant-evolution loop into variant-studio's TEST-AND-LEARN playbook rather than installing the repo.
- Risks: several skills assume vendors you do not use (RB2B, Gong). Opt-in usage telemetry exists; decline it if you ever run anything. Revenue claims in the README are marketing.
- First step: read the Autoresearch and Shortform Idea Grill folders and note what to lift into variant-studio.

**16. bybren-llc/safe-agentic-workflow**
- Why: two ideas worth stealing. "Evidence-based delivery" with stop-the-line authority, and the Knowledge Vault: every note records what it was verified against, so staleness is computed, not guessed. That second idea would keep Atelier's knowledge base honest.
- Plug-in: add a `verified_against` date and source field to Atelier knowledge notes and a small checker skill.
- Risks: heavy SAFe process built for software teams; the README says marketing adaptations are "not yet validated in production". Includes remote deploy commands and a "Dark Factory" of autonomous agents on remote servers. MIT, but the NOTICE requires attribution if you reuse it. Latest commit showed a failing check.
- First step: read the knowledge-vault README only.

**14. AgriciDaniel/dataforseo-brain**
- Why: a model for how to build a source-cited, dated knowledge vault for an API, including a cost-control playbook. Only directly useful if you enable DataForSEO inside claude-seo.
- Plug-in: if DataForSEO is enabled, point claude-seo sessions at it; otherwise copy its "every claim dated and sourced" format for HQ or Atelier notes.
- Risks: DataForSEO is a paid account. The "Brainstein SSS+ 100/100" badge is the maintainer's own scoring.
- First step: none until DataForSEO is on the table.

**17. AI-Captains-Academy/aeo-audit**
- Why: a tidy 10-agent pipeline that produces a branded AEO/SEO report from free data sources (PageSpeed, SSL, W3C, Wayback, WHOIS). The report structure and AEO-led framing are good proposal material.
- Plug-in: borrow the report outline for Bright Matter proposals and the social strategy deck.
- Risks: single commit, license type not shown on the page, and the README's sales motion is to audit prospects "without asking permission" and send it cold, which is not a Bright Matter look. claude-seo covers the same analysis with active maintenance.
- First step: read the agent list and report sections; skip installing.

**11. naveen-annam/creativly.ai-brand-video-remotion**
- Why: a worked example of code-driven brand video (kinetic type, transitions, reusable components) built with Claude Code. Relevant to the video ad mockups in greenway-avenues-creative-rebuild.
- Plug-in: compare against HeyGen HyperFrames and Clipkit, which already give you programmatic video without a Node toolchain.
- Risks: Remotion's own license terms for companies are not stated on this page; check remotion.dev before commercial use. 12,000+ lines for 57 seconds is a lot to maintain.
- First step: watch the rendered video and note which motion patterns to request in Clipkit or HyperFrames.

## SKIP

- **2. turso**: pre-1.0 engine replacement for SQLite. HQ's SQLite on Fly.io is not the bottleneck, and swapping the system of record's engine adds risk for no client-visible gain.
- **3. paradedb**: Postgres plus search under AGPL-3.0, with a curl-to-shell installer. HQ is not on Postgres and does not need a search engine.
- **4. tantivy**: a search library for developers building search engines. If HQ ever needs search over posts or briefs, SQLite's built-in FTS5 does it with zero new infrastructure. Benchmark claim (2x faster than Lucene) is the maintainer's.
- **5. firecrawl-claude-plugin**: redundant with the Firecrawl MCP you already have; adds a global npm CLI, a second API key location and a remote-browser feature that runs Playwright code in Firecrawl's cloud.
- **6. claude-context**: semantic search over large codebases; your repos are small. Sends code to an embedding provider (OpenAI by default) and a Zilliz cloud vector database.
- **7. cc-websearch**: replaces built-in WebSearch/WebFetch with DuckDuckGo HTML scraping; you already have those plus Exa and Firecrawl. 25 stars.
- **8. prime-agent**: a different agent runtime, installed by curl-to-shell. Its own README warns it executes model-generated code with your permissions and "is not a security sandbox".
- **10. mcpscraper-sdk**: the repo is only a client; the work happens in a closed, credit-billed hosted service. Overlaps Firecrawl, Exa and Apify, and its Gmail and lead-enrichment features would send mailbox and contact data to a third party. 1 star.
- **12. pixovid**: no license visible, face-swap feature (legal and ethical exposure for dealership ads), and Higgsfield and HeyGen already cover generation.
- **13. awesome ORM list**: last updated 2020, SERPWoo-heavy link list. Reputation work deserves a current source.
- **15. gsc-mcp-server**: stale (March 2025), no license visible, and the README suggests giving the service account an Editor or Owner role, which is broader than reading Search Console needs. claude-seo and claude-blog already reach GSC through Google APIs.
- **18. thesis-writer-rig**: academic; the veto-role idea is covered better by safe-agentic-workflow.
- **19. AgenticDesignPatterns**: a fork whose README only names Antonio Gulli's book; no license visible, so redistribution status is unclear. Read the book from the publisher if the topic interests you.
- **21. PixelRAG**: research project (Berkeley) for screenshot-based retrieval; its `pixelbrowse` skill screenshots pages so Claude reads layout. Firecrawl's screenshot format already gives you that. The full index is about 217 GB (README).
- **26. VibeVoice**: you already have ElevenLabs. This is a community fork kept alive after Microsoft removed the original repo, then restored it without code alongside a responsible-AI statement (README timeline). Voice cloning plus GPU requirements make it the wrong tool for client work.

## Profiles: anything notable beyond the list

These came from Exa's profile snapshots, which lag (it listed claude-video at 8,967 stars against 18k on the live repo page), so star counts here are approximate.

- **bradautomates**: `head-of-content` (social content research and marketing skills for Claude Code and Cowork), `content-ideas` (tracks competitors across X, Instagram, TikTok and YouTube with engagement data; overlaps trend-watch, worth a read), `focus-group` (builds customer personas from sales-call transcripts; interesting for dealership BDC calls, with consent questions), and `company-skills-marketplace-template` (a private team skills marketplace). That last one fits Bright Matter's "systems the client owns" pitch: a way to hand Greenway its own skills marketplace.
- **bybren-llc**: `story-systems-template` (screenplay and film project template), `a-safe-pulse` (SAFe planning with Linear and Confluence), `remote-mcp-server-with-auth` (template for a remote MCP server with GitHub OAuth, useful if HQ ever exposes its own MCP). Nothing to install.
- **AgriciDaniel**: `claude-obsidian` (Obsidian second brain), `banana-claude` (Gemini image-generation "creative director" skill; overlaps Higgsfield and Atelier), `codex-seo` (Codex port of claude-seo).
- **BetterStackHQ**: commercial logging and uptime monitoring (collector, Terraform providers). Not marketing. The only relevance is uptime monitoring for HQ's client portal on Fly.io, and Fly's own checks may already cover it.

## What Shawn likely uses versus inspiration

This is inference from the list, not something Shawn said. Most likely in his own daily use: claude-video (he recommends it outright), the AgriciDaniel suite (claude-ads, claude-seo, claude-blog, dataforseo-brain, plus he linked the profile), firecrawl-claude-plugin, cc-websearch, claude-context, gsc-mcp-server, book-to-skill and harness, since these are things you install into Claude Code. aeo-audit and thesis-writer-rig share an author (Jordan Urbs, AI Captains Academy), which suggests he follows that community. Likely inspiration only: turso, paradedb, tantivy, prime-agent, PixelRAG, VibeVoice, pixovid, AgenticDesignPatterns, the Remotion brand video and the 2020 reputation list. BetterStack may be what Greenway uses for site monitoring; worth asking.

## If you only do three things

1. Install claude-video, set it to the local engine, and run it on one Avenues clip and one top TikTok from trend-watch.
2. Add claude-seo from the same marketplace as claude-ads and run one read-only local-SEO audit on a Greenway rooftop.
3. Run book-to-skill on one brand guide and test Atelier against it.
