# Routine: weekly niche scan and slate (Monday)

Follow routines/_common.md first.

1. Run `python3 faceless.py scan`. Then `python3 faceless.py board`. If the scan prints STALE_REPORT, the facelessfinder briefing is older than 14 days: use the board for niche tier and CPC only and say in the summary that topics came from vidIQ.
2. Using the vidIQ connector, for the configured niche in `config.json`:
   - outliers: long-form, published this month, maxSubscribers 300000, minViews 20000, sorted by breakoutScore, limit 20;
   - keyword research, mode rising, niche text from config, period week, limit 25;
   - trending videos, long-form, titleQuery for the niche, sorted by vph, limit 15.
   Record the raw results as `state/signals/YYYY-MM-DD.json`.
3. Read `state/learnings.json` and `routines/LEARNINGS.md`. Read the last three records under `state/videos/` to avoid repeating a topic.
4. Write 6 to 8 ideas. For each, run:
   `python3 faceless.py new "WORKING TITLE" "AI News & Tools" --kind evergreen|timely --angle "one sentence stating the editor's point of view" --source URL --source URL --source URL`
   Mix: about 60% evergreen, 40% timely. Two of the ideas must use a title pattern not in the top of `state/learnings.json` (exploration). An idea is an argument, not a topic: "Why X fails" or "What I would do about Y", with the opinion in the angle.
5. For every idea, generate 3 title candidates through vidIQ (type long, with the outlier titles as competitor context) and score them; write the candidates and scores into the record's `title_candidates` list (edit the JSON under `state/videos/`), best first.
6. Summary to the owner: one line per idea in this exact shape:
   `ID | kind | best title (score) | angle`
   followed by the commands `python3 faceless.py approve ID` for each, and a one-line note on the facelessfinder staleness and anything in LEARNINGS.md that changed the slate. Do not approve anything yourself.
