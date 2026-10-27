# Research: RPM by niche, and what facelessfinder.com actually is (read 2026-10-27)

## Source tiers used here

- T1: a creator's own YouTube Studio figure (screenshot or stated on camera).
- T2: a measured dataset (Studio data across many channels, or aggregated creator disclosures).
- T3: a vendor blog range. Treated as a list of what people claim, not as a verdict.

RPM is the creator's revenue per 1,000 views after YouTube's 45% share. CPM is what advertisers pay per 1,000 monetized impressions and is always higher. Several blogs relabel 2021 CPMs as RPMs (Mark Studios makes this point); those are excluded.

## Long-form RPM by niche

| Niche | Low | High | Source | Tier |
|---|---|---|---|---|
| All niches, anchor | $1.00 | $7.00 | AIR Media-Tech, 300 channels, 3,595 channel-months, Studio data, median $2.30. https://air.io/en/air-data-findings/which-youtube-niche-makes-the-most-money-in-2026-ranked-by-real-rpm-and-cpm | T2 |
| All niches, anchor | | | Virev, median of 73 creator disclosures $4.14. https://virev.ai/_blog/covers/how-much-does-youtube-pay-per-view/youtube-rpm-aggregates-2026.csv | T2 |
| Science explainers (Education & Science) | $2.31 | $19.50 | AIR, median $10.22, highest in the study (URL above) | T2 |
| Personal finance | $11.16 | $15.31 | Virev, p25 to p75 of 11 disclosures, median $12.56 (URL above) | T2 |
| Business & Finance | $0.73 | $5.17 | AIR, median $2.01, fewer than 10 channels (URL above) | T2 |
| Gadgets & Tech | $0.70 | $3.71 | AIR, median $2.33, only 34% of views show an ad (URL above) | T2 |
| AI news and tools | $9 | $9 | One creator, Studio on screen, July 2025, CPM $17. https://starbelo.com/use-case/debby-ai-faceless-channel-rpm-cpm-15k-views/ | T1 |
| AI news | $3.10 | $3.10 | Big AI Reports, own channel, Q1 2026. https://bigaireports.com/2026-youtube-automation-audit/ | T1 |
| Stock market | $4.20 | $4.20 | Big AI Reports, own channel, Q1 2026 (URL above) | T1 |
| History documentary | $6.80 | $6.80 | Big AI Reports, own channel, Q1 2026 (URL above) | T1 |
| Side hustle, software tools | $8.81 | $9.70 | Casper van der Ree, own channel, Oct 2025; sells a course. https://www.youtube.com/watch?v=4aHM6gQnPnM | T1, promotional |
| Sleep history, 2h+ videos | $36 | $36 | Wanner, Dec 2025; sells a course. https://cashcowwanner.beehiiv.com/p/36-rpm-strategy-exposed | T1, promotional |
| Space | $5 | $12 | Hubfluence, Hypika | T3 |
| Animals and wildlife | $0.55 | $1.65 | Dollarpocket (CPM times 0.55, not measured) | T3 |
| True crime | $4 | $10 | Hypika, Autober | T3 |
| Horror stories | $2 | $6 | Hypika, Wick & Reel | T3 |
| Reddit stories | $2 | $6 | Hypika, FluxNote | T3 |
| Motivation and stoicism | $3 | $8 | Hubfluence, FluxNote | T3 |
| Ambient and sleep | $0.40 | $1.50 | YouTubeNiches | T3 |

No measured dataset breaks out true crime, horror, Reddit, motivation, space, animals or sleep; the T3 rows for those are claims.

vidIQ's earnings calculator (a T2 estimator, run 2026-10-27, channel mode, 1,000,000 monthly long-form views, US, English):

| Category | Low | Mid | High |
|---|---|---|---|
| Business | $4,800 | $8,000 | $12,800 |
| Education | $3,600 | $6,000 | $9,600 |
| Technology | $3,000 | $5,000 | $8,000 |
| Entertainment | $1,500 | $2,500 | $4,000 |

Read as RPM: Business $4.80 to $12.80, Education $3.60 to $9.60, Technology $3.00 to $8.00, Entertainment $1.50 to $4.00.

## Shorts versus long-form

- AIR, 274 channels, Studio API, Sep 2026: Shorts RPM is 3% to 14% of long-form; US-audience Shorts $0.328, most niches $0.07 to $0.20. It takes 11,000 to 34,000 Shorts views to earn what 1,000 long-form views earn. https://air.io/en/air-data-findings/youtube-shorts-rpm-vs-long-form-how-much-do-shorts-earn-in-2026 (T2)
- Digiday, Feb 2025: six creators all under $0.20 on Shorts against $3 to $6 long-form. https://digiday.com/media/how-youtube-shorts-revenue-compares-to-long-form-video-revenue-for-creators/ (T1)

Conclusion for this engine: long-form (8 to 12 minutes) is the revenue product. Shorts are a discovery channel only.

## facelessfinder.com, what it is and is not

- Operator not disclosed. No about, contact or founder page. Footer: "Niche intelligence for faceless operators. Data refreshed weekly. Not affiliated with YouTube."
- Pages that exist: `/`, `/report`, `/browser`. `/pricing`, `/api`, `/methodology`, `/about`, `/docs`, `/robots.txt`, `/sitemap.xml` return 404. `/login` and `/signup` return 500.
- Tiers quoted from the home page: Recon $0 (weekly briefing, outlier browser 10 queries a day, top-10 ranking); Operator $12 a month (unlimited browser and filters, saturation and freshness scores, advertiser demand data, CSV export); Lifetime $59 once, 150 seats. "Paid access opens at launch." Paid is not live; there is only a waitlist (`/api/waitlist`).
- No API, RSS, email digest or export today.
- Rising Index, quoted from `/report`: "outlier velocity (50%), winner freshness (30%), and advertiser demand (20%). An outlier is a video doing >=5x its niche's median views-per-day." The home page says 10x. CPC: "We pull real Google Ads cost-per-click data per niche." "Seed demand" is never defined; it reads as monthly search volume for a seed keyword. HIGH, MID and LOW RPM labels carry no dollar values anywhere on the site.
- Staleness: the briefing shown as CURRENT is "WEEK OF 2026-07-05", 16 weeks old on 2026-10-27. The weekly refresh appears to have stopped.

Consequences for the engine:

1. The scanner archives every week it sees and flags a report older than 14 days as stale. A stale report still informs niche selection (the 40-niche taxonomy, RPM tier, CPC) but never supplies topics.
2. Live topic signals come from vidIQ (outliers, rising keywords, trending) in the weekly routine. facelessfinder is a free second opinion, not the primary feed.
3. If facelessfinder resumes weekly updates, the history archive lets the scorer report rising-index deltas week over week.
