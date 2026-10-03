# Margaux: generation prompts

**Face reference:** always attach Higgsfield job 88bc4ef2-740d-4a9e-b38e-04df858ebad9 (casting #1 with locked eyes, 3 Oct 2026) as the image reference so the face stays hers. After the Soul ID is trained, use the Soul ID instead. The original casting still f47ed34b is superseded.

## Master prompt (paste as-is, then add one line from the shot list)

> Margaux, a strikingly beautiful woman in her early 30s from New York old money. Long, heavy, dark brown almost black hair with a soft natural wave, worn loose. Strong straight dark brows, open almond eyes with softly lifted outer corners, very light pale sea-glass grey-green irises (silvery grey with a cool green tint, identical in both eyes), pale olive skin with natural texture, high cheekbones, a calm, unreadable half-smile. Minimal makeup, bare lips, no visible lipstick. She wears a loose black men's silk shirt unbuttoned to a deep V, no cleavage because she is too thin, sleeves slightly pushed up, stacked antique silver rings and one worn silver signet ring on her right hand. Grounded, intelligent, quietly amused, effortlessly rich, never posing. Setting: a private archive library fully color-drenched in deep oxblood (walls, paneling, built-in bookcases and ceiling all the same color), floor-to-ceiling aged books, card catalog drawers with brass label holders, bundled letters tied with twine. Lit only by Tiffany-style stained-glass lamps casting warm jewel-colored light on her face, plus a candle. Photorealistic 35mm film photograph, shallow depth of field, natural skin, subtle film grain.

**Avoid:** heavy makeup, red or dark lipstick, gold jewelry, bright or overhead lighting, cold blue light, gothic props, a buttoned-up or high-collared shirt, plastic or airbrushed skin, cartoonish features.

## Shot list for the Soul ID training set (about 25 images)

Add one of these to the end of the master prompt. Keep everything else identical.

**Angles (8)**
1. Front-facing head and shoulders portrait, looking straight into the camera.
2. Three-quarter view facing left, head and shoulders.
3. Three-quarter view facing right, head and shoulders.
4. Full left profile, looking at the bookshelves.
5. Full right profile, reading a letter.
6. Slightly high angle, looking up at the camera from the desk.
7. Waist-up, standing at the card catalog, turned toward the camera.
8. Full body, standing in the middle of the library, hands in pockets.

**Expressions (6)**
9. Neutral and unreadable, lips closed.
10. Slow half-smile, as if she knows something you don't.
11. Genuine laugh, eyes creased, head tipped back slightly.
12. One eyebrow raised, dry skepticism.
13. Eyes closed, smelling her own wrist after spraying perfume.
14. Mid-sentence, explaining something, one hand gesturing.

**Actions with perfume (5)**
15. Holding a small dark glass perfume bottle near her collarbone.
16. Spraying perfume onto her wrist, mist visible in the lamplight.
17. Uncorking a vintage glass flacon at the desk.
18. Writing a label on an archive card with a fountain pen.
19. Pulling a perfume bottle out of a card catalog drawer.

**Lighting and room variation (6)**
20. Same scene but the forest green color-drenched archive with perfume cabinets.
21. Same scene but the tobacco brown two-level archive.
22. Lit mostly from one green-and-amber Tiffany lamp on her left, deep shadow on her right.
23. Candlelight only, close-up portrait.
24. Seated in a cognac leather wingback chair, legs crossed, reading.
25. Close-up of her hands with the silver rings holding a perfume bottle (no face).

## Settings

- Model: Higgsfield Soul 2.0 or Nano Banana Pro with the face reference.
- Aspect ratio: 3:4 for the training set (more face detail), 9:16 for content.
- One image per prompt. Discard any where the face drifts before training.

## Voice: ElevenLabs Voice Design prompt

**Voice description (paste into "Describe the voice"):**

> A woman in her early 30s from Manhattan old money, raised on the Upper East Side and educated at a New England boarding school. Refined American accent: crisp consonants, relaxed rounded vowels, a faint mid-Atlantic polish, no regional twang and no vocal fry. Low, warm alto with a slight natural huskiness, rich in the chest. Speaks slowly and deliberately, with confident pauses, like someone who has never had to raise her voice to be listened to. Dry, intelligent, quietly amused, warm underneath. Intimate, close-mic, studio-quality recording.

**Preview text (paste into the text box):**

> People expect me to smell like roses. I smell like a cathedral after the candles go out. This one has real frankincense in it. Edie wore it to a gallery opening and came home with somebody's husband's cufflinks. I wear it to read.

**Variations to try if the first round misses:**
- *Deeper:* add "deep, smoky alto, lower than average for a woman."
- *More old-Hollywood:* swap the accent line for "a 1940s mid-Atlantic accent like a classic film actress, softened for today."
- *Less polished:* add "a little gravel from late nights, relaxed and unbothered."

**Settings:** Voice Design v3. If previews drift from the description, raise "guidance" (prompt strength). Generate a few rounds and save the one that sounds like she owns the building.

### Voice design round 2 (3 Oct 2026, Manhattan old-money prompt)
Previews: MA g4c0KwLikiqhZVbQV2uc, MB sUmuuTBr3zOZA8XpAcEb, MC gqaVTrnel9yDInI3JvwZ (view viewstate_01m3znmmaqe9zvqn9azdvay215). Round 1 (M1 to M3) is logged in vesper-id-ledger.md.

### Voice design round 3 (3 Oct 2026, transatlantic "Locust Valley lockjaw", guidance 8)
Description: Upper East Side old money, pronounced transatlantic accent, slightly clenched jaw, non-rhotic Rs, broad A's, crisp T's, half British half Manhattan, low warm alto, dry and quietly amused, not a parody.
Previews: T1 SJJfz8p4huCPCjO6hb1T, T2 L2fsqHouyowafL2u0849, T3 4eCvKqkzEojCBLLY4zxp (view viewstate_01m3znyb0sfn49c83wnx1zabze)

**LOCKED 3 Oct 2026: Margaux's voice = T2**, saved in ElevenLabs as "Margaux", voice_id L2fsqHouyowafL2u0849.
