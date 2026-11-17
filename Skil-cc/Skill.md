---
name: 2d-animated-explainer-short-kit
version: 3.0.0
description: Create short-form 2D animated explainer videos with consistent human cartoon characters, reusable scenes, and credit-efficient production.
---

# 2D Animated Explainer Short Kit

## Primary visual target

Use the user's GitHub screenshot as the primary visual reference. Match its broad visual language closely: polished 2D human cartoon explainer animation, soft rounded shapes, expressive but simple faces, layered hair, recognizable clothing, gentle shading, clean silhouettes, and readable poses.

Do not default to stick figures, geometric mascots, chibi, anime, photorealism, or generic flat corporate vector art. Do not copy a specific existing character, logo, exact outfit, or proprietary asset. Create original characters in the same broad visual style.

### Character construction
- Human cartoon proportions similar to the reference: natural, slightly stylized anatomy.
- Rounded, appealing face; small simple eyes; restrained nose and mouth; clear brows.
- Hair has volume and a few readable layers, not hundreds of strands.
- Clothing has clear shapes, seams/folds only where they improve readability.
- Soft, restrained shadows and highlights. Avoid plastic 3D gloss and harsh gradients.
- Keep line weight, face scale, body proportions, palette, and shading consistent between shots.
- Hands are simple rounded mitten/oval shapes. No individual fingers, fingernails, knuckles, or forced hand anatomy. Only add a thumb-like bump if a pose absolutely needs it.
- Feet and shoes are simplified, with readable silhouettes.

## Character consistency workflow
Create a character reference sheet before scene generation. Lock:
1. character ID and name;
2. face shape, skin tone, eye and brow design;
3. hairstyle, hair color and hair silhouette;
4. body proportions and height relationship;
5. signature outfit and color palette;
6. front, 3/4 and side views;
7. neutral, happy, worried, shocked, confused, angry and sad expressions;
8. reusable standing, sitting, walking, pointing, holding and reaction poses.

Never redesign a character between scenes. Change only the expression, pose, camera framing, or explicitly requested costume. Reuse the reference image and assets wherever the chosen generator supports references.

## Animation direction
Prefer readable, restrained motion:
- idle breathing, blinking, head turns and small posture shifts;
- simple walk cycles and clean starts/stops;
- rounded mitten hands for pointing, holding and gesturing;
- clear anticipation and follow-through;
- stable body proportions and no shape-morphing;
- camera moves only when they add meaning: wide, medium, close-up, slow push-in, pan or tracking.
Avoid random limb movement, excessive bouncing, warped faces, extra limbs, finger generation, flicker, and uncontrolled camera motion.

## Scene and visual design
- Use clean 2D illustrated backgrounds with a foreground, middle ground and background.
- Keep props simple, reusable and correctly scaled.
- Use soft ambient shading and consistent light direction.
- Compose for vertical 9:16 by default; keep faces and important objects inside mobile-safe margins.
- Use wide shots to establish place, medium shots for action, and close-ups for emotion or key information.
- Background detail must support the story, not compete with the character.

## Short-form storytelling
For a 10-15 second clip:
1. 0-2s: visual hook or unusual event;
2. 2-6s: establish what is happening;
3. 6-11s: reveal, escalation or meaningful action;
4. final seconds: payoff, unanswered question, or transition to the next part.

Do not force every clip into this exact rhythm if the story needs a different beat. Every shot must communicate a visible change. Avoid static talking heads and generic filler.

## Credit-saving rules
1. Write the beat sheet and shot list before generating.
2. Generate one character reference sheet and reuse it.
3. Reuse backgrounds, props, poses and scene layouts.
4. Regenerate only the element that is wrong, not the entire scene.
5. Keep prompts structured and stable; change only scene-specific fields.
6. Use still-image generation for design approval before image-to-video.
7. Generate only the shots needed for the edit; avoid duplicate variations.
8. Keep clips short and motion simple when a longer generation adds no story value.
9. Maintain a continuity sheet for character, location, lighting, camera and timeline.
10. Never spend credits trying to fix a prompt that has not been checked for contradictions.

## Prompt order
[FORMAT / DURATION] + [VISUAL STYLE] + [CHARACTER IDENTITY] + [POSE / ACTION] + [LOCATION / PROPS] + [CAMERA] + [LIGHTING / COLOR] + [MOTION] + [CONTINUITY LOCKS] + [NEGATIVE CONSTRAINTS].

## Universal negative constraints
No stick figures, no photorealism, no 3D render, no chibi proportions, no anime redesign, no extra fingers, no individually drawn fingers, no malformed hands, no extra limbs, no face drift, no hairstyle drift, no outfit drift, no flicker, no warped anatomy, no text artifacts, no logos or watermarks.

## Platform-neutral operation
Write prompts that can be adapted to Google Flow, Dola, or another image/video generator. Do not assume a feature exists. If a platform supports reference images, seed/character references, start/end frames, or reusable assets, use them. If it does not, preserve consistency with explicit character descriptions and matching reference frames.

## Required output for each video request
- Story hook and concise narration/dialogue.
- Shot-by-shot storyboard with duration.
- Character and location continuity notes.
- Image prompt per shot.
- Motion/video prompt per shot.
- Negative constraints.
- Credit-saving note identifying reusable assets and what must actually be regenerated.


## Local character preview engine
The lightweight browser composer is in `engine-v3/`.
- Open `engine-v3/index.html` in a modern browser, or run `python -m http.server 8000` inside that folder and open `http://localhost:8000`.
- Use the composer to preview expressions, poses and palette variations before spending AI video credits.
- Start from the Bobwan Casual, Narrator, Student or Worker preset, then customize it.
- Export a PNG reference and JSON character profile; import the JSON later to restore the same character setup.
- Keep each character's PNG and JSON together as a reusable asset pair. Feed the PNG reference into a supported image/video generator to help preserve character identity.
- The browser engine is a reusable design/preview tool, not a replacement for Google Flow, Dola, or a full rigged animation package.
