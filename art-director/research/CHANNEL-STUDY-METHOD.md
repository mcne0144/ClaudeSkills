# How Atelier studies a creator

The repeatable method behind `knowledge/01-jason-swet-study.md` and `knowledge/12-tommy-geoco-study.md`. Use it for the next creator so every study is comparable.

## 1. Collect (primary sources only)

| Step | Tool | Settings |
|---|---|---|
| Top videos with stats and captions | Apify `clockworks/tiktok-scraper` | `profiles: [handle]`, `profileSorting: popular`, `resultsPerPage: 80`, `downloadSubtitlesOptions: DOWNLOAD_SUBTITLES`, `maxFollowingPerProfile: 150` |
| Recent videos (the popular sort skews old) | same | `profileSorting: latest`, `resultsPerPage: 40`, `DOWNLOAD_AND_TRANSCRIBE_VIDEOS_WITHOUT_SUBTITLES` |
| Transcripts of teaching videos with no captions | same | `postURLs: [...]`, `TRANSCRIBE_ALL_VIDEOS` (charged per video) |
| Read captions and transcripts | `get-key-value-store-record` on the run's key-value store | the follow list comes from `authorMeta.followDatasetUrl` (a signed URL, fetch with curl) |
| YouTube channel, videos, transcripts | vidIQ `channel_search`, `channel_videos` (popular and recent), `video_transcript` | long transcripts go to a research subagent that writes notes to `research/` |
| Facts about the person, their companies, people they cite | Exa search and fetch | primary pages first (their site, company pages, original studies) |

## 2. Analyze

- **Performance read**: median views, and save rate (saves / views) as the value signal. Flag paid partnerships and treat their reach as bought.
- **Frameworks**: named concepts, formulas, taxonomies, rules of thumb, in the creator's own words with short verbatim quotes.
- **Format craft**: how the videos open, their structure, their recurring series formats. These become templates for Bright Matter content.
- **Case studies** they teach from, with the transferable lesson.
- **Reference network**: who they follow and cite, split into creative-relevant and personal.
- **Evidence check**: any statistic they cite gets traced to its origin. Record what it actually measured (sample size, comparison base) and whether the creator's framing matches.
- **Disagreements and blind spots**: where the creator conflicts with another study in the knowledge base or with the evidence. Atelier should be able to argue both sides.

## 3. Write

File `knowledge/NN-<name>-study.md`, with sections in this order: who they are, what performs, core teachings, format craft, case studies, evidence check, reference network, how Atelier should use this. Rules: no em dashes, name the source and its tier, mark the creator's claims as claims, leave out what can't be verified. Raw notes stay in `research/` so they don't pollute search results.

## 4. Wire in

- Add a row to the table in `SKILL.md`.
- Add a line to `AGENT.md` only if the study changes Atelier's default behavior.
- Rebuild the app (`apps/atelier`, `npm run build`) so the new file is bundled.
