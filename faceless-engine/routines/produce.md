# Routine: production run (Tuesday, Thursday, Saturday)

Follow routines/_common.md first.

1. `python3 faceless.py status`. Take the oldest record in `approved`. If there is none, finish with the summary "No approved ideas; run or approve the slate" and stop.
2. Research. Find at least three primary sources for the idea (vendor documentation, papers, official announcements, filings, transcripts) through Exa and Firecrawl. Prefer the entity that made or governs the thing. Save `work/<id>/research.md` with quotes and URLs. If the angle in the record does not survive the research, change the angle and say so in the summary.
3. Script. Write `work/<id>/script.md` in the format of `docs/examples/sample-script.md`:
   - `# TITLE`, `<!-- angle: ... -->`, `<!-- sources: a | b | c -->`
   - `## HOOK` under 60 words that states the claim and why it matters now
   - `## SCENE: visual keywords | fallback keywords` every 20 to 30 seconds of narration (about 50 to 80 words), with concrete, filmable keywords (objects, places, actions), not abstractions
   - at least six first-person opinion sentences spread through the script ("I think", "in my experience", "I disagree", "here is what I would do")
   - one counterargument addressed honestly
   - `## OUTRO` with what the editor will watch next, no begging for likes
   - 1,200 to 1,800 words, 8 to 12 minutes at 150 words a minute
   - framing is analysis and opinion from a human editor; never medical, legal, or financial advice; never "you should buy/invest/take"
4. `python3 faceless.py script-check work/<id>/script.md`. Fix every PROBLEM and rerun until PASS. Then `python3 faceless.py script-save <id> work/<id>/script.md`.
5. Voice. If `doctor` shows ELEVENLABS_API_KEY set: `python3 faceless.py voice <id>`. Otherwise generate the narration with the ElevenLabs connector (voice id from `config.json`, one generation of the whole narration with the scene texts joined by blank lines), download the audio to `work/<id>/narration.mp3`, and run `python3 faceless.py voice <id> --from-audio work/<id>/narration.mp3`.
6. Key images. Read `work/<id>/audio/timeline.json`. For 6 to 10 scenes that carry the argument (the hook, every scene with a claim, the outro), generate one landscape image each through the ElevenLabs image tool (or Higgsfield if ElevenLabs is unavailable): photographic or editorial illustration, no text in the image, no real or recognizable people, no logos. Save each as `work/<id>/supplied/scene-NN.png` where NN is the two-digit scene index. Generate a thumbnail image with the same tool from the best title (bold single subject, high contrast, no text) and save it as `work/<id>/supplied/thumbnail.jpg`. If image generation is unavailable, continue; stock footage covers the rest, and the render will refuse only if more than half the scenes end up as text cards.
7. `python3 faceless.py visuals <id>` then `python3 faceless.py assemble <id>`. Report the visual mix line.
8. Packaging. Choose the title: rescore the record's candidates with vidIQ if the script changed the angle. Write `work/<id>/metadata.json` with:
   - `title` (under 70 characters, one idea, no clickbait the video does not pay off)
   - `description`: first sentence specific to this video and written by you, then two or three sentences on the argument, then chapters as `MM:SS Title` lines from the timeline scene starts, then `Sources:` with the URLs
   - `tags`: up to 15
   Then `python3 faceless.py metadata <id> work/<id>/metadata.json`.
9. `python3 faceless.py upload <id> --dry-run`, read the body, then `python3 faceless.py upload <id>`. If upload credentials are missing, stop at the dry run, leave the record `assembled`, and say in the summary that the render is ready and credentials are needed (SETUP.md step 4).
10. Summary: the title, scheduled publish time, duration, visual mix, ElevenLabs characters used, the Studio link, and one sentence on what in LEARNINGS.md you applied.
