# Routine: monthly strategy review (1st of the month)

Follow routines/_common.md first.

1. `python3 faceless.py scan` and `python3 faceless.py board`. Diff against the previous `state/niche_board.json` (git show HEAD~N) and list niches that moved more than three places.
2. `python3 faceless.py progress`. If an observed RPM exists, update `config.json` `targets.assumed_rpm_usd.mid` to it and set `targets.assumed_rpm_source` to "YouTube Analytics API, last 28 days, YYYY-MM-DD".
3. Read all weekly reports from the month. Decide and write, for the owner to confirm:
   - cadence: hold at 3 a week, or raise to 4 or 5 only if the median average view percentage of the month's videos is above 40% and views per video are rising month over month;
   - niche: keep, or add the backup niche as a second channel only if the first channel is in the Partner Program and the production routine has had no failed run in four weeks;
   - gates: tighten `quality_gates.max_similarity_to_previous` or raise `min_pov_sentences` if any video drew a limited-ads or policy flag; never loosen.
4. Prune `routines/LEARNINGS.md`: remove rules contradicted by this month's data, and say which.
5. Policy audit: for each published video check in Studio (through the vidIQ connector where possible) for limited ads, copyright claims, or a disclosure label applied by YouTube. List them.
6. Write `reports/monthly-YYYY-MM.md` with the sections: numbers, what worked, what did not, decisions needing a yes, policy audit. The summary ends with the decisions as yes-or-no questions.
