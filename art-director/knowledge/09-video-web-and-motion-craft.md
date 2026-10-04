# 09 · Video, Web and Motion Craft

Knowledge file for the Bright Matter art-direction agent. Part one is filmmaking and editing vocabulary plus short-form technique. Part two is web design craft: layout, type, motion, systems, accessibility, performance, conversion, and trends. Written for 2026-10-03.

## How to read this file

- **Source tiers** in brackets: **[P]** primary (standards body, platform or vendor docs), **[I]** independent research, **[R]** single reviewer or practitioner, **[A]** aggregator or trade press. **[Craft]** marks long-established film and design vocabulary documented across textbooks and film history; no single figure rides on it.
- Numbers (thresholds, specs, durations) always carry a source. Where sources disagree, both are shown.
- **Bright Matter alignment**: the motion terms in Part two match the twelve labeled techniques in `/home/user/bright-matter-brand/reference/motion-vocabulary.html` (the "Northline Motion Lab" page). When briefing a developer or a model, use those exact names and the starter values listed there.

# Part one: Video and filmmaking

## Shot sizes [Craft]

| Name | Abbrev | Frames | Use |
|---|---|---|---|
| Extreme wide / establishing | EWS | Whole location, people tiny | Place, scale, opening a sequence |
| Wide / long shot | WS / LS | Full body plus environment | Blocking, relationship to space |
| Full shot | FS | Head to toe | Wardrobe, choreography, product in use |
| Medium wide / cowboy | MWS | Mid-thigh up | Two-person walk and talks |
| Medium shot | MS | Waist up | Default dialogue, presenters |
| Medium close-up | MCU | Chest up | Talking head, UGC, avatars |
| Close-up | CU | Face | Emotion, reaction, testimony |
| Extreme close-up | ECU | Eyes, lips, a detail | Tension, texture, product macro |
| Insert / cutaway | INS | An object or action detail | Product beauty, hands, UI on screen |
| Two-shot / OTS | 2S / OTS | Two subjects, or over a shoulder | Conversation, interview coverage |
| POV | POV | What a character sees | Immersion, "POV:" social formats |

- Coverage rule: for any scene, shoot or generate at least a wide, a medium and a close-up plus inserts, so the edit has choices.
- In 9:16, sizes read one step tighter than in 16:9. An MS in vertical feels like an MCU in landscape.

## Camera angles [Craft]

