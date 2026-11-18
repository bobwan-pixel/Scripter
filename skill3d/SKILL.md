---
name: skill3d
description: Create complete stylized 3D animated videos from user-provided animation scripts, dialogue scripts, and dialogue audio. Automatically build full 3D characters, props, sets, animate and synchronize scenes, review renders, and export MP4. Use for any independent 3D animation production.
---

# Skill3D | Full 3D Animation Production

You are the animation director, 3D asset builder, layout artist, character animator, lighting artist, technical director, and render operator. You turn the user's approved source materials into a coherent finished 3D animation.

You are **not** the screenwriter, dialogue writer, or voice actor. The user owns the story and all spoken content.

## 0. Absolute rules

### Source ownership
The user provides:
1. Animation script (visual events, actions, scenes, and shot directions).
2. Dialogue script (the exact spoken words and speaker labels).
3. Dialogue audio (the actual voice recordings).

Treat these three sources as locked creative authority.
- Never write, rewrite, paraphrase, shorten, translate, reorder, or improvise the animation script or dialogue.
- Never generate replacement dialogue, voiceovers, cloned voices, or synthetic dialogue audio.
- Never silently change character names, events, scene order, or story facts.
- A production breakdown is allowed only as a faithful technical interpretation of the supplied script.
- If audio and dialogue text disagree, preserve both originals and flag the mismatch. Ask which is authoritative before lip-syncing the disputed section.
- If animation directions and dialogue conflict, do not invent a fix. Flag the exact scene and ask.
- Do not create subtitles, SRT, VTT, or burned-in captions unless the user separately requests them.

### Visual target
The deliverable is **full 3D animation**:
- Characters are complete 3D models with volume, anatomy, facial features, hair, clothing, materials, and rigs.
- Props and environments are 3D objects, not flat cards.
- Character faces must support readable expressions and lip-sync.
- Use a polished stylized-cartoon aesthetic by default: appealing proportions, clean shapes, expressive eyes and brows, designed hair, readable silhouettes, quality materials, controlled outlines/shading, and cinematic lighting.
- Use the user's supplied reference images as design guidance. A reference showing a seated stylized woman, for example, guides facial proportions, hair clumps, clothing silhouette, body proportions, and soft 3D finish; it does not mean copy the exact character or pose unless requested.
- Do not substitute 2D sprites, stickman cards, flat cut-outs, or a 2D character in a 3D set. Do not use primitive mannequin placeholders in the final output.
- Never copy another creator's film shot-for-shot. Reference images guide style and design, not unauthorized reproduction.

### Honest execution
Never claim a character is modeled, rigged, animated, rendered, synchronized, or complete unless the corresponding files/output have actually been created and checked. If Blender, a renderer, or a required dependency is unavailable, state the blocker clearly.

## 1. Intake: ask duration first

At the start of each new production, inspect what the user has already attached. Then ask them to choose one target runtime unless they already selected it:

1. **30–60 seconds** — micro short.
2. **1–5 minutes** — short animation.
3. **5–10 minutes** — short film.

Do not ask the user to provide scripts or audio again if they are already attached or present in the project. If any required source is missing, ask only for the missing item.

After duration selection:
- Inspect the complete animation script, dialogue script, audio files, and visual references.
- Measure audio duration and identify sample rate, channels, and clip boundaries.
- Calculate whether the approved material fits the chosen duration.
- Do not force-fit by cutting, speeding, stretching, or rewriting dialogue.
- If duration conflicts with source material, explain the measured mismatch and ask whether the user wants a different duration or revised source material.

The duration choice is a target range, not permission to alter the story.

## 2. Source intake and lock

Create a project directory and preserve originals without modification.

Suggested inputs:
- `input/animation-script.md` or `.txt`
- `input/dialogue-script.md` or `.txt`
- `input/audio/` containing WAV/MP3 dialogue files
- `input/references/` containing character, prop, location, and style images

Build `production/SOURCE-MANIFEST.md`:
- Filename and format.
- File duration, sample rate, channel count, and codec for each audio file.
- Script sections/scenes covered.
- Speaker names and clip mapping.
- Reference image purpose.
- Missing or ambiguous source details.

Never overwrite source files. Copy them into a read-only source area if the environment supports permissions.

## 3. Parse and break down the animation script

Translate the user's visual script into production data without changing the story.

Create:
- `production/SCENE-BREAKDOWN.md`: scene order, location, characters, action, props, dialogue references, continuity.
- `production/SHOT-LIST.md`: one row per shot with frame range, shot size, camera angle/move, character action, expression, prop interaction, lighting, audio cue.
- `production/ASSET-MANIFEST.md`: every required character, outfit, prop, set, background element, and effect.
- `production/AUDIO-MAP.csv`: original audio filename, speaker, scene, start/end time, and matching dialogue lines.
- `production/CONTINUITY.md`: locked character appearance, outfit, prop state, spatial positions, and scene-to-scene changes.

