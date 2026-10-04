# 08 · AI Production Toolkit (state of the art, October 2026)

Knowledge file for the Bright Matter art-direction agent. Covers generative image, video, avatar, voice, 3D, upscaling, relighting and motion-control tools as of 2026-10-03, then prompt craft, consistency systems, mascot workflow, and the legal and ethics layer.

## How to read this file

- **Source tiers** appear in brackets after every version, date, price, spec or figure:
  - **[P]** primary: vendor docs, vendor blog, official release notes, government or standards body text.
  - **[I]** independent test: a third party ran the same inputs through several tools.
  - **[R]** single reviewer or vendor-affiliated comparison (treat as a lead, not a verdict).
  - **[A]** aggregator or trade press summarizing others.
- **Vendor quality claims are labeled as claims.** "Most realistic", "#1", "state of the art" are marketing until an independent test agrees.
- **Blank beats plausible.** Where a fact could not be confirmed, it is left out. If a tool shows a newer version than listed here, trust the tool.
- **Connector reality check (2026-10-03).** The Higgsfield connector's live model list was queried for this file. Models it exposes are marked **HF hub**. That list is the fastest way to know what Shannon can actually run today: `models_explore(action:"list")` [P].
- The model market moves monthly. Re-verify versions before quoting them to a client.

## The landscape in one screen

| Job | First reach (Oct 2026) | Why | Watch out |
|---|---|---|---|
| Hero still, editorial taste | Midjourney V8.2 | Aesthetic default, native 2K `--hd` | V8.x has no Omni Reference; use Edit Model or V7 |
| Text-heavy poster, packaging, signage | Ideogram 4 / 4.5, GPT Image 2.5, Nano Banana Pro | Layout and type fidelity | Always proof every letter |
| Brand-consistent product variants | FLUX.2 / FLUX 3 Image, Nano Banana 2, Seedream 5.0 Pro | Multi-reference (10+ refs) | Reference drift on fine logos |
| Vector logo, icon set, SVG illustration | Recraft V4 / V4.1 Vector | Native editable SVG | Path count, cleanup still needed |
| Commercially indemnified asset | Adobe Firefly Image Model 5, Firefly Custom Models | Adobe "commercially safe" positioning | Partner models in Firefly are not covered the same way |
| Cinematic shot with audio | Veo 3.1, Gemini Omni Flash, Kling 3.0, Seedance 2.0/2.5 | Native audio, references | Clip length, physics, hands |
| Edit existing footage | Runway Aleph 2.0, Gemini Omni (conversational), Kling 3.0 Omni Edit | Video-to-video with continuity | Detail swim on fine text |
| Talking presenter | HeyGen Avatar V, Synthesia Express-3 | Lip sync, long form | Consent capture is mandatory |
| Voice and VO | ElevenLabs Eleven v4 / v4 Turbo | Expressive tags, 90+ languages | Voice clone consent and disclosure |
| Product or mascot to 3D | Meshy 7.1, Tripo P2.0, Rodin Gen-2.5, Higgsfield `generate_3d` | GLB fast, rig options | Topology and UVs need a pass |
| Upscale AI video | Topaz Starlight / Astra | Temporal stability | Over-smoothing skin |

## Image models

### Midjourney (V7, V8, V8.1, V8.2, Niji 7, Video V1)

- **Facts**
  - V7 released April 3, 2025; default from June 17, 2025 to June 9, 2026; introduced Draft Mode and Omni Reference (`--oref`) (Midjourney docs, Version page [P]).
  - V8 alpha opened March 17, 2026 with `--hd` native 2K and `--q 4` (Midjourney update post [P]).
  - V8.1 released April 14, 2026; default June 10 to July 23, 2026 (PixMind comparison citing Midjourney docs [R]).
  - **V8.2 is the current default as of July 24, 2026**; adds an "Edit Model" that replaces Omni Reference, Character Reference and Retexture (Midjourney docs, Version page [P]).
  - Omni Reference works with V7, not V8.1 or V8.2; Niji 7 sits on the V7 side of the compatibility table (PixMind [R], consistent with the docs note that Edit Model replaced oref [P]).
  - Video V1 (June 18, 2025): image-to-video, four 5-second clips per job, extend in 4-second steps, `--motion low|high`, `--loop`, `--end`; 480p SD with 720p HD on Standard and above (Midjourney update and Video docs [P]).
- **Best at**: taste. Lighting, texture, fashion, editorial and moodboard work where nobody has written the art direction yet. Style references (`--sref`), moodboards and personalization profiles carry across V7 and V8 (V8 alpha post [P]).
- **Known weakness**: precise layout, exact copy, and multi-element brand compliance. Not an API-first tool, so it does not slot into automated pipelines. Video V1 is short and low resolution versus Veo, Kling or Seedance.
- **Prompting technique**
  - Write like a photographer's caption, not a keyword list. Subject, setting, light, lens, mood.
  - Lock look with `--sref` codes and a personal moodboard; lock subject with V8.2's Edit Model, or drop to V7 with `--oref` when a mascot or product must hold.
  - Use `--raw` to reduce Midjourney's house style when the brand style must dominate.
  - Use Draft Mode (V7) to explore 20 to 40 compositions cheaply, then re-render the keeper.
  - `--chaos` for exploration rounds, low or zero for production rounds.

### OpenAI GPT Image (gpt-image-1, GPT Image 2, Images 2.5 Flare and Sunburst)

- **Facts**
  - `gpt-image-1` reached the API April 23, 2025, carries C2PA metadata, and launched at roughly $0.02 / $0.07 / $0.19 per low / medium / high square image (OpenAI blog and dev forum [P]).
  - `gpt-image-2` launched April 21, 2026: up to 2K, more aspect ratios, stronger text and layout, a "thinking mode" for self-checking (OpenAI dev forum announcement [P]).
  - **ChatGPT Images 2.5** launched September 8, 2026 with two API models: **GPT-Image-2.5 Flare** (default, OpenAI claims higher quality than GPT Image 2 at 50% lower latency) and **GPT-Image-2.5 Sunburst** (precision edits, longer generation) (OpenAI announcement [P]). The API guide lists `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare` with quality tiers up to "xhigh" and "max" and an "opaque" background option (OpenAI docs and dev forum changelog [P]).
  - GPT Image 2 and 2.5 are both on the **HF hub** [P]; GPT Image 2 is also inside Adobe Firefly with 10 aspect ratios as of September 2026 (Adobe community "What's new" [P]).
- **Best at**: instruction following, conversational multi-turn edits, infographics, UI mockups, product-in-scene composites, readable text.
- **Known weakness**: a recognizable "GPT look" (warm, slightly glossy) unless pushed; content moderation can refuse legitimate brand work involving real people; Sora (OpenAI video) is gone (see video section), so OpenAI is image-only for Bright Matter purposes.
- **Prompting technique**
  - Talk to it like a junior designer: "Make the headline 20% smaller, move the product left, keep everything else identical."
  - For edits, say what must NOT change. Sunburst exists for tight, iterative edits.
  - Put literal copy in quotes. Specify font category, weight, case, and placement.
  - Request transparent background for cutouts (supported since gpt-image-1 [P]).

### Google Gemini image: Nano Banana, Nano Banana Pro, Nano Banana 2, Nano Banana 2 Lite

