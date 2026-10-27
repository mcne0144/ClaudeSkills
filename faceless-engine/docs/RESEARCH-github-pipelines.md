# Research: open-source faceless YouTube pipelines (read 2026-10-27)

Survey of what the public projects agree on, so this engine borrows proven shapes instead of inventing them. Star counts and push dates were read from the GitHub search API on 2026-10-27; READMEs were read raw.

## Repos reviewed

| Repo | Stars | Pushed | Stages | Visuals | TTS | Upload | License |
|---|---|---|---|---|---|---|---|
| [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 135,490 | 2026-10-27 | script, TTS, visuals, assembly, upload | Pexels, Pixabay, Coverr, AI video | Edge, Azure, ElevenLabs, Kokoro, others | Shorts/TikTok/IG publish | MIT |
| [ShortGPT](https://github.com/RayVentura/ShortGPT) | 8,077 | 2025-02-10 | script, TTS, visuals, captions, assembly | Pexels, Bing images | EdgeTTS, ElevenLabs | none | MIT |
| [SaarD00/AI-Youtube-Shorts-Generator](https://github.com/SaarD00/AI-Youtube-Shorts-Generator) | 261 | 2026-10-13 | topic, script, TTS, visuals, assembly, upload | Pexels, 2 clips per scene | edge-tts | Data API v3 OAuth, refresh token | MIT |
| [stickman-video-director](https://github.com/kaomei/stickman-video-director) | 3,121 | 2026-10-25 | script, storyboard, TTS, illustrated scenes, captions, render; long-form first | AI illustrations, Ken Burns | unnamed | none | MIT |
| [xbrxr03/content-factory](https://github.com/xbrxr03/content-factory) | 4 | 2026-06-02 | script, voice, edit plan, visuals, render, thumbnail, upload; 8 to 12 min documentary | ComfyUI images | Piper (offline) | Data API v3 OAuth, scheduled | MIT |
| [mmagdyelsafty/faceless-video-pipeline](https://github.com/mmagdyelsafty/faceless-video-pipeline) | 4 | 2026-03-04 | script split, slides, ducking, assembly, SRT, A/B thumbnails, metadata | HTML slides via Playwright | recorded VO | none | MIT |
| [lymcho/story-to-video](https://github.com/lymcho/story-to-video) | 0 | 2026-02-27 | TTS chunked, mix, cover, assembly, upload, localize | DALL-E cover | OpenAI TTS | OAuth, playlist, daily schedule | MIT |
| [jansencruz23/faceless-youtube-factory](https://github.com/jansencruz23/faceless-youtube-factory) | 10 | 2026-02-12 | script, casting, audio, compose, upload (LangGraph) | gameplay, AI images | Edge-TTS | Data API v3 OAuth | MIT |
| [Dark2C/Viral-Faceless-Shorts-Generator](https://github.com/Dark2C/Viral-Faceless-Shorts-Generator) | 118 | 2026-05-10 | trends, script, approval gate, TTS, forced-aligned captions, assembly | local clips | Piper | none | unstated |
| [sasharun/awesome-faceless](https://github.com/sasharun/awesome-faceless) | 48 | 2026-07-11 | directory of 80+ tools | | | | CC0 |

## Consensus architecture

Every project converges on one linear chain with the same boundaries: topic, script as a structured scene list, TTS per scene or chunk, visual fetch per scene, ffmpeg assembly, captions, metadata and thumbnail, upload. The boundary that matters most is the scene-level script object: scene text, visual keywords, and the audio duration measured from the TTS file. Duration flows from audio, never the other way. A file-backed artifact between every stage makes each stage re-runnable on its own.

## Patterns this engine copies

- Scene splitting with two visual keywords per scene and a fallback chain when stock search returns nothing.
- ffmpeg xfade between scenes, yuv420p and faststart on output.
- Captions from the TTS provider's own timestamps (ElevenLabs returns character alignment), burned in with the subtitles filter. No Whisper download.
- Sidechain ducking of music under narration.
- YouTube Data API v3 with a stored refresh token, private by default, scheduled publishAt.
- Idempotent state: check for each stage's artifact before regenerating, write JSON then rename, per-video record, queue with explicit statuses.
- An approval gate before the paid stages (voice, render) so a bad script never costs money.
- A used-asset ledger so the same stock clip is not reused across videos (MoneyPrinterTurbo issues #953, #615, #479, #149).

## Documented pitfalls

- YouTube Data API: an upload costs 1,600 quota units of a 10,000 per day default, so about six uploads per day per project. An unverified Google Cloud project uploads as private only. An OAuth consent screen left in Testing mode expires refresh tokens after 7 days (SaarD00 README).
- LLM rate limits (MoneyPrinterTurbo issues #202, #203, #208, #339): back off and retry.
- Audio and video desync when clip order or length is derived from anything but the narration audio (MoneyPrinterTurbo #1019, fixed in #1702).
- Empty stock results: every stock-based project warns of it.
- TTS cost: roughly $0.50 per short on ElevenLabs (dev.to write-up); a 10 minute AI-visual pass can cost tens of dollars with retries (stickman README).
- Edge-TTS is free but fails silently behind proxies.

## Best bases for 8 to 15 minute explainers

1. content-factory for the operational core (agent per stage, artifact resume, atomic state, queue with leases, scheduled upload).
2. faceless-video-pipeline for the long-form craft layer (3 minute segments, intro and outro join, ducking, chaptered descriptions, A/B thumbnails).

MoneyPrinterTurbo is worth mining for provider adapters, not as a base: it is Shorts-first and its tracker shows the repetition and sync problems that get worse at long durations.