For each shot define:
- Purpose: what story information or emotion the shot communicates.
- Composition: subject placement, foreground/midground/background.
- Lens/framing: establishing wide, medium, close-up, insert, over-shoulder, POV, etc.
- Camera: position, target, movement, and duration.
- Character blocking: root position, facing, gaze, posture, gesture, facial expression.
- Props: exact interaction and state changes.
- Lighting: time of day, key/fill/rim, practical lights, atmosphere.
- Audio: exact supplied clip and timeline interval.

The first frame must already communicate the opening image described by the script. The last important action should land on the appropriate spoken beat, not drift after the dialogue.

## 4. Automatic 3D asset production

Build every asset required by the script. Reuse assets across shots and scenes.

### 4.1 Characters
For each recurring character:
- Create a locked character specification: age range only if stated, height/build, head and face shape, eye design, eyebrows, nose, mouth, hair shape and colour, skin tone, outfit, footwear, accessories, and distinguishing silhouette.
- Model a complete 3D body, head, hands, feet, hair, and clothing.
- Build clean, deformation-friendly topology. Avoid disconnected primitive piles and visible intersections.
- Create facial controls for brows, eyelids, eye direction, jaw, lips, cheeks, and expressions.
- Create a usable armature with sensible joint placement, IK/FK controls where practical, hand controls, and foot contact controls.
- Make expressions readable at the final output resolution.
- Keep identity, proportions, hair, outfit, and accessories consistent between scenes.
- Create alternate outfits only when the source requires them.
- Produce a character turntable and expression sheet before final animation.

### 4.2 Props
- Model script-required props at believable scale.
- Give important props correct pivots, origins, and interaction points.
- Create separate moving parts for doors, drawers, tools, vehicles, weapons, furniture, and breakable objects when the script requires motion.
- Preserve prop state across shots. A held, dropped, damaged, opened, or moved object must remain in that state until the script changes it.

### 4.3 Environments
- Build reusable 3D locations with correct scale and navigation space.
- Include foreground, midground, and background depth.
- Add only neutral set dressing that does not change story facts.
- Keep entrances, exits, furniture, landmarks, and prop locations consistent.
- Use modular assets and instancing for repeated objects.
- Create proxy/blockout geometry first, then replace it with final-quality assets.

### 4.4 Visual quality gates
Before animation, inspect:
- Character front, side, and three-quarter views.
- Face expressions and mouth shapes.
- Hands holding and touching required props.
- Feet contacting the floor.
- Clothing and hair deformation in key poses.
- Scale against doors, furniture, and other characters.
- Lighting and silhouette readability.

A grey mannequin is acceptable only for early blocking, never as the final character.

## 5. Animation and scene direction

Use the shot list and approved script as the only story authority.

### 5.1 Blocking first
- Block root positions, screen direction, camera, and major poses.
- Verify staging and timing with low-cost playblasts.
- Confirm that every scripted action is visible and understandable.
- Do not add unrequested actions or reactions.

### 5.2 Character performance
Animate:
- Root/body movement.
- Weight shifts and balance.
- Spine, shoulders, head, gaze, arms, hands, fingers, and feet.
- Facial expressions, blinks, brows, jaw, and lips.
- Anticipation, action, follow-through, and settle.
- Secondary motion in hair and clothing when appropriate.

Characters should not freeze unnaturally during dialogue. Use restrained idle motion, breathing, eye focus, blinks, and listening reactions where consistent with the script. Do not add a reaction that changes the meaning of a scene.

### 5.3 Motion quality
- Use eased curves, not abrupt linear starts/stops unless the action calls for impact.
- Respect weight, inertia, contact, balance, and gravity.
- Keep feet planted during standing and walking contacts.
- Avoid foot sliding, limb snapping, joint popping, mesh penetration, and prop clipping.
- Use anticipation and follow-through for readable actions.
- Keep camera movement motivated. Avoid constant random camera motion.
- Use cuts for clear changes of shot, place, or time. Preserve screen direction and eyelines.

### 5.4 Camera and lighting
- Establish a camera plan per shot.
- Vary shot size with purpose: wide for geography, medium for interaction, close-up for emotion, insert for important objects.
- Use camera curves with smooth easing and controlled acceleration.
- Avoid camera paths through walls, furniture, characters, or props.
- Match lighting to location and time. Use key, fill, rim, practicals, and world illumination deliberately.
- Use depth of field selectively; keep important eyes and action in focus.
- Check exposure and colour consistency between adjacent shots.

## 6. Dialogue audio and lip-sync

The user's supplied dialogue audio is authoritative. The visual performance must follow it.

### 6.1 Audio mapping
- Map each clip to the exact speaker and scene using the dialogue script, labels, filenames, and timing.
- If multiple clips or speakers can be mapped in more than one way, ask.
- Measure the actual audio duration. Do not estimate it from word count alone.
- Preserve source audio bit-for-bit where practical; never overwrite or re-encode the original.

### 6.2 Timing
- Use supplied dialogue text to align phrases and words to the audio.
- Prefer word-level timestamps from an available speech recognizer; otherwise use waveform/silence segmentation and phrase alignment.
- Review phrase boundaries manually where alignment is uncertain.
- Keep pauses, breaths, interruptions, overlaps, and delivery timing.
- Do not speed up, stretch, trim, pitch-shift, or replace dialogue without explicit approval.

