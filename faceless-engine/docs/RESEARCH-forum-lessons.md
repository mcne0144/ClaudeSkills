# Research: forum lessons on faceless channels (read 2026-10-27)

Source threads were pulled through the Apify Reddit scraper (271 posts and comments) plus two Hacker News and one Indie Hackers thread. Everything here is anecdote. Promotional posters are flagged. Where several independent posters agree it is marked "repeated".

## Niche choice

- Niche matters more than tools. Bookmark 5 to 10 channels under 1,000 subscribers that get outsized views in your candidate niche before committing. (r/aitubers 1uql5vq, OP, 309 upvotes; OP later promotes BuildTuber. Repeated across threads.)
- "$2 RPM vs $20 RPM from the exact same views." Ask three questions: can I make 100 videos faceless, are people already watching this, is there a path to money. Target US, UK and Canada viewers aged 40 to 60 for RPM. (r/aitubers 1wpuj8o, OP summarizing 15 guru videos; repeated by HN posters.)
- Reported numbers: an 85k-subscriber channel at about $900 a month AdSense against $2,500 affiliate and $3,000 brand deals (HN 35840097, one person); "$5 per 1,000 views" on a 14-month faceless long-form channel at 75k subscribers (r/PartneredYoutube 1q4p5qo, one person); psychology long-form, US audience, "$3 to $6" RPM (1uql5vq OP).
- Avoid: motivation and stoicism (saturated), luxury lifestyle (cooling), top-10 and did-you-know, "1000 AI images" compilations, anything without a repeatable format. (r/ReelFarmer 1rveed8, OP is the aituber.app founder, promotional; corroborated by an HN poster who failed in gaming, motivation and meditation music.)

## Cadence and time to traction

- "Faceless channels DO WORK but not in 20 to 40 videos." OP took 4 months to earn, posts about 3 times a week after 4 to 5 years, says quality beats daily posting; pick Shorts or long-form, not both, for the first 4 months. (r/passive_income 1ro6ciq, OP, 136 upvotes; quality over quantity repeated.)
- Treat the first 20 to 30 uploads as education; expect 3 to 6 months of near-zero views and 6 to 12 months to traction; one guru admits "hundreds of failed channels". (1uql5vq OP; 1wpuj8o OP; repeated.)
- Counter-anecdotes: a creepy-story narration channel monetized in a month; another claims 150k subscribers on about 3 uploads a month. (1q4p5qo, single posters.)
- Failure data points: 26 videos to reach 100 subscribers (Indie Hackers); 54 templated Shorts in a month for 100 subscribers (1uirvc8 commenter).

## Retention and packaging

- "People don't click videos. They click ideas." One idea per title and thumbnail; the first 30 seconds decide retention; copy title formats, not titles. (1uql5vq OP; echoed in 1wpuj8o.)
- Format lock-in: a consistent hook, pacing and visual identity so the algorithm knows who to show it to. (1ro6ciq commenter, one person.)
- Keep a per-upload log: title promise, 30-second retention, drop points, impressions against clicks, to tell "not shown" from "clicked then bailed". (1wpuj8o commenter promoting embertube, vendor flag. The idea is sound and is what `state/videos/*.json` metrics snapshots record.)
- Start with images and quick cuts, not AI video; use AI video only where it adds value. (1uql5vq OP and a commenter.)

## What got channels demonetized in the January 2026 wave

- A scrolling-text story channel, one upload a day, ElevenLabs narration, original scripts, demonetized for "Inauthentic content: Content that appears mass-produced or repetitive", $13k withheld; OP suspects "Part 2" videos reusing identical titles and thumbnails. (r/aitubers 1q65n5b, OP.)
- Also hit: Suno music videos with heavy AI visuals; a lore explainer with a unique AI image every 3 to 7 seconds (3,200 EUR withheld); a researched story channel over background gameplay; a 500k-subscriber channel. Appeals answered with the same canned letter. (1q65n5b, multiple posters.)
- Commenter consensus on causes: visuals that look templated (scrolling text, static slideshows), identical thumbnails across parts, reused generic descriptions. Suggested fixes: visibly hand-edited video, a unique first sentence in each description documenting the human workflow, no edits to existing videos mid-appeal. (1q65n5b, repeated by 4 or more posters.)
- One flagged channel puts every channel on the account at risk. (1uql5vq OP.)
- Fully automated n8n pipelines with no human in the loop "get you demonetized or shadowbanned". (1wpuj8o OP.)
- AI voiceover over reused clips is not automatically transformative; add commentary, structure and analysis. (1uql5vq OP.)

## Economics

- Per-video cost reports: $35 to $55 long-form (1uirvc8 OP, the OpenVidi founder, largely an ad); about 16 AUD on a self-built Claude plus ElevenLabs pipeline; about $100 a video with about 12 videos to break even for an experienced operator, 35 for beginners (vidIQ interview, promotional).
- "Faceless isn't a strategy, it's a production constraint." Tutorial makers often earn more teaching than running channels; survivorship bias is heavy. (1wpuj8o top comment.)
- Sponsors are harder without a face; the money is often in affiliates and deals, not AdSense. (1q4p5qo commenters; HN 35840097.)

## What this engine takes from it

1. One niche, one format, long-form only for the first four months.
2. Budget for 30 videos before judging; measure from video 10 onward.
3. Hook under 60 words, one idea per title, title format study from outliers every week.
4. Visual variety is a monetization requirement, not polish: mixed stock footage, AI images with motion, capped text cards, no scrolling text.
5. Unique thumbnail and unique first-sentence description on every upload, enforced in code.
6. A human approves every script and every upload. The engine does the labor; it does not remove the editor.
