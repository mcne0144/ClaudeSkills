# Setup: the human checklist

Everything here is a one-time step that only the account owner can do. Each is checked by `python3 faceless.py doctor`. Estimated total: about 90 minutes, plus waiting on YouTube for monetization.

## 1. The channel (10 minutes)

1. Create a new YouTube channel under a Google account you control (a Brand Account is fine). Name it for the niche, not for Bright Matter.
2. Turn on 2-Step Verification for the Google account (a Partner Program requirement).
3. In YouTube Studio, Settings, Channel, Feature eligibility: verify the phone number so custom thumbnails and longer uploads are enabled.
4. Fill `config.json`: `channel.name`, `channel.handle`, `channel.youtube_channel_id` (starts with UC).

## 2. vidIQ (5 minutes)

1. The vidIQ connector is already attached to this Claude account (balance read on 2026-10-27: 2,000 renewable credits a month).
2. Connect the new channel to vidIQ: in a Claude session, ask it to run the vidIQ connect-channel tool and complete the authorization link it returns. The routines use channel analytics, title scoring, outliers and thumbnail generation through it.

## 3. ElevenLabs (5 minutes)

Option A, API key (recommended, gives exact per-scene timing and captions): create a key at https://elevenlabs.io/app/settings/api-keys and store it as the environment variable `ELEVENLABS_API_KEY` in the Claude cloud environment (Settings, Environments, your environment, Environment variables).

Option B, no key: the production routine generates narration through the ElevenLabs connector and passes the file with `--from-audio`; captions are then estimated.

The configured voice is "Brian" (`nPczCjzI2devNBz1zQrb`), chosen from the vidIQ and ElevenLabs voice lists for long-form narration. Change `voice.voice_id` in `config.json` to use another.

## 4. YouTube API credentials (30 minutes)

1. Go to https://console.cloud.google.com, create a project named for the channel.
2. APIs & Services, Library: enable "YouTube Data API v3" and "YouTube Analytics API".
3. OAuth consent screen: User type External, fill the app name and emails, add the scopes `youtube.upload`, `youtube`, `yt-analytics.readonly`, `yt-analytics-monetary.readonly`. Then set the publishing status to **Production**. If it stays in Testing, the refresh token expires every 7 days and the uploader stops silently.
4. Credentials, Create credentials, OAuth client ID, type Desktop app. Note the client id and secret.
5. Set `YT_CLIENT_ID` and `YT_CLIENT_SECRET` in the environment, then run:

```
python3 faceless.py yt-auth-url
```

Open the printed URL while signed in as the channel owner, approve, and copy the `code=` value from the redirect URL (the page will not load; that is expected). Then:

```
python3 faceless.py yt-auth-exchange THE_CODE
```

Store the printed `refresh_token` as `YT_REFRESH_TOKEN` in the environment.

6. Quota: the project starts with 100 uploads a day and 10,000 units for other calls, which is more than this plan uses. No verification is needed for public uploads as of 2026-10-13 (docs/POLICY.md).

## 5. Pexels (2 minutes)

Create a free API key at https://www.pexels.com/api/ and store it as `PEXELS_API_KEY`.

## 6. Music (10 minutes, optional)

Download three to five royalty-free background tracks (YouTube Audio Library or Pixabay Music, both allow monetized use) and commit them under `assets/music/`. With none present the renderer leaves narration unaccompanied.

## 7. Scheduled tasks (created 2026-10-27, one fix needed)

The four routines in RUNBOOK.md exist as Claude scheduled tasks that start fresh cloud sessions, enabled, each reporting by push notification:

| Task | Schedule (America/Chicago) | Id |
|---|---|---|
| Faceless engine: weekly slate | Monday 06:40 | trig_015gbLDNRw7JJZBiTLBVCZEu |
| Faceless engine: production run | Tuesday, Thursday, Saturday 05:40 | trig_01JRnj2qCSwThpYHuqAKNdyH |
| Faceless engine: weekly review | Friday 07:40 | trig_01BLHXRA6znTTMKMAGGZC4aD |
| Faceless engine: monthly strategy review | 1st of the month 08:40 | trig_017rTvXWesLMiG1QA218ov3G |

They were created from a coding session, and the scheduler recorded them with no connectors attached, so the sessions they start have no vidIQ, ElevenLabs, Exa, Higgsfield or GitHub tools. The engine still runs on API keys (steps 3 to 5) and the routines carry fallbacks (`routines/_common.md`), but the live vidIQ signals, title scoring and image generation need the connectors. The fix named by the scheduler: open each task in the claude.ai scheduled tasks list and attach the connectors there (vidIQ, ElevenLabs, Exa, GitHub, Higgsfield), or recreate the four tasks from the claude.ai routines UI with the same prompts, which are stored on each task. The existing "Weekly receipt and subscription sweep" task shows the connector set those UI-created tasks carry.

## 8. Partner Program (when the thresholds are met)

Apply in YouTube Studio, Earn, once the channel has 1,000 subscribers and 4,000 public watch hours in the last 12 months (docs/POLICY.md). Link an AdSense for YouTube account. Then run `python3 faceless.py measure --monetary` in the Friday review so revenue metrics flow.

## 9. The first slate

After steps 1 to 5, open a Claude session in this repo and say: "Run routines/weekly-slate.md now." Approve the ideas you like with `python3 faceless.py approve ID`. The next production run picks them up.