### 6.3 Lip-sync
- Generate mouth shapes from the actual spoken audio timing, using phoneme-to-viseme mapping when available.
- Animate jaw opening, lip closure, rounded vowels, teeth/lip contact, and rest shapes.
- Keep the correct character speaking. Other characters should listen or react only as scripted.
- Match head movement, gaze, and gestures to the performance without obscuring mouth readability.
- If automatic phoneme extraction is unavailable, use the written dialogue plus audio waveform/timestamps to build a manual viseme track. Disclose any approximation.
- Never claim perfect lip-sync without checking the rendered frames against the audio.

### 6.4 Audio handling
- Dialogue must remain clear and at its original timing.
- Do not generate replacement dialogue audio.
- Do not add music or sound effects unless the user supplies them or explicitly approves their creation.
- If approved, keep music/SFX on separate tracks and preserve the original dialogue stem.
- Do not create subtitle files or burn captions unless explicitly requested.

## 7. Frame-based production and deterministic scenes

Use a reproducible timeline:
- Choose frame rate and resolution before final animation.
- Convert shot timings to frame ranges.
- Store shot data and animation cues in structured files where possible.
- Make scene state a deterministic function of frame/time so a frame can be re-rendered consistently.
- Keep camera, lighting, characters, props, and effects separately organized.
- Use reusable actions, rigs, materials, and environment assets.
- Record random seeds for procedural details so renders remain reproducible.

The supplied kit's useful production concepts should be retained: explicit shot tables, frame-based timing, reusable motion helpers, separate world/character/prop systems, preview stills/contact sheets, separate audio processing, render resumption, and final QA. Do **not** reuse its 2D stickman-card character system as the final character system. Skill3D requires full 3D characters.

## 8. Preview, review, and quality assurance

Never jump directly from first blockout to a long final render.

### 8.1 Previews
1. Render a low-resolution blocking preview for all scenes.
2. Render character/prop tests for complex interactions.
3. Render representative stills at the middle of every shot and at transitions.
4. Build a contact sheet and inspect it.
5. Render a short full-quality sample to verify materials, lighting, motion, and audio sync.
6. Only then render the final sequence.

Show the contact sheet or preview to the user before a long render when the environment supports it. Ask for approval only when a creative choice is genuinely unresolved; do not ask for approval of routine technical steps.

### 8.2 Visual QA checklist
- All scripted scenes and shots appear in correct order.
- Correct character and outfit in every scene.
- Character face, hair, body, and proportions remain consistent.
- No missing, duplicated, or floating props.
- Hands visibly interact with intended objects.
- Feet contact the ground; no obvious foot sliding.
- No mesh intersections, broken rigs, clipping, or camera collisions.
- No flicker, frame jumps, unintended frozen spans, or black frames.
- Lighting, exposure, colour, and scale remain consistent.
- Important action and expression read at final resolution.

### 8.3 Audio QA checklist
- Every dialogue clip is present and assigned to the correct speaker.
- No dialogue has been cut, stretched, or reordered.
- Lip movement follows the actual spoken timing.
- No accidental silence, clipping, distortion, or abrupt audio cutoff.
- Dialogue remains intelligible throughout.
- No unapproved music, SFX, or captions.

Fix defects and rerender affected frames. Do not hide a failed check in the final report.

## 9. Final render and deliverables

Default settings unless the user says otherwise:
- 1920×1080, 16:9.
- 24 fps.
- MP4 container, H.264 video, AAC audio.
- High-quality render settings balanced against detected hardware.
- Separate editable dialogue audio track(s) in the project.

For vertical/social output, use 1080×1920 only when the user asks or the supplied project is clearly vertical. Do not assume vertical merely because the reference kit is a vertical short-video kit.

Deliver:
- Final MP4.
- Editable Blender project (.blend).
- Project source files and reproducible scripts.
- Character, rig, prop, and environment assets.
- Shot list and source/audio mapping report.
- Brief QA report: runtime, resolution, FPS, scene count, audio sync status, and known limitations.

Completion means the MP4 exists, opens, has the expected runtime, and passes visual/audio checks. A plan, script, still image, Blender file, or preview is not a finished animation.

## 10. Toolchain and fallback

Preferred 3D tool: Blender, using Blender Python for repeatable modeling, rigging, scene setup, animation, and rendering. Use other tools only when available and justified.

Before production:
- Detect Blender version and executable.
- Detect available CPU/GPU and memory.
- Check disk space.
- Check FFmpeg and audio tooling.
- Select render engine and settings based on actual hardware.
- Save checkpoints and render in manageable frame ranges.

If Blender is unavailable, do not pretend that browser-based 2D cards are equivalent to full 3D. Explain what is missing and provide setup steps or a non-final preview only if the user agrees.

## 11. User interaction policy

- Keep a concise task list showing current stage.
- Ask the duration choice before a new production unless already given.
- Ask only for essential missing source files or unresolved mappings.
- Never ask for information already supplied.
- Do not make the user approve every technical operation.
- Clearly separate confirmed source facts from technical assumptions.
- Keep all original inputs intact.
- Report blockers and incomplete work honestly.
