# Policy guardrails (YouTube, read 2026-10-27)

Everything below is quoted or paraphrased from YouTube's own help and developer pages, which are the primary source. Forum reports of enforcement are in RESEARCH-forum-lessons.md and are anecdotes.

## Partner Program thresholds

Source: https://support.google.com/youtube/answer/72851

- "Get 1,000 subscribers with 4,000 qualified watch hours in the last 12 months, or"
- "Get 1,000 subscribers with 10 million qualified Shorts views in the last 90 days."
- Also required: follow the channel monetization policies, live in an eligible country, no active Community Guidelines strikes, 2-Step Verification on the Google account, advanced features access, one active AdSense for YouTube account linked.
- Updated YPP terms take effect February 1, 2027 and must be accepted by January 31, 2027.

## Channel monetization policies, the parts that bind this engine

Source: https://support.google.com/youtube/answer/1311392

- July 15, 2025 notice: "We're making a minor update to our 'repetitious content' policy to better clarify this includes content that is repetitive or mass-produced." Renamed to "inauthentic content"; "This type of content has always been ineligible for monetization."
- What is checked: content must "Not be mass-produced, generic, repetitive, or manipulative."
- Generic or repetitive content, not allowed: "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value" and "AI-generated content made with generic or unoriginal templates giving the impression of mass production." Allowed: shared intros and outros, series with recurring characters where each video has its own storyline, focus or concept.
- Reused content, not allowed: clip compilations with little narrative, reactions with no spoken commentary, readings of others' text. Allowed: critical reviews, reaction with commentary, substantial editing.
- Unsatisfying or off-putting content: "If you use automated tools or templates to help create your content" the channel is checked for "generic templates or emotionally manipulative themes" and "videos that stitch together unrelated or inconsistent AI clips to surprise or shock viewers."
- AI personas related to sensitive topics: "any content that presents itself as a human expert providing advice to viewers", with the examples of an AI doctor giving health advice, AI podcast hosts giving financial guidance, AI personas giving legal advice; "channels uploading this content will not be allowed to monetize."
- Enforcement: limit ad earnings, suspend YPP, suspend or terminate the channel, "Withhold, adjust, charge back, or offset earnings or payment."

## Disclosure of altered or synthetic content

Source: https://support.google.com/youtube/answer/14328491

- "We require creators to disclose AI-generated or altered content that seems realistic": a real person made to appear to do or say something, altered footage of a real event or place, realistic scenes that never happened, AI music as the main focus.
- Not required: non-realistic AI content, minor edits, "using AI for scripts, titles, or thumbnails."
- In the API the flag is `status.containsSyntheticMedia` on videos.insert and videos.update. Creators who consistently fail to disclose "may be subject to manual application of a label" and penalties up to YPP suspension.

## YouTube Data API

Source: https://developers.google.com/youtube/v3/getting-started#quota and https://developers.google.com/youtube/v3/docs/videos/insert (last updated 2026-10-15)

- Default quota per project per day: 100 `search.list` calls, 100 `videos.insert` calls, and 10,000 units for all other endpoints combined. A video upload costs 1 unit; most other writes cost about 50; reads cost 1.
- "Videos uploaded from unverified API projects are not restricted to private viewing mode." Google confirmed on Issue Tracker 572863050 (2026-10-13) that the forced-private restriction was lifted and a compliance audit is no longer required to bypass it. Audits still apply to quota extension requests.
- An OAuth consent screen left in Testing mode expires refresh tokens after 7 days (Google OAuth docs; also reported in the SaarD00 README). The consent screen must be set to Production for an unattended uploader.

## How the engine enforces this

| Rule | Where it is enforced | What enforces it |
|---|---|---|
| No templated scripts | `engine/script_tools.py` | 5-gram Jaccard similarity against every previous script, hard fail above 0.25 |
| Original point of view in every video | `engine/script_tools.py` | at least 6 first-person opinion sentences per script, hard fail |
| Sourced claims | `engine/script_tools.py` | at least 3 source URLs per script, hard fail |
| No AI persona giving finance, health or legal advice | `config.json` niche.avoid and `engine/niche_score.py` policy penalty; routine prompts forbid advice framing | scorer penalty plus prompt rule; the human approval gate is the backstop |
| Not an image slideshow | `engine/assemble.py` | visual mix check: stock footage share, motion on every still (Ken Burns), text cards capped |
| Unique packaging per video | `engine/youtube.py` | description first sentence must be unique across the ledger; thumbnail perceptual hash must differ from every previous thumbnail |
| Synthetic media disclosure | `engine/youtube.py` | `containsSyntheticMedia` set from config (default true because AI images of realistic scenes may appear) plus a description footer stating AI assistance and synthetic narration |
| Human review before money is spent or anything publishes | `engine/ledger.py` statuses `approved` and `publishing.require_human_approval` | voice, render and upload verbs refuse to run on a record that is not approved |
| Upload quota | `engine/youtube.py` | per-day upload counter in state, refuses past 90 |