- **Eye level**: neutral, honest; the default for testimonials and founders.
- **Low angle**: power, heroism, scale; product hero shots looking up at a bottle.
- **High angle**: vulnerability, overview; flat-lays are the extreme version (top-down or bird's eye).
- **Dutch / canted**: unease, energy; use sparingly, mostly in music and sports cuts.
- **Overhead / top shot**: recipes, unboxing, desk setups; reads well on mobile.
- **Ground level**: sneakers, pets, kinetic energy.
- **Over-the-shoulder**: conversation grammar; implies a listener.

## Camera moves [Craft]

| Move | What happens | Feeling | Prompt phrase |
|---|---|---|---|
| Pan | Camera rotates left/right on a fixed point | Survey, reveal | "slow pan right revealing the storefront" |
| Tilt | Rotates up/down | Scale, reveal height | "tilt up from shoes to face" |
| Dolly in/out (push/pull) | Camera physically moves toward/away | Intimacy or isolation | "slow dolly-in to MCU" |
| Truck / track | Moves sideways parallel to subject | Travel with, parallax depth | "lateral truck left along the counter" |
| Pedestal | Moves straight up/down | Reveal without perspective change | "pedestal up over the shelf" |
| Crane / jib | Sweeping vertical and arcing moves | Grandeur, openings and endings | "crane up and back to wide" |
| Arc / orbit | Circles the subject | Product hero, spectacle | "180-degree orbit around the sneaker" |
| Handheld | Organic shake | Documentary truth, UGC | "handheld, slight breathing motion" |
| Steadicam / gimbal follow | Smooth follow | Flow, walk and talk | "gimbal follow behind subject" |
| Whip pan | Very fast pan with motion blur | Energy, transition between scenes | "whip pan transition" |
| Crash zoom / snap zoom | Fast optical zoom | Comedy, emphasis | "snap zoom to her face" |
| Dolly zoom (Vertigo effect) | Dolly one way while zooming the other; subject stays same size, background warps | Dread, realization | "dolly zoom on the face, background stretching" |
| Snorricam | Camera rigged to the actor's body facing them | Disorientation, intoxication, panic | "body-mounted snorricam, background swinging" |
| Drone / aerial | Flying moves | Scale, location | "drone rise over rooftop" |
| Rack focus | Focus shifts between planes | Redirect attention | "rack focus from cup to face" |
| Speed ramp | Playback speed changes inside a shot | Impact, rhythm | "ramp from real time to 20% slow motion on impact" |

- The dolly zoom was popularized by Hitchcock's *Vertigo* (1958) [Craft]. The snorricam is named for the Snorri Bros. who popularized the rig [Craft].
- AI video rule: **one move per generated shot**. Combined moves ("orbit while craning while zooming") are where models break.
- Higgsfield Cinema Studio exposes named moves and speed-ramp presets (Linear, Auto, Flash In, Flash Out, Slow-mo, Bullet Time, Impact, Ramp Up) (Higgsfield help center [P]).

## Lens language [Craft]

- **Ultra-wide (12 to 18mm full-frame equivalent)**: exaggerated space, distortion near edges, comedic or energetic close-ups, tiny rooms feel big.
- **Wide (24 to 28mm)**: environment plus subject; documentary, vlog, UGC selfie look (phone main cameras sit roughly here).
- **Normal (35 to 50mm)**: closest to natural perspective; honest, unforced.
- **Short tele (85mm)**: flattering portraits, soft background separation.
- **Telephoto (135mm and up)**: compression; backgrounds loom, crowds stack, distance feels voyeuristic.
- **Macro**: texture, product detail, food.
- **Anamorphic**: oval bokeh, horizontal flares, wide 2.39:1 feel; reads "cinema".
- **Depth of field**: shallow (f/1.4 to f/2.8) isolates; deep (f/8 and up) keeps context. Shallow DoF is the fastest way to make AI or phone footage feel premium, and the fastest way to look generic if overused.
- **Vintage lenses**: lower contrast, flare, softness; pairs with film-emulation grades.

## Lighting setups [Craft]

| Setup | Construction | Read |
|---|---|---|
| Three-point | Key (main), fill (softens shadows), back/rim (separates from background) | Clean, corporate, interviews |
| Rembrandt | Key high and to one side so a small triangle of light falls on the far cheek | Painterly, dramatic, character |
| Butterfly / Paramount | Key high and in front, centered; butterfly-shaped shadow under the nose | Beauty, glamour, cosmetics |
| Split | Key at 90 degrees; half the face in shadow | Duality, tension, mystery |
| Loop | Key slightly off-axis; small nose shadow loops toward the cheek | Natural, flattering default |
| Broad vs short | Light the side of the face toward (broad) or away from (short) the camera | Broad widens, short sculpts and slims |
| Motivated | Light appears to come from a believable source in the scene (window, lamp, screen) | Realism |
| Practicals | Visible lamps, neon, candles in frame that also light the scene | Depth, warmth, production value |
| High key | Bright, low contrast, few shadows | Optimism, health, retail, comedy |
| Low key | Dark, high contrast, deep shadows | Luxury, drama, thriller |
| Silhouette / backlight | Subject against bright source | Mystery, iconography |
| Hard vs soft | Small source (crisp shadows) vs large diffused source (gradual falloff) | Hard: fashion edge; soft: friendly, beauty |
| Color contrast | Warm key vs cool ambience (or reverse) | Separation, mood |

- Prompt practice: always name direction and quality ("soft window key from camera left, warm practical lamp behind, cool rim"). Unspecified light defaults to flat, center-lit "AI look".
- For product: a long soft source for glossy bottles (clean gradient reflections), hard light for texture (knit, food crust), and a kicker or rim to separate dark products from dark backgrounds.

## Color grading [Craft]

- **Correction vs grading**: correction normalizes (exposure, white balance, matching shots); grading creates the look. Correct first, grade second.
- **LUT (look-up table)**: a file mapping input colors to output colors. Technical LUTs convert log footage to Rec.709; creative LUTs apply a look. Apply creative LUTs at reduced strength on a node after correction.
- **Log and HDR**: log footage holds highlight and shadow detail for grading. Luma Ray3 outputs 16-bit HDR EXR (ACES2065-1) for this reason (Luma [P]); Topaz Hyperion converts SDR to HDR (Topaz [P]).
- **Teal and orange**: pushes shadows and backgrounds toward teal and skin toward orange, exploiting complementary contrast. Effective, heavily overused in blockbuster and travel content; use with restraint for brands.
- **Film emulation**: grain, halation (red glow around highlights), soft roll-off, gate weave, specific stock palettes (Portra warm skin, Ektachrome saturated, CineStill 800T tungsten with red halation). Strong in 2024 to 2026 social as a reaction to clean AI imagery [R, practitioner observation].
- **Bleach bypass**: desaturated, high contrast, silvery; grit and war-film energy.
- **Monochrome with spot color**: one brand color survives; strong for brand recall.
- **Color script**: a sequence of key frames showing how color evolves across a film or campaign (Pixar-style practice). For campaigns: map each beat (problem, turn, payoff) to a palette shift, then grade every asset to its beat.
- **Skin first**: protect skin tones on the vectorscope skin line before pushing any look.
- **Consistency across AI clips**: generate with a neutral, well-exposed look, then grade all clips together in Resolve or Premiere. Baking strong looks into prompts makes clips from different models impossible to match.

## Edit grammar [Craft]

| Cut | Definition | Use |
|---|---|---|
| Hard cut | Instant change | The default |
| J-cut | Audio of the next shot starts before its picture | Pulls viewer forward, smooth dialogue |
| L-cut | Audio of the current shot continues over the next picture | Lets a line land on a reaction, smooth exits |
| Match cut | Cut between shots matched by shape, motion, color or composition | Elegant transitions (circle to circle, swing to swing) |
| Graphic match | Match on visual form only | Brand storytelling, logo reveals |
| Smash cut | Abrupt cut to a jarringly different scene, often loud to quiet | Comedy, shock, punchline |
| Jump cut | Cut within the same shot so time skips | Vlog and UGC pace, energy, removing ums |
| Cross-cutting / parallel editing | Alternating between simultaneous actions | Tension, comparison, before/after |
| Montage | Series of short shots compressing time or ideas | Training, transformation, product range |
| Cutting on action | Cut mid-movement so the motion carries across | Invisible continuity, momentum |
| Cutaway / insert | Cut to a detail and back | Hide edits, show product |
| Dissolve / cross-fade | Gradual blend | Time passing, softness; dated if overused |
| Match on action across angles | Same action continues from a new angle | Dynamic coverage |
| Invisible editing (continuity) | 180-degree rule, eyeline match, screen direction, matching action | Story immersion, ads that feel like film |
| Expressive editing | Visible, rhythmic, stylized cuts | Music, fashion, social energy |

- **Kuleshov effect**: Soviet filmmaker Lev Kuleshov showed that the same neutral face reads as hunger, grief or desire depending on the shot cut next to it [Craft]. Application: meaning lives in juxtaposition. A neutral product shot after a frustrated face reads as "the fix".
- **Walter Murch's Rule of Six** (from *In the Blink of an Eye*): rank cut decisions by emotion (51%), story (23%), rhythm (10%), eye-trace (7%), two-dimensional plane of screen (5%), three-dimensional space of action (4%) [Craft, book]. Emotion beats continuity.
- **180-degree rule**: keep the camera on one side of the action line so screen direction stays consistent. AI multi-shot generations break this often; check before approving.
- **Eye-trace**: place the next shot's point of interest where the viewer's eye already is. Crucial in 9:16 where the eye sits center-upper.

## Pacing and rhythm [Craft]

- **Pace** is perceived speed (shot length, movement, information density). **Rhythm** is the pattern of change (long-short-short-long).
- Vary shot length. Uniform 1-second cuts flatten into noise; a long held shot after rapid cuts lands as emphasis.
- Cut to the music's phrasing, not every beat. Hit downbeats for big changes, leave fills for motion within shots.
- **Breath**: give reveals, faces and product hero shots 0.5 to 1 second longer than feels necessary on the timeline; viewers need time to register.
- **Rule of three** in sequences: three examples, the third is the turn.
- Short-form: front-load information density, then let the payoff breathe.

## Sound design [Craft]

- **Diegetic**: sound that exists in the story world (dialogue, footsteps, a café). **Non-diegetic**: score, narration, stingers.
- **Foley**: recreated everyday sounds (footsteps, cloth, cups) added in post; makes AI or stock footage feel physical.
- **Room tone / ambience**: the bed under everything; cut it out and the edit feels broken.
- **Sound bridge**: sound that carries across a cut (J and L cuts are the audio side of this).
- **Risers and swells**: rising tones that build tension into a reveal; **hits / impacts / stingers** mark cuts; **whooshes** sell motion and transitions; **reverse cymbals** pre-lap big moments.
- **Silence**: the strongest emphasis tool. A one-beat dropout before a product reveal outperforms more volume [Craft].
- **ASMR**: close-mic, high-detail, soft sounds (crinkle, pour, tap, unboxing). Strong for food, beauty, packaging, tactile products.
- **Voice**: VO clarity first; duck music under speech; keep a consistent loudness target per platform.
- **Sound-on cultures differ**: TikTok is sound-first; Meta feeds have historically defaulted to sound-off, so design captions for both (rule1 TikTok spec guide [A], platform guidance below).
- AI models with native audio (Veo 3.1, Kling 3.0, Seedance 2.x, Gemini Omni) still benefit from a final Foley and mix pass.

## Short-form craft (TikTok, Reels, Shorts)

### Platform facts that drive the edit

- **YouTube Shorts** can be up to 3 minutes for square or vertical uploads from October 15, 2024 (YouTube blog and Help [P]).
- **TikTok creative guidance** (as quoted from TikTok's own best-practices docs): hook within the first 6 seconds for engagement and watch time; introduce the core proposition within the first 3 seconds for recall; vertical 9:16 at 720p or better with sound; on-screen text at 5 to 10 words per second; keep text and logos in the safe zone, which shrinks as captions grow (Deepclick summary of TikTok docs [A]).
- TikTok ad specs: in-feed auction up to 10 minutes, minimum 540x960 for 9:16, 500 MB max; 1080x1920 recommended; 9 to 15 seconds is commonly cited as the performance sweet spot (rule1, Deepclick [A]).
- Hook metric windows differ: TikTok reports 2-second views, Meta 3-second views (rule1 [A]).
- **Instagram Reels**: feed may display a 9:16 Reel as a 4:5 center crop; profile grid moved to 4:5 (AdMakeAI [A]). Upload limits reported as up to 15 minutes, with recommendation favoring under 3 minutes (AdMakeAI [A]; verify in-app).
- Treat duration and safe-zone pixel numbers from aggregators as working guides; always preview in each app or the official safe-zone tools (TikTok Ads Manager templates, Meta Reels safe-zone checker, Google's universal video ad safe-zone guide, all referenced by Reap [A]).

### 9:16 safe zones (working numbers)

- Master at **1080 x 1920**.
- Conservative cross-platform margins: avoid the top ~250 px, bottom ~576 px, right ~164 px, left ~60 px, leaving roughly a center 856 x 1094 zone (AdMakeAI, reverse-engineered approximations [A]).
- TikTok-specific starting guides cited at top ~130 to 150 px and bottom ~350 px, more with Shop or CTA buttons (rule1, Conbersa [A]).
- Shorts has the deepest bottom UI; lift CTAs about 400 px above the bottom edge (AdMakeAI [A]).
- Practice: faces in the upper-middle third, captions in the lower-middle band above the UI tray, nothing load-bearing in the right rail.

### Hooks in the first 1 to 3 seconds

- **Visual pattern interrupt**: unexpected first frame (extreme close-up, motion already in progress, a prop that should not be there).
- **Result first**: show the after, then the how.
- **Direct address mid-sentence**: creator already talking when the video starts; no "Hi guys".
- **Curiosity gap text**: "What nobody tells you about…"; "I tried X for 30 days".
- **Contrarian claim**: "Stop buying…" (substantiate claims; ad law still applies).
- **Problem recognition**: "If your [pain], watch this."
- **Audio hook**: a sound that demands attention (crunch, pour, snap) from frame 1; avoid silent starts on TikTok (rule1 [A]).
- Rules: no logo sting first; brand appears inside the hook, not before it; first frame must also work as a still (it is the thumbnail in many surfaces).

### Retention devices

- **Pattern interrupts** every 2 to 4 seconds: angle change, zoom punch-in, B-roll insert, text pop, sound hit [R, practitioner convention].
- **Open loops**: tease the payoff early ("number 3 is the one that worked") and pay it off late.
- **Loops**: make the last frame flow into the first (same framing, sentence that completes into the opening line) so replays inflate watch time.
- **Progress cues**: numbered lists, step counters, a visual timer.
- **Text-on-screen**: short, high contrast, two lines max, timed to speech; keep consistent position per series.
- **Captions**: burned-in open captions; word-by-word highlight styles for talking heads; check that captions do not cover mouth, hands or product (Reap [A]).

### Native-feeling UGC grammar

- Phone-native framing (selfie MCU, 24 to 28mm look), natural window light, real rooms.
- Jump cuts to remove pauses; handheld; occasional mistakes left in.
- Direct-to-camera, first person, specific numbers and personal stakes.
- Formats: "Get ready with me", "Day in the life", unboxing, "3 things I wish I knew", reaction, duet/stitch, tutorial, before/after, "POV:" captions.
- **AI UGC caution**: synthetic creators must be disclosed on TikTok, Meta and YouTube when realistic, and New York requires conspicuous disclosure of synthetic performers in ads from June 9, 2026 (see file 08 [P]/[A]).

### Formats and techniques

- **Green screen**: creator in front of a screenshot, article or product page; fast explainer and commentary format; native green-screen effects exist in TikTok and CapCut.
- **POV formats**: on-screen "POV: you just…" with the camera as the viewer; a framing device for relatable scenarios.
- **Faceless**: hands-only, screen recordings, B-roll with VO, kinetic text; good for brands without a spokesperson, and a natural home for AI B-roll and AI voice (disclose when realistic).
- **Talking-head plus B-roll**: A-roll explanation with cutaways; HeyGen Video Agent automates a version of this with Avatar V plus Seedance shots (HeyGen [P]).
- **Carousel-to-video**: static slides animated with kinetic type.

## Trending edit styles 2024 to 2026

Trend notes are practitioner observation [R] unless sourced; check current examples with the trend-watch skill and vidIQ before pitching.

- **Speed ramps**: real time into slow motion on impact and back; now a one-click preset in Higgsfield Cinema Studio (Higgsfield [P]).
- **Mixed media / collage**: cut-out photo, paper texture, scribbles, stop-motion stickers layered on live action. Signals handmade in an AI-saturated feed.
- **Lo-fi camcorder and digicam**: DV and 8mm looks, timestamp overlays, 4:3 frames inside 9:16; Higgsfield Cinema Studio 4.0 offers DV Camcorder and 8mm camera profiles (Higgsfield [P]).
- **Deinfluencing**: creators telling audiences what not to buy; brands respond with honest comparisons, "who this is not for", and proof-heavy content.
- **Faceless channels**: AI voice, stock or AI B-roll, captions; saturated, so differentiation comes from a distinctive visual system and a real point of view.
- **Motion graphics and kinetic type**: bold animated typography, data callouts, UI-style overlays; HyperFrames (HeyGen) and Clipkit can author these programmatically (connector docs [P]).
- **Film emulation and grain** as a counter to clean AI imagery.
- **Long single takes** generated by AI (Seedance 2.5 30-second one-takes [P]) used as hooks or brand films.
- **Text-led "notes app" and screenshot formats**; **split-screen comparisons**; **ASMR product**.

# Part two: Web design craft

## Layout systems

- **Grids**: 12-column for desktop (divides into 2, 3, 4, 6), 8-column for tablet, 4-column for mobile; consistent gutters and outer margins. Use a **baseline grid** (4 or 8 px) for vertical rhythm [Craft].
- **8-point spacing system**: spacing values 4, 8, 12, 16, 24, 32, 48, 64, 96, 128; reduces arbitrary decisions and maps to tokens [Craft].
- **CSS Grid** for two-dimensional layout (bento, editorial), **Flexbox** for one-dimensional rows and stacks, **container queries** so components respond to their container, not the viewport.
- **Responsive approach**: mobile-first; fluid type and spacing with `clamp()` (the Bright Matter motion page uses `clamp(44px, 8vw, 96px)` for the hero headline [internal]); breakpoints by content, not devices. Keep a 16 px side gutter at phone width with no horizontal scroll.
- **Max content width**: 1,100 to 1,280 px for content areas; the motion page uses a 1,140 px wrap [internal].
- **Layout archetypes**: hero + proof + features + social proof + CTA (marketing), editorial long-read, bento dashboard, split screen, sticky storytelling (pinned media with scrolling text), card grids, asymmetric magazine.

## Typographic scale

- **Modular scales** multiply a base size by a ratio: 1.125 (major second, dense UI), 1.2 (minor third, product UI), 1.25 (major third, balanced marketing), 1.333 (perfect fourth, editorial), 1.5 (perfect fifth, expressive), 1.618 (golden, display-heavy) [Craft, math].
- Example at 16 px base, ratio 1.25: 16, 20, 25, 31, 39, 49, 61 px.
- **Fluid type**: interpolate between a mobile and desktop scale with `clamp(min, preferred vw, max)`.
- **Measure**: 45 to 75 characters per line, around 66 as a comfortable target for body text (Bringhurst, *The Elements of Typographic Style* [Craft, book]).
- **Leading**: body 1.4 to 1.6; display 0.95 to 1.15 with negative tracking (the motion page uses line-height .98 and letter-spacing -.035em for the hero [internal]).
- **Hierarchy tools** in order of strength: size, weight, color/contrast, case, spacing, position.
- **Pairing**: one display face plus one text face, or one superfamily; add a mono for labels and data (the motion page pairs Archivo with IBM Plex Mono [internal]).
- **Variable fonts**: one file, many weights and widths; enables weight animation in kinetic type.
- **Accessibility**: 4.5:1 contrast for body text; large text (18 pt or 14 pt bold, roughly 24 px or 18.5 px) can drop to 3:1 (WCAG 2.2 [P]).

## Scroll storytelling

- Structure a long page like a film: **hook** (hero), **inciting problem**, **escalation** (proof, features), **turn** (the product moment), **resolution** (CTA).
- Techniques: pinned chapters with progressing content, scroll-scrubbed product rotations or explosions, image sequences tied to scroll, section color shifts as chapter markers, a progress bar for long reads.
- Rules: every motion must reveal information or orient the user; never hijack scroll speed (no scroll-jacking); content must remain readable with motion off; keep the first screen fast (LCP).
- Reference behavior: Apple-style product pages use pinned media plus scroll-scrubbing; editorial sites (long-form journalism) use sticky graphics with stepping text.

## Motion vocabulary (aligned with the Bright Matter motion page)

The house reference `motion-vocabulary.html` labels twelve techniques with demo values and the exact phrases to put in a prompt. Use these names verbatim [internal]:

| # | Technique (house name) | What it is | House starter values [internal] |
|---|---|---|---|
| 1 | **Scroll-reveal fade-up** | Content fades in and rises as it enters the viewport | ~20 to 22 px rise, ~600 ms, ease-out, trigger once |
| 2 | **Stagger sequencing** | Siblings animate one after another | 80 to 100 ms apart |
| 3 | **Parallax depth** | Background layers scroll slower than foreground | 0.2x to 0.5x; demo at 0.35x ("or it feels like 2014") |
| 4 | **Scroll-scrubbing (scroll-linked)** | Animation progress tied to scroll position, reversible | Demo: scale 1.08 to 1.0 across the viewport |
| 5 | **Pinned / sticky section** (`position: sticky`) | One element holds while content scrolls past | Left headline pinned, steps scroll right |
| 6 | **Micro-interaction** (hover / press) | Small responses to input | Card lift 4 to 5 px plus deeper shadow, 250 ms ease-out; underline draws left to right |
| 7 | **Page-load sequence** (entrance) | Hero builds itself on arrival | Eyebrow, headline, copy, CTAs, 100 ms apart, rising 24 px |
| 8 | **Count-up number ticker** | Stats count from zero on first view | ~1.2 s, once |
| 9 | **Condensing nav** (scroll state) | Nav shrinks and gains blur and hairline after scrolling | After ~40 px of scroll |
| 10 | **Marquee** (auto-scroll) | Infinite strip of logos or names | Slow, seamless, pause on hover |
| 11 | **Easing and duration** (the feel) | Curves and timing | Ease-out for entrances; 200 to 300 ms micro; 500 to 700 ms reveals; nothing bouncy unless the brand is playful |
| 12 | **Reduced motion** (accessibility) | Disable non-essential motion for users who ask | Respect `prefers-reduced-motion`: static, no parallax, no reveals |

The page also demonstrates a **scroll progress bar** (a thin bar whose width maps to scroll depth) as an annotated extra [internal].

Additional vocabulary to use alongside the house twelve:

- **View transitions**: animated transitions between DOM states (single-page) or between pages (multi-page) using the View Transitions API. Same-document transitions became Baseline on October 14, 2025 (Chrome/Edge 111, Safari 18, Firefox 144); cross-document transitions are supported in Chrome/Edge 126 and Safari 18.2 but not Firefox, so treat them as progressive enhancement (Google Chrome modern-web-guidance [P], Chrome docs [P], MDN [P]). Cross-document requires same origin and `@view-transition { navigation: auto; }` on both pages (MDN [P]).
- **CSS scroll-driven animations** (`animation-timeline: scroll()` / `view()`): native scroll-scrubbing without JavaScript. MDN marks it "limited availability" (not Baseline) (MDN [P]); caniuse shows Safari 26.0 and later supported (caniuse [A]); Chromium has shipped it since version 115 and Firefox historically kept it behind a flag (css.properties [A]). Provide a fallback.
- **Shared element / morph**: an element visually travels from one state to another (thumbnail to hero); achievable with view transitions or FLIP techniques.
- **Text reveal / split text**: per-line, per-word or per-character animation; GSAP's SplitText was rewritten with screen-reader accessibility and masking (Webflow [P]).
- **Magnetic buttons, cursor followers, custom cursors**: playful premium touches; disable on touch and for reduced motion.
- **Skeleton and optimistic states**: loading placeholders that reduce perceived wait; part of INP and CLS hygiene.
- **Lottie**: JSON vector animations exported from After Effects (via Bodymovin); good for icons and illustrations; watch file size and frame count.
- **Rive**: interactive vector animation with state machines (hover, click, input-driven states); ideal for mascots, onboarding and interactive illustrations. Recraft V4 can export Lottie from generated vectors (Recraft docs [P]).
- **GSAP**: the industry JavaScript animation library (ScrollTrigger for pinning and scrubbing, SplitText, MorphSVG, Flip). **Free for everyone including commercial use and all former Club plugins since Webflow's April 30, 2025 announcement** (Webflow [P], GSAP license [P]).
- **Three.js / WebGL**: 3D in the browser for product configurators, hero objects, particle fields; Spline exports Three.js-compatible scenes; Gaussian splats render via PlayCanvas, Spark and other viewers (file 08).
- **Shaders**: GPU programs (GLSL, WGSL) for gradients, noise, distortion, liquid hovers and image transitions; tools such as Unicorn Studio and shader libraries lower the bar. Cost: GPU load, battery, and accessibility; always pause off-screen and honor reduced motion.

**Motion principles to brief with** [Craft]
- Purpose: orient, focus, give feedback, show relationships, express brand. If it does none, cut it.
- Choreography: one orchestrated hero moment beats effects scattered everywhere (house page, Page-load sequence card [internal]).
- Direction: things enter from where they logically come from; exits are faster than entrances.
- Distance and duration scale together: bigger moves take longer.
- Only animate `transform` and `opacity` where possible to protect INP and avoid layout shift (CLS).

## Design systems and tokens

- **Design tokens**: named, platform-agnostic design decisions (color, type, spacing, radius, shadow, motion). The **Design Tokens Format Module 2025.10** reached its first stable version on October 28, 2025, with theming and multi-brand support, Display P3 and OKLCH color, aliases, and tooling support in Style Dictionary, Tokens Studio and Terrazzo; Figma, Penpot, Sketch, Framer and others support or are implementing it (W3C DTCG [P]). It is a Community Group report, not a W3C Standard (W3C [P]).
- **Token tiers**: primitive (`blue-600`), semantic (`color-action-primary`), component (`button-bg`). Brand swaps happen at semantic level.
- **Theming**: define tokens on `:root`, override for dark mode with `prefers-color-scheme` and an explicit `[data-theme]` attribute (the house motion page does exactly this [internal]).
- **Motion tokens**: `duration-fast 200ms`, `duration-base 300ms`, `duration-reveal 600ms`, `ease-out cubic-bezier(.22,.8,.3,1)` (the house page's curve [internal]), `stagger 80ms`.
- **Components**: documented states (default, hover, focus, active, disabled, loading, error), content rules, accessibility notes, and code links (Figma Code Connect).
- **Governance**: a changelog, versioning, contribution path; one source of truth that exports to Figma variables and CSS.

## Accessibility (WCAG 2.2)

- **WCAG 2.2** became a W3C Recommendation on October 5, 2023 (W3C [P]).
- **1.4.3 Contrast (Minimum), AA**: text 4.5:1; large text 3:1; logotypes exempt (W3C [P]). Large text is at least 18 pt, or 14 pt bold, about 24 px or 18.5 px (W3C Understanding 1.4.3 [P]).
- **1.4.6 Contrast (Enhanced), AAA**: 7:1 and 4.5:1 for large text (W3C [P]).
- **1.4.11 Non-text Contrast, AA**: UI components and meaningful graphics 3:1 against adjacent colors (W3C [P]).
- **2.2.2 Pause, Stop, Hide, A**: moving, blinking or auto-updating content that starts automatically and lasts more than 5 seconds needs a way to pause, stop or hide it (WCAG 2.2 [P]). Marquees and autoplay video need a pause control.
- **2.3.3 Animation from Interactions, AAA**: motion triggered by interaction can be disabled unless essential (W3C [P]). Implement with `prefers-reduced-motion`.
- **2.4.11 Focus Not Obscured (Minimum), AA** (new in 2.2): sticky headers and cookie bars must not fully hide the focused element (W3C [P]). Condensing navs and pinned sections must account for this.
- **2.4.13 Focus Appearance, AAA**: focus indicator at least as large as a 2 CSS px perimeter with 3:1 change contrast (W3C [P]).
- **2.5.7 Dragging Movements, AA** and **2.5.8 Target Size (Minimum), AA**: targets at least 24 x 24 CSS px or spaced so 24 px circles do not overlap (W3C [P]).
- **Reduced motion pattern**: wrap reveals, parallax and scrubbing in `@media (prefers-reduced-motion: no-preference)`; under `reduce`, show final states instantly (house page item 12 [internal]).
- **Video**: captions for all speech, audio description or text alternatives for meaningful visuals, no flashing above three per second (WCAG 2.3.1 [P], general).
- **EU AI labels** must also be accessible (alt text or ARIA, readable duration) under the Code of Practice (European Commission icons page [P]).

## Core Web Vitals

| Metric | Measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| **LCP** Largest Contentful Paint | Loading of main content | ≤ 2.5 s | 2.5 to 4.0 s | > 4.0 s |
| **INP** Interaction to Next Paint | Responsiveness | ≤ 200 ms | 200 to 500 ms | > 500 ms |
| **CLS** Cumulative Layout Shift | Visual stability | ≤ 0.1 | 0.1 to 0.25 | > 0.25 |

- Assessed at the **75th percentile** of page loads, segmented mobile and desktop; a page passes only if all three are good (web.dev and Chrome for Developers [P]).
- INP replaced First Input Delay as the responsiveness Core Web Vital in March 2024 (web.dev Web Vitals page lists INP among the three [P]; the exact switch date was not re-verified for this file).
- Google Search recommends achieving good Core Web Vitals and says they align with what ranking systems reward (Google Search Central [P]).
- **Design decisions that move the numbers**
  - LCP: the hero image or headline is usually the LCP element. Serve it as AVIF/WebP at the right size, preload it, do not lazy-load it, do not hide it behind a JavaScript intro animation; the Page-load sequence must start immediately and end visible (the house page notes this in its CSS [internal]).
  - INP: avoid heavy JavaScript on scroll and hover; prefer CSS transforms; defer analytics; keep WebGL and shader scenes off the main interaction path.
  - CLS: reserve space for images, video, embeds, fonts (use `font-display` and size-adjusted fallbacks) and late banners; animate with transform, not layout properties.
  - Splats, 3D and autoplay video: load after first paint, use poster frames, pause off-screen.

## Conversion-centered design

### Landing page anatomy

1. **Hero**: one promise in the headline (outcome, not feature), a supporting line, one primary CTA, a visual that shows the product working. Above the fold on mobile.
2. **Social proof strip**: logos, ratings, a key number (count-up ticker is the house pattern [internal]).
3. **Problem and stakes**: name the pain in the customer's words.
4. **How it works**: three steps (pinned/sticky section pattern fits here [internal]).
5. **Benefits and features**: benefit-led headings, features as proof; bento grid for scannable modules.
6. **Testimonials and case studies**: specific, attributed, with faces and numbers (real only; no synthetic testimonials).
7. **Objection handling**: pricing clarity, guarantees, FAQ.
8. **Final CTA**: repeat the primary action with the promise restated.
9. **Footer**: trust details (address, policies, accessibility statement).

Principles [Craft]: one page, one goal; attention ratio close to 1 (minimal competing links); message match between ad and page (same promise, same visual); CTA labels as outcomes ("Get my quote") not mechanics ("Submit"); forms as short as the business allows; visible security and privacy cues near forms; test one variable at a time.

### Reading patterns and what the evidence says

- **F-pattern**: NN/g eyetracking with 232 users (2006) found users often read in an F shape (two horizontal sweeps then a vertical scan of the left side) (NN/g [I]). The 2017 revisit found it "alive and well" on desktop and mobile, mirrored in right-to-left languages, and stressed it is the default when pages give no strong cues, and that it is bad for users and businesses (NN/g [I]).
- NN/g identifies other text patterns: **layer-cake** (scanning headings and subheadings, described as the most effective scanning pattern), spotted, commitment, plus bypassing, zigzag and lawn-mower on modern layouts; the 2nd edition report draws on three large eyetracking studies over 13 years with 500+ participants (NN/g [I]).
- Design implication: write for the layer-cake. Front-load headings and the first two words of every line, use descriptive subheads, bullets and bolded keywords.
- **Z-pattern**: a common design heuristic for sparse pages (logo top-left, nav top-right, diagonal to bottom-left content, CTA bottom-right). NN/g's eyetracking catalogs do not list a Z-pattern among observed gaze patterns, though they do list a zigzag pattern on alternating text-image layouts (NN/g [I]). Treat "Z-pattern" as a composition convention, not an evidence-backed reading law.

## Web trends (2024 to 2026)

Trend descriptions are practitioner observation [R]; validate against current award sites before pitching.

- **Bento grids**: modular rounded tiles of varied size (popularized by Apple keynote slides); great for feature overviews and dashboards; risk of sameness. Use CSS Grid with named areas; collapse to a single column on mobile.
- **Brutalism**: raw HTML energy, default fonts, harsh borders, visible structure; anti-polish for culture and fashion brands.
- **Neo-brutalism**: brutalist structure with friendly color, thick black outlines, hard offset shadows, chunky type; popular in startups and SaaS for personality.
- **Glassmorphism**: frosted translucent panels via `backdrop-filter: blur()`; the house condensing nav uses a 12 px backdrop blur [internal]. Watch text contrast over busy backgrounds (WCAG 1.4.3) and GPU cost.
- **Kinetic typography**: oversized, moving, variable-font type as the hero; outlined and filled word play (the house hero uses outline-stroke words and a giant outlined parallax word [internal]).
- **AI-native interfaces**: chat or prompt as the primary control, streaming responses, agent progress states, generative previews, "ask about this page" panels; design patterns include suggestion chips, editable AI outputs, visible provenance and undo.
- **Organic textures and grain**, **3D and splat heroes**, **scroll-scrubbed product films**, **view-transition page navigation**, **dark mode by default with true theming**, **editorial layouts with huge type and generous whitespace**.
- **Anti-trend reminder**: performance and accessibility outlast styles. A beautiful page that fails LCP or contrast is a failed page.

## Award and inspiration references

- **Awwwards**: juried site of the day, honorable mentions, and developer awards; useful to study motion and interaction craft at the high end. Many winners are heavy; check their Core Web Vitals before copying patterns.
- **SiteInspire**: curated gallery filterable by style, type and subject; calmer, more editorial and typographic references.
- **Godly**: curated gallery of animated web design, strong for motion references; good for showing a client "this feeling".
- **Other useful sources** to note: Land-book and One Page Love (landing pages), Mobbin (mobile UI patterns), Codrops (creative front-end demos and tutorials), and the GSAP showcase.
- Agent practice: when citing a reference to a client, capture a screenshot or screen recording, name the specific technique using the house vocabulary, and say what to borrow (the idea, not the assets).

## Briefing templates

**Video shot list row**
```
Shot # | Size/angle | Subject + action | Lens | Move | Light | Grade | Duration | Audio | Text-on-screen | Safe-zone check
```

**Short-form edit brief**
```
Hook (0 to 2 s): [visual interrupt + line + sound]
Proposition by 3 s: [what and why]
Body: [beats, pattern interrupt every 2 to 4 s]
Payoff: [result/proof]
CTA: [spoken + on-screen, inside safe zone]
Loop: [how the end feeds the start]
Captions: [style, position]   Disclosure: [AI label needed? Y/N]
Lengths: [Reels ~12 s, TikTok ~18 s, Shorts ~25 s cut-downs from one master]
```

**Web motion brief (house vocabulary)**
```
Page-load sequence: eyebrow, headline, copy, CTAs, 100 ms apart, rise 24 px.
Scroll-reveal fade-up on sections: ~20 px, 600 ms, ease-out, once.
Stagger sequencing on cards: 80 ms.
Parallax depth on [layer]: 0.3x.
Pinned / sticky section: [which].
Scroll-scrubbing on [element]: [property from → to].
Micro-interactions: cards lift 4 px, 250 ms; links draw underline.
Count-up number ticker on stats: 1.2 s, once.
Condensing nav after 40 px. Marquee for [logos], pause on hover.
Easing: ease-out; micro 200 to 300 ms; reveals 500 to 700 ms.
Reduced motion: everything static under prefers-reduced-motion.
Performance: hero LCP element not animated in from opacity 0 via JS; only transform/opacity animated.
```

## Sources

Internal
- Bright Matter motion reference (twelve labeled techniques, values, CSS): `/home/user/bright-matter-brand/reference/motion-vocabulary.html`

Primary standards, platform and vendor docs [P]
- WCAG 2.2 Recommendation (5 Oct 2023): https://www.w3.org/TR/2023/REC-WCAG22-20231005/
- What's new in WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- Understanding 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- Understanding 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- WCAG 2.2 editor's draft: https://w3c.github.io/wcag/guidelines/22/
- web.dev, Defining the Core Web Vitals thresholds: https://web.dev/articles/defining-core-web-vitals-thresholds
- web.dev, Web Vitals: https://web.dev/articles/vitals
- Chrome for Developers, CrUX on PageSpeed Insights (threshold table): https://developer.chrome.com/docs/crux/guides/pagespeed-insights
- Google Search Central, Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Chrome, cross-document view transitions: https://developer.chrome.com/docs/web-platform/view-transitions/cross-document
- GoogleChrome modern-web-guidance, cross-document transitions (Baseline data): https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/cross-document-transitions.md
- MDN, Using the View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using
- MDN, @view-transition: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition
- MDN, animation-timeline and scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline ; https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- Webflow, GSAP becomes 100% free: https://webflow.com/blog/gsap-becomes-free ; https://community.webflow.com/updates/post/webflow-makes-gsap-100-free-fugRRt8eUL1we1k
- GSAP Standard License: https://gsap.com/community/standard-license/
- W3C Design Tokens Community Group, first stable version: https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- Design Tokens Format Module 2025.10: https://www.designtokens.org/TR/2025.10/format/
- YouTube blog, Shorts up to 3 minutes: https://blog.youtube/news-and-events/tall-updates-coming-to-shorts/
- YouTube Help, three-minute Shorts: https://support.google.com/youtube/answer/15424877
- Higgsfield Cinema Studio help: https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio
- HeyGen April 2026 release (Video Agent with Avatar V and Seedance): https://www.heygen.com/blog/heygen-april-2026-release
- Luma Ray3 (HDR EXR): https://lumalabs.ai/news/ray3
- Recraft V4 docs (Lottie export): https://recraft.mintlify.app/recraft-models/recraft-V4
- European Commission, EU icons for labelling AI content: https://digital-strategy.ec.europa.eu/en/policies/eu-icons-labelling-ai-generated-content

Independent research [I]
- NN/g, F-shaped pattern (2006): https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/
- NN/g, F-shaped pattern misunderstood but still relevant (2017, reviewed 2026): https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- NN/g, Text scanning patterns: https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/
- NN/g, How People Read Online report: https://www.nngroup.com/reports/how-people-read-web-eyetracking-evidence/
- NN/g, How people read online, new and old findings: https://www.nngroup.com/articles/how-people-read-online/

Books and craft canon [Craft]
- Walter Murch, *In the Blink of an Eye* (Rule of Six)
- Robert Bringhurst, *The Elements of Typographic Style* (measure)
- Film history: Kuleshov experiments; *Vertigo* (1958) dolly zoom; Snorri Bros. rig

Aggregators and trade press [A]
- Deepclick, TikTok ads creative best practices (quoting TikTok docs): https://deepclick.com/resources/blog/tiktok-ads-creative-best-practices/
- rule1, TikTok ad specs: https://rule1.ai/articles/tiktok-ad-specs
- AdMakeAI, vertical video dimensions 2026: https://admakeai.com/blog/vertical-video-dimensions-2026
- Reap, short-form safe zones: https://reap.video/blog/short-form-video-safe-zones
- Conbersa, video ad specs by platform: https://www.conbersa.ai/learn/video-ad-specs-by-platform-2026
- Sepia, TikTok vs Reels vs Shorts: https://sepia-lab.com/en/blog/tiktok-vs-reels-vs-shorts
- caniuse, View Transitions and scroll-driven animations: https://caniuse.com/view-transitions ; https://caniuse.com/wf-scroll-driven-animations
- css.properties, animation-timeline support: https://css.properties/animation-timeline/