- **Facts**
  - Nano Banana (Gemini 2.5 Flash Image) launched August 2025 (Google blog referencing it in the Nano Banana 2 post [P]).
  - **Nano Banana Pro (Gemini 3 Pro Image)**, November 20, 2025: up to 4K, multilingual text rendering, up to 14 input images (varies by surface), grounding with Google Search, SynthID watermark (Google blog and developer blog [P]).
  - **Nano Banana 2 (Gemini 3.1 Flash Image)**, February 26, 2026: Pro-level quality at Flash speed; replaced Pro as the default across the Gemini app, Search, AI Studio, Vertex and Flow; Pro stays available to paid subscribers via "Redo with Pro"; outputs carry SynthID and C2PA Content Credentials (Google blog [P]).
  - **Nano Banana 2 Lite**, June 30, 2026: fastest, cheapest Gemini image model for high throughput (Google developer blog [P]).
  - Inside Firefly: Nano Banana 2 listed among 30+ models (Adobe blog, March 2026 [P]). On the **HF hub**: Nano Banana, Pro, 2 and 2 Lite [P].
- **Best at**: world knowledge (real places, objects, diagrams), infographics, character consistency across edits, multi-image blending, fast iteration. Pro for the hardest text and layout.
- **Known weakness**: Google's own prompt guide flags limitations in text rendering, factual accuracy and fine detail (Google prompting tips [P]). Independent typography test: designers picked Nano Banana 2 first 30.0% of the time vs Ideogram 4 at 47.9% (ContraLabs blind test, published by Ideogram, so vendor-affiliated [R]).
- **Prompting technique** (Google's guidance plus practice)
  - Specify subject, composition, action, location, style, then camera angle and lighting (Google prompting tips [P]).
  - Feed reference images and name them in the prompt by role: "Image 1 is the product, Image 2 is the lighting reference."
  - For diagrams and infographics, give the facts explicitly; do not rely on grounding for client claims.
  - Use Pro (or "Redo with Pro") for final text-heavy frames, Nano Banana 2 for volume.

### Black Forest Labs FLUX (Kontext, FLUX.2, FLUX 3)

- **Facts**
  - FLUX.1 Kontext launched May 29, 2025: in-context generation and editing, [pro] and [max] (Business Wire release [P]).
  - **FLUX.2**, November 25, 2025: up to 10 reference images, 4MP editing, improved typography; variants [pro], [flex], [dev] (32B open weights, commercial license required), [klein] (Apache 2.0 planned) and later [max] with grounded web context (BFL blog and model page [P]).
  - **FLUX 3**, announced July 23, 2026 as a multimodal image, video and audio model; FLUX 3 Video in early access first (BFL blog [P]).
  - **FLUX 3 Image** released around October 1 to 2, 2026: multi-step edits that leave the rest of the image alone, bounding-box composition, up to 10 references, up to 4K; open weights "in the coming weeks" (The Decoder [A]). FLUX 3 Image, Video and Video Edit are already on the **HF hub** [P].
  - FLUX models power features in Adobe Photoshop and are being tested by Canva, Krea and Picsart (BFL press release [P]).
- **Best at**: photoreal product and lifestyle imagery, multi-reference consistency (product + model + setting), and self-hostable open weights for custom fine-tunes.
- **Known weakness**: style range is narrower than Midjourney's; open-weight licenses differ by variant, so check before client use.
- **Prompting technique**
  - FLUX responds well to plain, structured descriptions; BFL lists a JSON-based control system and hex-color control on FLUX.2 (BFL model page [P]).
  - Assign each reference a job ("use the bottle from ref 1, the hand pose from ref 2").
  - Use bounding boxes (FLUX 3 Image) for layouts that must match a template.

### Ideogram (3.0, 4.0, 4.5)

- **Facts**
  - **Ideogram 4.0**, June 3, 2026: 9.3B open-weight model trained on structured JSON captions; bounding-box layout `[y_min, x_min, y_max, x_max]` on a 0 to 1000 grid; up to 16 palette hex colors per image and 5 per element; native 2K (Ideogram press release and technical blog [P]).
  - License caution: the press release says "open weights under a commercial license", while the Hugging Face model card lists the downloadable nf4/fp8 checkpoints under an "Ideogram 4 Non-Commercial" license (Ideogram press release and HF card [P]). Treat self-hosted commercial use as needing a separate license until confirmed.
  - Blind typography evaluation by ten Contra designers: Ideogram 4 first-place 47.9%, Nano Banana 2 30.0%, FLUX.2 [max] 15.5%, Grok Imagine 1.0 15.0%; "would you use this in client work" 3.55/5 vs 2.84 for Nano Banana 2 (published by Ideogram [R]).
  - **Ideogram 4.5**, September 30, 2026: "Precise Edit" model aimed at multi-turn editing without artifact buildup; up to five source images; open weights promised without a date (Ideogram post quoted by Creative AI News and others [A]). On the **HF hub** [P].
  - Ideogram claims 95% text accuracy on its features page (vendor claim [P]).
- **Best at**: the words. Posters, event graphics, packaging copy, signage, multi-line type, multilingual scripts.
- **Known weakness**: anatomy and over-tight crops on figurative prompts; aspect-ratio adherence reported imperfect (Venice model page summarizing third-party tests [A]).
- **Prompting technique**
  - Use the JSON structure: a `high_level_description`, a `background`, then `elements` each typed `text` or `obj`, with `text` holding the literal string and `desc` holding the styling (Ideogram technical blog [P]).
  - Pin headline, date and CTA with bbox; leave decorative elements descriptive.
  - Pass the brand palette as hex codes, not adjectives.
  - Render at the highest quality tier for type-dense finals; low tiers drift on small copy (Runware guide [A]).

### Recraft (V3, V4, V4.1, V4 Styles)

- **Facts**
  - **Recraft V4**, February 2026: four variants, V4 (1024px raster), V4 Vector, V4 Pro (2048px), V4 Pro Vector; exports SVG, PNG, JPG, PDF, TIFF and Lottie (Recraft docs [P]).
  - V4.1 family appeared on partner platforms by June 2026 with six variants (Kolbo blog [A]). V4 Styles Pro Vector listed with release date August 13, 2026 (Runware model docs [A]). V4.1 is on the **HF hub** with `model_type` for vector logos and icons [P].
  - Vendor claim: "the only model capable of generating editable, production-quality SVG" (Recraft docs [P]).
- **Best at**: real vector output for logos, icon systems, spot illustrations, pattern and packaging graphics; reusable style references that keep an icon family consistent.
- **Known weakness**: generated SVGs still need path cleanup, color-count reduction and grid alignment before they become a brand mark. Never ship an AI logo as final identity without human redraw (see copyright section).
- **Prompting technique**
  - Specify shape language ("geometric, 2px stroke, rounded joins, no gradients"), color count, and use case ("app icon at 24px").
  - Build an icon set from one approved icon used as style reference.
  - Open in Illustrator or Figma, simplify paths, snap to grid, re-color to tokens.

### Adobe Firefly (Image Model 5, Custom Models, Boards, partner models)

- **Facts**
  - **Firefly Image Model 5** announced at MAX, October 28, 2025: native 4MP, prompt-based editing ("Prompt to Edit"), "commercially safe" (Adobe newsroom [P]); generally available by March 19, 2026 (Adobe blog [P]).
  - **Firefly Boards**: public beta June 2025, worldwide launch September 24, 2025 with Presets, Generative Text Edit (beta) and Describe Image; Rotate Object (2D to 3D posing) added at MAX 2025 (Adobe blog and newsroom [P]).
  - **Firefly Custom Models**: private beta at MAX 2025, public beta March 19, 2026, trained on images you have rights to, private by default (Adobe [P]).
  - **Firefly AI Assistant** (agentic, runs workflows across Creative Cloud apps) announced April 15, 2026, public beta "in the coming weeks" (Adobe newsroom [P]).
  - Partner models in Firefly include Nano Banana 2, Veo 3.1, Runway Gen-4.5 and Aleph 2.0, Kling 3.0 and 3.0 Omni, Luma Ray3.14, FLUX.2 [pro], ElevenLabs Multilingual v2, Topaz Astra, GPT Image 2 (Adobe newsroom April 2026, Adobe partner page, community post September 2026 [P]).
- **Best at**: the safest licensing story for brand clients (Adobe's own models), Boards as a shared moodboard and concept space, direct handoff into Photoshop and Premiere.
- **Known weakness**: Firefly-native aesthetics are more conservative than Midjourney's. "Commercially safe" applies to Adobe's own models; partner-model outputs inside Firefly carry the partner's terms. Confirm before promising indemnity.
- **Prompting technique**
  - Use Boards for divergent rounds (generate across several models side by side), then pin winners.
  - Use Describe Image to reverse-engineer a reference into an editable prompt.
  - Train a Custom Model on the client's approved photography for on-brand series work.

### ByteDance Seedream (4.0, 4.5, 5.0 Lite, 5.0 Pro)

- **Facts**
  - Seedream 4.0, September 9, 2025: unified generation and editing (ByteDance Seed blog [P]).
  - Seedream 4.5: stronger multi-image editing and dense text (Seed model page [P]).
  - Seedream 5.0 Lite, February 13, 2026: reasoning, real-time search enhancement (Seed blog [P]).
  - **Seedream 5.0 Pro**, July 8, 2026: complex infographics, high-density text, localized and controllable editing; ByteDance itself notes room to improve fine text and pixel-level edit consistency (Seed blog [P]).
  - 4.5, 5.0 Lite, 5.0 Flash and 5.0 Pro are on the **HF hub** [P].
- **Best at**: e-commerce product imagery, multi-reference composites, infographic layouts at volume and low cost.
- **Known weakness**: self-described limits on fine text and pixel-level consistency (above). Training-data and likeness questions follow ByteDance models (see Seedance).
- **Prompting technique**: give the product image as reference, describe the set and lighting, request the edit as an instruction ("replace background with marble counter, keep label sharp").

### Others on the hub worth knowing

- **Higgsfield Soul 2.0 / Soul Cinema / Soul ID**: fashion and UGC aesthetic model with presets, Moodboards, Soul HEX palette control; Soul ID trains a face from 20 to 80 photos and works across the Soul family; not exportable (Higgsfield help center [P]). Use for influencer-style and lifestyle shoots.
- **Grok Image 2.0**, **Kling O1 Image**, **Z Image**, **Wan** models are also on the hub [P]. No independent quality data gathered here.

## Video models

### Status changes that matter first

- **OpenAI Sora is gone.** The Sora app and website ended April 26, 2026 (OpenAI note on the Sora 2 page [P]). The Sora 2 API was switched off September 24, 2026 with no replacement listed (developer reports citing OpenAI's deprecations page [A]). Remove Sora from any workflow or proposal.
- **Veo 4 does not exist** as of this file. Google's I/O 2026 video launch was **Gemini Omni** instead (Google blog [P]); rumor pages about Veo 4 are not sources.
- **Kling 4.0** was announced September 28, 2026; Flash variant for Ultra Yearly only, full release "October", 4K 10-bit HDR "coming soon" (TechTimes, Modellix [A]). Do not promise 4K Kling output to clients yet.

### Google Veo 3.1 and Gemini Omni Flash

- **Facts**
  - Veo 3 debuted at I/O May 2025 with native audio; **Veo 3.1** and Veo 3.1 Fast, October 15, 2025: richer audio, better image-to-video adherence, Flow features "Ingredients to Video", "Frames to Video" (first/last frame) and "Extend" (Google blog [P]).
  - January 13, 2026 update: improved Ingredients to Video, native 9:16 vertical, upscaling to 1080p and 4K on Flow, API and Vertex only (Google blog [P]).
  - **Gemini Omni Flash**, May 19, 2026: any-input video generation (text, image, audio, video) plus conversational video editing; SynthID watermark; rolled out to the Gemini app, Flow and YouTube Shorts (Google blog [P]). API preview June 30, 2026 at $0.10 per second of output, "the same as Veo 3.1 Fast" (Google developer blog [P]). Omni replaces Veo in the Gemini app (Gemini overview page [P]). Model card covers Omni Flash and Omni 1.1 Flash (DeepMind model card, Aug 2026 [P]).
  - Veo 3, Veo 3.1, Gemini Omni Flash and Omni Flash 1.1 are on the **HF hub** [P].
- **Best at**: Veo 3.1 for cinematic realism with synchronized dialogue and SFX; Omni for iterative "change this, keep that" edits to a clip, mixed-media inputs, and fast vertical social.
- **Known weakness**: short clip units; text on objects can swim; Ingredients mode can loosen product fidelity. Verify logos frame by frame.
- **Prompting technique**
  - Veo follows full shot grammar well (see Prompt Craft). Put dialogue in quotes and name who says it; describe ambient sound and SFX separately.
  - Use first/last frame to control where a move ends (product lockup on the final frame).
  - With Omni, iterate in conversation: one change per turn, restate what stays fixed.

### Runway (Gen-4, Gen-4.5, Aleph, Aleph 2.0, Act-Two)

- **Facts**
  - Gen-4.5, December 1, 2025: vendor reported #1 on the Artificial Analysis text-to-video leaderboard at 1,247 Elo vs Veo 3 1,226, Kling 2.5 1,225, Sora 2 Pro 1,206 at release (Runway research post [P], leaderboard is independent [I] but rankings move).
  - **Aleph 2.0**, June 2, 2026: video editing model for localized edits, single-frame guidance, consistency across cuts, clips up to 30 seconds at 1080p (Runware model docs [A]; Adobe partner page confirms Aleph 2.0 in Firefly [P]).
  - Runway is researching real-time generation built on Gen-4.5 (Runway news, September 10, 2026 [P]).
  - Credit costs reported by one reviewer: Gen-4.5 12 credits/sec, Aleph 15, Gen-4 Turbo 5; API $0.01 per credit (AIUnpacking review [R]).
- **Best at**: Aleph for post-production on real footage (relight, swap product, change weather, remove objects, new camera angle). Act-Two for driving a character with a phone performance video. Gen-4.5 for controllable, cinematic generation.
- **Known weakness**: not on the HF hub list queried today; budget separately. Fine typography on packaging may drift in Aleph edits.
- **Prompting technique**: for Aleph, describe the edit as a delta ("change the sky to overcast dusk, keep the actor and wardrobe unchanged"); edit one keyframe and let it propagate where offered.

### Kling (2.5 Turbo, 2.6, O1, 3.0, 3.0 Omni, 4.0 announced)

- **Facts**
  - **Kling 3.0**, February 5, 2026: Video 3.0, Video 3.0 Omni, Image 3.0, Image 3.0 Omni; up to 15 seconds; native multilingual audio; reference video plus multiple image references for consistency; built on Kling O1 and 2.6 (Kuaishou press release [P]).
  - Multi-shot storyboards up to 6 cuts and native 4K/60fps claims come from partner write-ups (BestPhoto, GenMediaLab [A]); verify in-app.
  - Kling 4.0 status: see above [A].
  - Kling 2.6, 3.0, 3.0 Turbo, 3.0 Omni Edit and 3.0 Motion Control are on the **HF hub** [P]; Kling 3.0 and 3.0 Omni are in Firefly (Adobe [P]).
- **Best at**: human motion, dance, action, physical interaction; Motion Control (transfer a reference performance onto a character); multi-shot sequences.
- **Known weakness**: hard cuts within one generation can break continuity of small props; lip sync across languages varies.
- **Prompting technique**: one action verb per shot; describe camera move explicitly; for Omni, upload character and product as Elements and name them in the prompt.

### Luma (Ray3, Ray3.14, Ray3.2)

- **Facts**
  - Ray3, September 18, 2025: "reasoning" video model, native 16-bit HDR in ACES2065-1 EXR, Draft Mode (vendor claims) (Luma news [P]).
  - Ray3.14, January 26, 2026: native 1080p, vendor claims 4x faster and 3x cheaper at 720p than Ray3; character References not supported in 3.14 (Luma news [P]).
  - **Ray3.2**, June 9, 2026: frame-level control, first public Ray API (Luma news [P]).
- **Best at**: HDR/EXR deliverables for grading, animation-style stability, video-to-video "Modify".
- **Known weakness**: not on the HF hub list today; character references missing in 3.14.
- **Prompting technique**: explore in Draft Mode, then master; supply keyframes for start and end; grade the EXR in Resolve rather than baking a look into the prompt.

### MiniMax Hailuo and H3

- **Facts**: Hailuo 02, June 18, 2025, 1080p up to 10 s; Hailuo 2.3 and 2.3 Fast followed (MiniMax release notes [P]). **MiniMax H3**, July 31, 2026: omni-modal video with native stereo audio, up to 2K and 15 s, open-sourced August 3, 2026; vendor claims 2K pricing under a third of mainstream models (MiniMax news [P]). Hailuo, H3 and H3 Max on the **HF hub** [P].
- **Best at**: facial emotion and natural physics (Higgsfield hub description [P]); low cost per second for volume.
- **Known weakness**: open checkpoints need the closed regeneration API to match full 2K quality (MiniMax HF card [P]).

### ByteDance Seedance (1.5 Pro, 2.0, 2.5)

- **Facts**
  - **Seedance 2.0**, February 12, 2026: unified audio-video generation from text, image, audio and video inputs (ByteDance Seed [P]). Launch triggered controversy over realistic renderings of real people without authorization (Global Times summarizing Reuters, Bloomberg coverage [A]).
  - **Seedance 2.5**, July 31, 2026: 30-second single-pass audio-video, built for long-form storytelling, reference control and editing; rolled out first on China-market apps with API "coming soon" via BytePlus (ByteDance Seed blog [P]). Up to 50 reference inputs and clay-render (grey 3D blocking) referencing per launch coverage (Digital Applied [A]).
  - Seedance 2.0, 2.5 and Ad Multiplier (powered by 2.5) are on the **HF hub** [P]. Higgsfield **Cinema Studio 4.0** runs on Seedance 2.5 with up to 50 references and 30-second clips (Higgsfield help center [P]). HeyGen Video Agent uses Seedance 2.0 as an engine beside Avatar V (HeyGen blog [P]).
- **Best at**: reference-driven ads (product + character + location + temp score in one job), long single takes, multi-SKU variation.
- **Known weakness**: likeness and IP guardrails are weaker in public perception; never feed real people or third-party IP without rights. Access path for 2.5 outside China is via partners such as Higgsfield.
- **Prompting technique**: treat references as a cast and crew list; block the scene with clay renders or a rough 3D layout when camera path matters.

### Higgsfield as hub (what it adds beyond models)

- **Cinema Studio** versions 2.0 to 4.0: camera rig with sensor profile, lens, focal length 12mm to 135mm, aperture; genre, era (60s to 2020s), tempo (Single Shot to Chaotic), 50+ grade templates, lighting presets; speed-ramp presets (Linear, Flash In, Flash Out, Slow-mo, Bullet Time, Impact, Ramp Up) in 3.0; Claude Chat "AI Director" in 3.5 (Higgsfield help center [P]).
- **Elements** system for reusable characters, locations, props; **Soul Cast** actors (Higgsfield [P]).
- **Genjutsu** motion transfer and object replacement; Kling 3.0 Motion Control (HF hub [P]).
- **Marketing Studio**, **Ad Multiplier**, **virality predictor**, **upscale**, **reframe**, **relight_image**, **outpaint**, **generate_3d** (connector tool list [P]).
- Agent rules for Shannon's connector: browse presets freely, but only execute after explicit approval; for multi-step videos call `get_workflow_instructions` first; character sheets only on explicit request (Higgsfield MCP instructions [P]).

## Avatar and voice

### HeyGen

- **Facts**
  - **Avatar V**, April 8, 2026: trained from a 15-second reference video; separates identity and motion so new outfits and settings keep your real gestures; vendor claims stable long form beyond 30 minutes; same cost as Avatar IV at 20 Premium Credits per minute (HeyGen blog, research post, webinar recap [P]).
  - Avatar V requires a combined consent recording with a security code (HeyGen webinar recap [P]); the connector exposes `create_avatar_consent` before `create_digital_twin` [P].
  - API: Avatar V is opt-in per look via `"engine": {"type": "avatar_v"}`; `expressiveness` control remains Avatar IV only (HeyGen developer docs [P]).
  - Video Agent composes Seedance 2.0 cinematic shots with Avatar V scenes from one prompt (HeyGen blog [P]).
- **Best at**: founder and spokesperson videos, localized versions via translation, explainer and training video, UGC-style talking heads (with disclosure).
- **Known weakness**: hands and teeth historically; HeyGen says Avatar V fixed teeth drift seen in IV (webinar [P]). Still read as avatars in close-ups.
- **Technique**: record the reference in the final framing and light; neutral background; natural gestures; script in short spoken sentences; use the brand glossary for pronunciations.

### Synthesia

- **Facts**: Express-2 (September 2025) full-body gesturing avatars at 1080p 30fps with no length limit (Synthesia blog [P]); **Express-3** and Synthesia Assistant, July 15, 2026, script-aligned emotion, up to 2x faster generation (vendor claim), plus Style Avatars (stylized brand characters) via Avatar Builder (Synthesia [P]). Interactive "Sessions" avatars and API listed September 2026 (Synthesia updates [P]).
- **Best at**: enterprise training, compliance, multilingual internal comms; governance features.
- **Known weakness**: stock-avatar policy historically blocked brand promotion; November 2025 change allows it for the new customizable avatars (Synthesia blog [P]).

### ElevenLabs

- **Facts**
  - Eleven v3: alpha 2025, generally available February 2, 2026 (ElevenLabs blog [P]); introduced inline audio tags.
  - **Eleven v4 and v4 Turbo**, September 28, 2026: 90+ languages (up from 70), instant clone from 10 seconds of audio, stackable expression tags read in sequence, 10,000-character limit per request; v4 Turbo median latency about 100 ms (ElevenLabs changelog [P], TechCrunch [A]). v4 and v4 Turbo also on the **HF hub** [P].
  - Firefly carries ElevenLabs Multilingual v2 (Adobe [P]).
- **Best at**: VO, character voices, dubbing, sound effects, voice design from a text description.
- **Prompting technique**: write for the ear (contractions, short clauses); place tags like `[whispers]`, `[laughs]`, `[excited]` before the line they color; in v4 stack tags in order; spell brand names phonetically in a pronunciation dictionary.

### Voice cloning consent (rules for the agent)

- Clone only Shannon's voice or a person who signed a written release naming: scope (channels, clients), term, territory, compensation, revocation, and AI disclosure.
- Platforms now verify: HeyGen requires a consent recording (above [P]); Higgsfield's Soul ID instructions say upload only yourself or someone who gave permission (Higgsfield help [P]).
- Never clone a celebrity, competitor, or "sound-alike". State laws such as Tennessee's ELVIS Act (2024) create liability for tools and uses that reproduce an identifiable voice without consent (LexBlog summary [A]).

## 3D: image-to-3D, splats, real-time and DCC

### Image-to-3D generators

| Tool | Current version (source) | Strength | Weakness |
|---|---|---|---|
| Meshy | Meshy 7.1 is the API default; Meshy 6 full release Jan 18, 2026; Smart Topology model `meshy-t2` (Meshy API docs [P], Meshy guide [R]) | Fast, textured PBR, rigging and 600+ animations, many export formats, official MCP server | Geometry accuracy lagged Tripo in one test |
| Tripo | Tripo 3.1; **Tripo P2.0**, Sept 21, 2026, native quad mesh up to 25k quads (Tripo press release [P]) | Clean topology, auto-rig, speed | Stylized bias on hard-surface noted by one reviewer |
| Rodin (Hyper3D) | Gen-2.5, May 26, 2026, 10B params, 10M+ polygons, Smart Low-Poly (partner summary of Hyper3D blog [A]) | Highest raw detail, ChatAvatar faces | Dense meshes need retopo; slower |
| Hunyuan3D (Tencent) | Open: 2.1 (June 2025, community license excludes EU, UK, South Korea); hosted v3.1 Pro (GitHub [P], TripoSR comparison [R]) | Multi-view input, PBR paint stage | License limits; heavy VRAM |
| TRELLIS.2 (Microsoft) | Dec 2025, 4B params, MIT, up to 1536³, PBR incl. opacity (comparison citing official repo [R]) | Open, transparent materials, complex topology | 24 GB Linux GPU; single image only |
| Higgsfield `generate_3d` | Hub exposes Image to 3D, Multi-Image to 3D (1 to 4 views), 3D Rigging (Meshy-backed), SAM 3 3D Objects [P] | Inside Shannon's connector, GLB out | Same topology caveats |

- **Independent test** (Meshy-authored, so [R]): Meshy 6 vs Tripo v3.1 vs Rodin Gen-2.5, April to May 2026: Tripo best white-mesh geometry and quad topology; Meshy fastest text-to-3D (88 s median) and strong textures; Tripo fastest image-to-3D (99 s); per-call cost $0.18 to $0.25 (HackerNoon [R]).
- **Technique**: feed a clean, evenly lit, orthographic-ish front view on a plain background; use multi-view (front, side, back) for mascots; request A-pose for anything that will be rigged; set a polycount target for web (GLB under a few MB) and decimate after.

### Gaussian splatting

- What it is: a captured scene stored as millions of colored, semi-transparent ellipsoids; photoreal, real-time, but not a mesh.
- **Standards**: Khronos `KHR_gaussian_splatting` glTF extension, release candidate February 2026 (The Future 3D [A]); described as ratified in 2026 by a September 2026 explainer (ARGO [A]). Treat glTF splat import as still arriving in tools.
- **Blender 5.3** (alpha, release expected November 10, 2026) adds native splat import from PLY, SPZ and USD, rendering in Workbench, EEVEE and Cycles; no export yet; color and transform caveats (Digital Production, Creative Bloq [A]).
- **Capture**: Polycam and Luma on phones, Postshot locally, DJI Terra for aerial (The Future 3D [A]). **Edit/publish**: PlayCanvas SuperSplat (free, web) exports PLY, compressed PLY, SOG, SPZ and a self-contained HTML viewer, and renders camera paths to video up to 8K including 9:16 (PlayCanvas docs [P], ARGO [A]).
- **Spline** imports splat `.ply` up to 480 MB, but splats do not receive lights or shadows, physics, fog or material transparency, and mobile support is partial (Spline docs [P]).
- **Agency uses**: venue and store walkthroughs, product turntables from phone capture, 3D hero backgrounds, and vertical "flythrough" social videos rendered from SuperSplat.

### Spline, Blender and the web

- Spline: browser 3D design with states, events and web embed; good for interactive hero objects and Rive-like 3D micro-interactions. Keep scenes light for LCP (see file 09).
- Blender: free DCC for cleanup, retopo, UV, lighting and rendering of AI meshes; 5.3 adds splats (above).
- Higgsfield's **Scene Builder 3D** tools in the connector can assemble scenes and export GLB and `.blend` [P].

## Upscalers, relighting and motion control

- **Topaz Labs**: "Next-Gen" release April 28, 2026: Wonder 3, Denoise Max, Super Focus 3, High Fidelity 3 for images; Starlight Precise 2.5 and Astra 2 for video (Topaz press release [P]). Hyperion 2 SDR-to-HDR and a Premiere panel, May 7, 2026 (Topaz [P]). Starlight Precise 2.5 is described as specialized for realistic faces, skin, texture and text in AI video (Topaz community release notes [P]). Topaz Astra, Bloom and Hyperion 2.5 are reachable via the HF hub and Firefly [P].
- **Practice**: for AI video use temporally stable models (Starlight/Astra) over frame-by-frame generative upscalers, which can flicker (MindStudio explainer [R]). Upscale last, after the edit is locked, and add light grain to hide generative smoothness.
- **Magnific** (the company formerly Freepik, per BFL press release [P]): generative "creative" upscaling for stills; strong on texture invention, risky on faces and logos.
- **Relighting**: Higgsfield `relight_image` [P], Runway Aleph relighting of footage (Runway/Adobe [P]), Firefly Image Model 5 prompt edits, and Blender 5.3 relit splats. Practice: relight to match a plate before compositing products; check shadow direction against the key light in the plate.
- **Motion control**: Kling 3.0 Motion Control and Higgsfield Genjutsu transfer motion from a reference video onto characters in images [P]; Runway Act-Two drives a character from a phone performance (AIUnpacking [R]); Higgsfield Cinema Studio exposes named camera moves and speed ramps [P]. Practice: shoot the reference performance at the target framing and frame rate.

## Prompt craft for art directors

### The shot-list grammar

Write every prompt in the same order a DP reads a shot list. Models weight early tokens more, so lead with what matters.

1. **Shot size and angle**: "Medium close-up, low angle."
2. **Subject**: who or what, with fixed identifiers. "A 40-year-old woman, short silver bob, rust linen jacket (brand character 'Mara')."
3. **Action**: one clear verb per shot. "Lifts the mug and smiles off-camera."
4. **Setting**: place, time, weather. "Sunlit café counter, early morning, steam in the air."
5. **Lens and focal length**: "35mm, shallow depth of field, f/2." Wide (14 to 24mm) for space and energy, 35 to 50mm for natural perspective, 85 to 135mm for compression and flattering portraits.
6. **Camera move**: "Slow push-in", "lateral truck left", "orbit 90 degrees", "handheld follow". One move per shot.
7. **Lighting**: key direction and quality, then fill and accents. "Soft window key from camera left, warm practical lamps in background, rim light on hair."
8. **Film stock or grade**: "Kodak Portra 400 look, soft halation", "clean commercial grade, neutral whites", "teal and orange". Name the feel, not a LUT file.
9. **Composition**: "Rule of thirds, subject on left third, negative space right for headline", "center-framed symmetrical".
10. **Aspect ratio and duration**: "9:16, 6 seconds" or the model's parameter. Compose for the safe zone (file 09).
11. **Era and style references**: "1970s Italian food advertising", "Wes Anderson-adjacent symmetry" (style families, not living artists' names; see legal section).
12. **Audio** (video models with sound): dialogue in quotes with speaker, then ambience, then SFX, then music mood.
13. **Negative or constraints**: "No text in frame. Do not change the logo. Keep the product label legible."

**Template**

```
[Shot size, angle]. [Subject + identifiers] [action] in [setting, time].
Shot on [focal length], [aperture/DoF]. Camera: [move, speed].
Lighting: [key], [fill], [practicals/rim]. Look: [stock/grade].
Composition: [placement, negative space]. Format: [ratio], [duration].
Audio: [dialogue "..."], [ambience], [SFX], [music mood].
Constraints: [what must not change].
```

### Model-specific adjustments

- **Midjourney**: shorter, evocative; lean on `--sref`, moodboards, `--raw`, `--stylize`.
- **GPT Image / Nano Banana / Seedream**: full sentences and edit instructions; describe what stays fixed.
- **Ideogram 4/4.5**: JSON with bbox and hex palettes.
- **FLUX.2 / FLUX 3**: structured prose or JSON, references with assigned roles.
- **Veo / Omni / Kling / Seedance**: full shot grammar plus audio; one move and one action per clip; use first/last frames for endings that land on the product.
- **Higgsfield Cinema Studio**: put lens, camera, genre, era and tempo in the panel, keep the prompt for story and action.

### Consistency techniques

| Technique | What it locks | Where |
|---|---|---|
| Character sheet (turnaround: front, 3/4, side, back, expressions) | Identity, wardrobe, proportions | Any image model; Higgsfield workflow on explicit request [P] |
| Reference images with roles | Product, face, location, light | Nano Banana (up to 14 [P]), FLUX.2 (10 [P]), FLUX 3 Image (10 [A]), Seedance 2.5 (50 [A]), Cinema Studio 4.0 (50 [P]) |
| Saved elements / casts | Reusable character, prop, location | Higgsfield Elements and Soul Cast, Kling Elements, HeyGen looks [P] |
| Trained identity | One face across styles | Higgsfield Soul ID (20 to 80 photos [P]) |
| Custom model / LoRA | House style or product family | Firefly Custom Models [P], FLUX [dev] fine-tunes (license permitting) |
| Style reference codes | Look and texture | Midjourney `--sref`, Recraft styles, Soul Moodboards [P] |
| Seeds | Repeatability of a single prompt | Useful for A/B tweaks; weaker than references on modern models |
| Palette lock | Brand colors | Ideogram hex palettes [P], Soul HEX [P], FLUX hex control [P] |
| First/last frame | Shot endings, match cuts | Veo 3.1 Frames to Video [P], Luma keyframes, MiniMax H3 FL2VA [P] |

Practice rules:
- Generate the character sheet first, approve it, then never generate the character without it.
- Keep a **bible** per client: approved refs, seeds, sref codes, palette hexes, lens and grade defaults, forbidden elements.
- Change one variable per iteration. Log prompt, model, version and settings with every approved asset (also your copyright evidence).

### Avatar and mascot design workflow

1. **Brief**: personality in three adjectives, audience, channels, what the mascot does (talks? demos product? reacts?). Decide realistic human (avatar) vs stylized character (mascot).
2. **Shape language**: circles (friendly), squares (stable), triangles (energetic). Silhouette must read at 48px and in one color.
3. **Exploration**: 30 to 60 thumbnails across Midjourney V8.2, Nano Banana 2 and Recraft (for flat vector mascots). Pick 3.
4. **Human redraw**: an illustrator refines the chosen direction in vector. This step matters for ownership (see copyright section) and for clean geometry.
5. **Character sheet**: turnaround, expression set (8 to 12), hand poses, color specs in brand tokens, do/don't sheet.
6. **Motion**: 2D rig in Rive or After Effects for UI and social stickers; or 3D via Meshy/Tripo multi-view to GLB, retopo in Blender, rig (Tripo/Meshy auto-rig or Higgsfield 3D Rigging [P]).
7. **Voice**: ElevenLabs voice design from a written description (connector `creative_design_voice` [P]); save, document tags and pronunciation.
8. **Talking mascot**: HeyGen photo/prompt avatar or Synthesia Style Avatars for stylized presenters [P]; for a realistic spokesperson use Avatar V with signed consent.
9. **Governance**: a usage guide (where it appears, what it never says), disclosure language, and an asset registry with provenance.

## Ethics and legal layer

Not legal advice. Flag high-risk work for counsel.

### Copyright status of AI output (United States)

- **Human authorship is required.** The Copyright Office's Part 2 report (January 29, 2025) concludes: copyright protects human expression even in works that include AI material; purely AI-generated material, or material without sufficient human control over expressive elements, is not protected; analysis is case by case (Copyright Office Part 2 [P]).
- **Prompts alone are not enough.** The report treats prompts as instructions conveying unprotectable ideas given current tools (Part 2, as summarized by Mayer Brown [A]).
- **What can be protected**: human expressive inputs perceptible in the output (your sketch, your photo), creative selection, coordination or arrangement, and creative modifications of outputs (Part 2 [P]).
- **Registration**: disclose more-than-de-minimis AI material and describe the human contribution (2023 Guidance restated in Part 2 [P]).
- **Courts**: *Thaler v. Perlmutter* (D.C. Cir., March 18, 2025) held the Copyright Act requires human authorship; the Supreme Court denied review March 2, 2026 (D.C. Circuit opinion [P], Mayer Brown [A]). *Allen v. Perlmutter* (600+ prompt refinement) is pending in D. Colo. (Mayer Brown [A]).
- **Part 3** (training) exists as a May 9, 2025 pre-publication report (Copyright Office [P]).
- **Agency implications**
  - Logos, mascots and key brand marks: human-drawn final, AI only for exploration. Keep the sketch trail.
  - Contracts: do not warrant exclusive copyright in raw AI output; warrant the human-authored parts and the license terms of the tools used.
  - Keep a production log (prompts, references, edits, versions) per asset.
  - Avoid naming living artists in style prompts; describe the visual qualities instead.

### Likeness and voice rights

- **State laws**: eight states (Tennessee, California, Illinois, New York, Utah, Arkansas, Montana, Washington) have AI digital-replica statutes (LexBlog [A]). Tennessee's ELVIS Act targets unauthorized voice and likeness tools and uses (LexBlog [A]).
- **New York synthetic performer law** (S.8420-A, signed December 2025, effective June 9, 2026): ads disseminated in New York that use an AI "synthetic performer" (a digital human not recognizable as a real person) must conspicuously disclose it (BBB National Programs [A], LexBlog [A]). Applies regardless of where the ad was made. This hits AI UGC-style ads directly.
- **Federal NO FAKES Act of 2026**: advanced unanimously from Senate Judiciary June 2026; floor passage blocked by an objection on September 30, 2026; would create a federal voice and likeness right with notice-and-takedown and statutory damages (Senate text on govinfo [P], Deadline [A], LexBlog [A]).
- **FTC and ad law**: AI does not change truth-in-advertising rules; a synthetic presenter cannot imply real customer experience or fake testimonials (BBB National Programs [A]).
- **Agent rules**: no real person (client staff included) without signed release covering AI; no celebrity or public-figure lookalikes; synthetic "customers" are disclosed and never framed as real reviews.

### Platform disclosure rules (organic and paid)

- **YouTube**: creators must disclose realistic content that makes a real person appear to say or do something they did not, alters footage of a real event or place, or generates a realistic scene that did not occur; set via "AI use" under Attributes in Studio; YouTube may auto-label content with C2PA metadata, made with its own tools, or detected by its systems, and C2PA-based labels cannot be removed by the creator; repeat non-disclosure risks removal or YPP suspension (YouTube Help [P]). Not required for clearly unrealistic or animated content, color and lighting filters, or production help like scripts (YouTube blog, March 18, 2024 [P]).
- **Meta (Facebook, Instagram, Threads)**: "AI info" labels applied when industry-standard signals are detected or users self-disclose (Meta newsroom 2024 [P]); for ads, AI info appears in "About this ad", and AI-generated photorealistic humans from Meta's tools get a label next to the ad label; third-party AI tools detected via industry signals (Meta newsroom February 2025, Business Help [P]). Political and social issue ads have separate disclosure requirements (Meta [P]).
- **TikTok**: creators must label AI-generated content with realistic images, audio or video, using the AI-generated toggle or clear caption/sticker; TikTok auto-labels some content via Content Credentials (Creators Agency summary of TikTok policy [A]). Treat as required for any AI avatar or synthetic presenter ad.
- **EU AI Act Article 50**: applies from August 2, 2026. Deployers must disclose deepfakes (realistic image, audio or video resembling real persons, places, objects or events); artistic and fictional works get a lighter "do not hamper enjoyment" disclosure; providers must machine-mark outputs, with a grace period to December 2026 for systems already on the market; a voluntary Code of Practice (June 2026) and optional EU "AI" icons support compliance; video labels at start, after interruptions and at intervals (European Commission pages and Orrick summary [P]/[A]).
- **Default for Bright Matter**: if a reasonable viewer could think it is real, label it on every platform, keep provenance metadata, and add plain-language context ("AI-generated scene", "AI voice of our founder, used with permission").

### C2PA Content Credentials

- An open standard that cryptographically binds provenance (who made it, with what tools, what edits) to media as a signed "manifest"; specification versions 2.3 (January 5, 2026) and 2.4 (April 1, 2026) are current (C2PA spec PDFs [P]).
- C2PA published guidance on a dedicated `c2pa.ai-disclosure` assertion for model provenance and degree of human oversight, and reports 500+ members (C2PA site, updated August 2026 [P]).
- Adoption signals: OpenAI image outputs carry C2PA (OpenAI [P]); Nano Banana 2 outputs carry SynthID and C2PA (Google [P]); Pixel 10 camera signs every photo at C2PA Assurance Level 2 (Google, September 2025 [P]); YouTube, Meta and TikTok read C2PA signals for labels (platform pages above [P]/[A]).
- **Agent rules**: do not strip metadata to dodge labels; keep originals with credentials in the DAM; when compositing, re-export from tools that preserve or append credentials (Adobe apps) so the chain survives.

## Default production pipelines (Bright Matter)

- **Social ad set (product)**: brief → Firefly Boards or Higgsfield Canvas moodboard → hero still (Nano Banana 2 / FLUX / GPT Image 2.5) → type layer in Ideogram or Figma → animate (Veo 3.1 / Kling 3.0 / Seedance via Higgsfield) → edit in Clipkit or Premiere → Topaz upscale → captions → disclosure flag → C2PA-preserving export.
- **Founder video**: script → ElevenLabs or own voice → HeyGen Avatar V (consent on file) → B-roll from Seedance/Veo → captions and safe zones (file 09) → YouTube/Meta/TikTok AI labels.
- **Mascot program**: workflow above → Recraft vector → human redraw → Rive/After Effects motion → 3D via Meshy/Tripo → usage guide.
- **3D venue or product page**: phone capture → Polycam/Postshot splat → SuperSplat clean → web viewer or 9:16 flythrough video → Spline for interactive objects.

## Sources

Primary vendor and official [P]
- Midjourney Version docs: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- Midjourney V7 default post: https://updates.midjourney.com/v7-is-now-the-default-model/
- Midjourney V8 Alpha: https://updates.midjourney.com/v8-alpha/
- Midjourney Video V1: https://updates.midjourney.com/introducing-our-v1-video-model/ and https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video
- OpenAI gpt-image-1: https://openai.com/index/image-generation-api/ and https://community.openai.com/t/new-gpt-image-model-in-the-api/1239462
- OpenAI gpt-image-2: https://community.openai.com/t/introducing-gpt-image-2-available-today-in-the-api-and-codex/1379479
- OpenAI ChatGPT Images 2.5: https://openai.com/index/introducing-chatgpt-images-2-5/
- OpenAI image guide: https://developers.openai.com/api/docs/guides/image-generation
- OpenAI Sora 2 page (shutdown note): https://openai.com/index/sora-2/
- Google Nano Banana Pro: https://blog.google/innovation-and-ai/products/nano-banana-pro/
- Google Nano Banana Pro prompt tips: https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
- Google Nano Banana 2: https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/
- Google Nano Banana 2 Lite and Omni Flash API: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/
- Google Gemini Omni: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/
- DeepMind Gemini Omni Flash model card: https://deepmind.google/models/model-cards/gemini-omni-flash/
- Google Veo 3.1 and Flow: https://blog.google/innovation-and-ai/products/veo-updates-flow/
- Google Veo 3.1 Ingredients update: https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/
- BFL FLUX.2: https://bfl.ai/blog/flux-2 and https://bfl.ai/models/flux-2
- BFL FLUX 3: https://bfl.ai/blog/flux-3
- BFL FLUX.1 Kontext release: https://www.businesswire.com/news/home/20250529605562/en/
- Ideogram 4.0 press release and technical blog: https://ideogram.ai/news/ideogram-4.0/ and https://ideogram.ai/blog/ideogram-4.0/
- Ideogram 4 Hugging Face card: https://huggingface.co/ideogram-ai/ideogram-4-nf4
- Recraft V4 docs: https://recraft.mintlify.app/recraft-models/recraft-V4
- Adobe Firefly Boards worldwide: https://blog.adobe.com/en/publish/2025/09/24/firefly-boards-launches-globally-now-with-runway-aleph-moonvalley-marey-models-new-powerful-ideation-features-flexible-offers
- Adobe MAX 2025 Firefly: https://news.adobe.com/news/2025/10/adobe-max-2025-firefly
- Adobe Firefly March 2026: https://blog.adobe.com/en/publish/2026/03/19/adobe-firefly-expands-video-image-creation-with-new-ai-capabilities-custom-models
- Adobe Firefly AI Assistant April 2026: https://news.adobe.com/en/gb/news/2026/04/adobe-new-creative-agent
- Adobe Firefly September 2026 updates: https://community.adobe.com/announcements-402/what-s-new-in-adobe-firefly-september-2026-1642552
- Adobe Runway partner page: https://www.adobe.com/products/firefly/partner-models/runway.html
- ByteDance Seedream 4.0, 5.0 Lite, 5.0 Pro: https://seed.bytedance.com/en/blog/seedream-4-0-officially-released-beyond-drawing-into-imagination ; https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite ; https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro
- ByteDance Seedance 2.0 and 2.5: https://seed.bytedance.com/en/blog/seedance-2-0-official-launch ; https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- Runway Gen-4.5: https://runway.com/research/introducing-runway-gen-4.5
- Runway real-time research: https://runway.com/news/research/towards-instant-video-generation
- Kuaishou Kling 3.0: https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be
- Luma Ray3, Ray3.14, Ray3.2: https://lumalabs.ai/news/ray3 ; https://lumalabs.ai/news/ray3_14 ; https://lumalabs.ai/news/introducing-ray-3-2
- MiniMax H3 and release notes: https://www.minimax.io/news/minimax-h3-open-source ; https://platform.minimax.io/docs/release-notes/models
- Higgsfield help center (Soul ID, Soul, Cinema Studio, tools): https://higgsfield.ai/creator-hub/help-center/
- Higgsfield connector `models_explore` live listing, queried 2026-10-03
- HeyGen Avatar V: https://www.heygen.com/blog/announcing-avatar-v ; https://developers.heygen.com/avatar-v ; https://community.heygen.com/public/resources/avatar-v-live-webinar-recap-top-questions-answered-2026-04-16
- Synthesia Express-2, Express-3, updates: https://www.synthesia.io/post/express-2-is-synthesias-next-chapter-for-full-body-expressive-ai-avatars ; https://www.synthesia.io/post/synthesia-launches-new-ai-assistant-for-faster-video-creation-and-express-3-avatar-model ; https://www.synthesia.io/updates
- ElevenLabs blog and changelog: https://elevenlabs.io/blog ; https://elevenlabs.io/docs/changelog
- Meshy API docs: https://docs.meshy.ai/en/api/image-to-3d
- Tripo P2.0 release: https://finance.yahoo.com/technology/ai/articles/tripo-ai-releases-latest-model-032200541.html
- Hunyuan3D 2.1 repository: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
- PlayCanvas SuperSplat import/export: https://developer.playcanvas.com/user-manual/supersplat/editor/import-export/
- Spline Gaussian splatting docs: https://docs.spline.design/designing-in-3-d/scenes/3d-gaussian-splatting
- Topaz Labs releases: https://www.prnewswire.com/news-releases/topaz-labs-announces-its-largest-single-release-of-ai-models-in-company-history-with-next-gen-launch-302756375.html ; https://community.topazlabs.com/t/topaz-video-1-6-0/102732
- US Copyright Office AI hub and Part 2: https://www.copyright.gov/ai/ ; https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf
- Thaler v. Perlmutter, D.C. Cir. 2025: https://caselaw.findlaw.com/court/us-dc-circuit/117062322.html
- NO FAKES Act of 2026 text: https://www.govinfo.gov/content/pkg/BILLS-119s4591rs/xhtml/BILLS-119s4591rs.html
- YouTube AI disclosure help and blog: https://support.google.com/youtube/answer/14328491 ; https://blog.youtube/news-and-events/disclosing-ai-generated-content/
- Meta AI labeling: https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/ ; https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/ ; https://www.facebook.com/business/help/1010479435004531
- EU AI Act Article 50, Code of Practice, icons: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50 ; https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content ; https://digital-strategy.ec.europa.eu/en/factpages/quick-facts-transparency-rules-ai-systems ; https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content
- C2PA specification 2.3 and 2.4: https://spec.c2pa.org/specifications/specifications/2.3/specs/ContentCredentials.html ; https://spec.c2pa.org/specifications/specifications/2.4/specs/_attachments/C2PA_Specification.pdf
- C2PA implementation guide news: https://c2pa.org/a-new-implementation-guide-for-content-credentials/
- Google Pixel 10 Content Credentials: https://blog.google/security/pixel-android-trusted-images-c2pa-content-credentials/

Independent tests and single reviewers [I]/[R]
- Artificial Analysis video leaderboard figures as reported by Runway (leaderboard independent, report vendor): see Runway Gen-4.5 link
- ContraLabs typography evaluation (published by Ideogram): https://github.com/ideogram-oss/ideogram4
- Meshy 6 vs Tripo 3.1 vs Rodin Gen-2.5 (Meshy-authored): https://hackernoon.com/how-i-stress-tested-3-ai-3d-generators-on-the-same-inputs-what-the-numbers-actually-show
- PixMind Midjourney V8.1 vs V7: https://www.pixmind.io/posts/midjourney-v8-1-vs-v7
- AIUnpacking Runway review: https://aiunpacking.com/review/runway/
- TRELLIS.2 vs Hunyuan3D comparison: https://triposr.org/blog/hunyuan3d-vs-trellis
- MindStudio on Topaz Astra vs Magnific: https://www.mindstudio.ai/blog/topaz-astra-video-upscaler-scene-detection

Aggregators and trade press [A]
- The Decoder, FLUX 3 Image: https://the-decoder.com/black-forest-labs-launches-flux-3-image-with-multi-step-editing-that-leaves-the-rest-of-your-picture-alone/
- Creative AI News, Ideogram 4.5: https://www.creativeainews.com/articles/ideogram-4-5-precise-edit-multi-turn-2026/
- Runware docs (Aleph 2.0, Ideogram 4 guide, Recraft V4 Styles): https://runware.ai/docs/models/runway-aleph-2-0.md
- Kolbo, Recraft V4.1: https://kolbo.ai/blog/recraft-v41-launch
- TechCrunch, ElevenLabs v4: https://techcrunch.com/2026/09/28/elevenlabs-new-v4-speech-model-supports-more-expression-control-and-90-languages/
- Digital Applied, Seedance 2.5: https://www.digitalapplied.com/blog/seedance-2-5-official-launch-one-take-video
- Global Times, Seedance 2.0 reception: https://www.globaltimes.cn/page/202602/1355356.shtml
- TechTimes and Modellix, Kling 4.0: https://www.techtimes.com/articles/328285/20260930/kling-40-promises-30-second-4k-video-broadcast-spec-coming-october-not-today.htm ; https://www.modellix.ai/blog/kling-4-0/
- Pasquale Pillitteri and Convly, Sora API shutdown: https://pasqualepillitteri.it/en/news/18764/openai-sora2-api-dismessa-en ; https://convly.ai/sora-2-api-shutdown-september-2026/
- Best AI Web, 3D tools (Rodin Gen-2.5 date): https://www.bestaiweb.ai/how-to-use-meshy-tripo-ai-and-rodin-gen-2-for-game-assets-character-models-and-product-visualization/
- The Future 3D, state of Gaussian splatting: https://www.thefuture3d.com/blog/state-of-gaussian-splatting-2026/
- ARGO, splat deliverables: https://ar-go.co/blog/gaussian-splatting-deliverables/
- Digital Production and Creative Bloq, Blender 5.3 splats: https://digitalproduction.com/2026/09/22/blender-5-3-brings-gaussian-splats-home/ ; https://www.creativebloq.com/3d/blender-5-3-finally-gets-game-changing-native-gaussian-splat-support
- Mayer Brown on Thaler cert denial: https://www.mayerbrown.com/en/insights/publications/2026/03/supreme-court-denies-review-in-ai-authorship-case
- BBB National Programs, synthetic performers: https://bbbprograms.org/media/insights/blog/synthetic-performers
- LexBlog, NO FAKES and state laws: https://www.lexblog.com/2026/08/20/a-federal-shift-in-ai-and-the-right-of-publicity-no-fakes-act-advances-in-congress/
- Deadline, NO FAKES blocked: https://deadline.com/2026/09/ted-cruz-no-fakes-act-senate-1237143753/
- Creators Agency, YouTube and TikTok disclosure: https://creatorsagency.co/blog/youtube-tiktok-ai-disclosure-rules-2026
- Orrick, EU AI Act Article 50: https://www.orrick.com/en/insights/2026/08/eu-ai-act-transparency-obligations-for-ai-generated-content-article-50
