# Routine: weekly analytics review (Friday)

Follow routines/_common.md first.

1. `python3 faceless.py measure` (add `--monetary` once `config.json` records that the channel is in the Partner Program). Then `python3 faceless.py report` and `python3 faceless.py progress`. If credentials are missing, say so and still produce the report from the ledger.
2. For every video that has been public for at least 3 days, pull the retention curve through the vidIQ connector (channel analytics, report `audience_retention`, filter `video==ID`) and traffic sources. Write per video in the weekly report: where the first drop below 70% happens (seconds), what the script was doing there (read the script and the timeline), and the main traffic source.
3. Compare title patterns: `state/learnings.json` ranks them. In the report, name the pattern with the best median views per day and the one with the worst, each with the supporting video ids.
4. Rules. Append to `routines/LEARNINGS.md` only a rule that at least two videos support, in this shape: `- [YYYY-MM-DD] RULE. Evidence: id, id.` Remove nothing; the monthly review prunes.
5. Summary: top and bottom video of the week with one sentence each on why; views in the last 28 days against the views needed at the planning RPM (from `progress`); whether the Partner Program thresholds are met; two concrete instructions for Monday's slate.
