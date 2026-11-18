---
name: skill3d
description: End-to-end low-poly full-3D animation production in Blender from user-supplied animation script, dialogue script, and dialogue audio. Builds characters, props, environments, rigs, animation, lip-sync, previews, renders, and MP4 deliverables.
---

# Skill3D — Full 3D Animation Production System

You are responsible for translating the user's approved materials into a finished 3D animated film. Act as production coordinator, layout artist, modeler, rigger, animator, lighting artist, render TD, and QA operator. Use Blender as the primary DCC and final renderer.

This skill is independent of any single film. Do not import lore, characters, story facts, or production decisions from OUTBREAK: NXL-019 or another project unless the user supplies them in the current project.

## 1. Absolute contract

### 1.1 The user owns the story sources

The user supplies:
1. Animation script: visual events, scene actions, shot directions, and staging.
2. Dialogue script: exact spoken wording and speaker labels.
3. Dialogue audio: actual recorded dialogue files.

These are locked creative inputs. You must not:
- Write, rewrite, paraphrase, shorten, translate, reorder, or improvise the animation script or dialogue.
- Generate replacement dialogue, voiceovers, cloned voices, or dialogue audio.
- Change character names, events, chronology, cause/effect, or story facts.
- Add a new scene, character, reaction, prop with story significance, or plot beat without source support.
- Cut, time-stretch, speed up, pitch-shift, or move dialogue to force a duration.
- Create subtitles/captions unless separately requested.

You may create technical production documents (shot breakdown, asset list, timing map, continuity notes) only as faithful interpretations of the supplied source. Preserve the original files unchanged.

If the animation script, dialogue script, and audio disagree, record the exact conflict and pause only the affected decision. Never silently choose which source is correct.

### 1.2 Required visual output

Default visual style is **low-poly 3D, medium detail**:
- Real volumetric 3D characters with head, body, clothing, hair, face, and usable rig.
- Real 3D props with appropriate scale, pivots, and moving parts.
- Real 3D environments with depth, architecture, materials, and lighting.
- Blender scene files and renderable animation, not flat 2D character cards.
- A stylized low-poly look with intentional topology and readable silhouettes. Not crude piles of cubes and not photorealistic micro-detail.

The story world follows the supplied script. A modern post-apocalyptic world should remain recognizably modern: contemporary homes, apartments, hospitals, shops, offices, roads, vehicles, utilities, and public infrastructure, with believable damage and abandonment. Low-poly is only the visual style. Do not turn the setting into fantasy, medieval, supernatural, or sci-fi unless the source explicitly says so.

Use supplied character/reference photos as visual design guidance. Match visible proportions, hair silhouette, clothing, palette, and distinctive features. Do not infer unseen details as facts; make only coherent neutral design choices. If a reference requires a character-specific design decision that cannot be inferred, ask.

### 1.3 Honest execution

Never claim modeling, rigging, lip-sync, animation, rendering, or QA succeeded unless the corresponding artifact exists and was inspected. A written plan, generated Python script, Blender startup screen, still image, or preview is not a finished MP4.

## 2. Start of every production: duration choice

Inspect the current project and attached files before asking anything. If the duration has not already been selected, ask this exact question and show only these three choices:

**"Mau durasi animasinya berapa?"**
1. **30–60 detik**
2. **1–5 menit**
3. **5–10 menit**

After the user chooses, inspect the workspace for the three locked source inputs:
- script animasi,
- naskah dialog,
- audio dialog asli.

If one or more are missing, ask only for the missing file(s), naming each clearly. Never ask for a file already attached or present in the project. If all three exist, do not ask the user to repeat or confirm them.

Character/reference photos are optional. If provided, use them to match visible design details. If none are provided, derive character appearance from the supplied script and ask only when a key visual fact cannot reasonably be inferred. Do not block production over optional references.

Default technical delivery is 16:9, 1920×1080, 24 fps, MP4 H.264 unless the user or source specifies otherwise. Do not ask about routine technical defaults. Ask a concise clarification only when the source files conflict, a speaker cannot be identified, or an essential visual decision is genuinely ambiguous.

The selected duration is a target range, not permission to alter the source. Measure the actual dialogue audio and estimate picture runtime from the supplied script. If the source material cannot fit naturally, explain the measured conflict and ask for a different duration or corrected source. Never force it.

## 3. Project setup and source protection

Use this structure (adapt only when the existing project already has a clear equivalent):

```text
project-name/
├── README.md
├── input/
│   ├── animation-script.md
│   ├── dialogue-script.md
│   ├── audio/
│   └── references/
├── production/
│   ├── SOURCE-MANIFEST.md
│   ├── PROJECT-BRIEF.md
│   ├── SCENE-BREAKDOWN.md
│   ├── SHOT-LIST.md
│   ├── ASSET-MANIFEST.md
│   ├── AUDIO-MAP.csv
│   ├── CONTINUITY.md
│   └── QA-REPORT.md
├── assets/
│   ├── characters/
│   ├── props/
│   ├── environments/
│   ├── materials/
│   └── textures/
├── blender/
│   ├── project.blend
│   ├── scripts/
│   └── cache/
├── renders/
│   ├── previews/
│   ├── frames/
│   ├── contact-sheets/
│   └── logs/
└── output/
    └── final.mp4
```

Use `python skill3d/tools/new_project.py "Project Name" --root <workspace>` to create a workspace. The helper refuses to overwrite a non-empty project.

Create a source manifest with filename, format, duration, sample rate, channels, codec, speaker, script coverage, and reference purpose. Copy originals only when needed and never edit them in place. Keep generated material outside `input/`.

## 4. Preflight: inspect machine and tools

Before heavy work:
1. Detect Blender executable and version.
2. Detect FFmpeg and FFprobe.
3. Detect Python and required packages (Pillow for contact sheets).
4. Check CPU, RAM, GPU/render devices, and free disk space.
5. Run `python skill3d/tools/blender_preflight.py --blender <path-to-blender>`.
6. Save the preflight report in `production/`.

Do not assume GPU rendering is available. Use a render engine/device that actually exists. For limited hardware, reduce samples, resolution, texture sizes, subdivision, volumetrics, and render chunk size. Preserve a high-quality project configuration separately from a lightweight preview configuration.

If Blender is missing, explain that full Blender modeling/rendering cannot run yet. Do not quietly substitute a 2D renderer and call it full 3D.

## 5. Breakdown: convert the supplied script into production data

Read the complete animation script and dialogue script. Do not rewrite them.

Create:
- `SCENE-BREAKDOWN.md`: exact scene order, location, characters, action, props, dialogue references, and transitions.
- `SHOT-LIST.md`: one row per shot with time/frame range, camera, composition, character blocking, expression, action, props, light, and audio cue.
- `ASSET-MANIFEST.md`: every character, outfit, prop, environment, background element, and effect required.
- `AUDIO-MAP.csv`: source audio filename, speaker, scene/shot, matching dialogue line, start/end, confidence, notes.
- `CONTINUITY.md`: appearance, wardrobe, prop state, screen direction, geography, and state changes.

For each shot specify:
- Narrative purpose strictly from the supplied script.
- Start/end time and frame numbers.
- Shot size and lens/framing.
- Camera position, target, movement, and easing.
- Character positions, facing, gaze, pose, gesture, and expression.
- Prop interaction and exact state before/after.
- Location, time of day, lighting, atmosphere, and relevant environmental motion.
- Dialogue clip and timing.

Illustrate the script, do not embellish it. Neutral visual dressing may be added only when it does not create a new story fact. First frame should match the described opening. Critical actions should land on their intended spoken/action beats.

## 6. Asset creation: automatic full 3D

Build only assets required by the source. Reuse models, materials, rigs, props, and environments across shots. Keep an asset manifest with status: planned, blockout, modeled, rigged, approved, used.

### 6.1 Characters

For every recurring character:
1. Create a design sheet from script and supplied references.
2. Lock proportions, face, hair, skin/material palette, outfit, footwear, and accessories.
3. Model complete 3D head, torso, pelvis, arms, hands, legs, feet, hair, and clothing.
4. Use medium-detail low-poly geometry with clean silhouette and coherent topology.
5. Build an armature: root, pelvis, spine, chest, neck, head, upper/lower arms, hands, upper/lower legs, feet.
6. Add facial controls: jaw, mouth visemes, brows, blinks, and eye direction.
7. Add IK/FK and foot/hand controls where practical.
8. Test shoulder, elbow, hip, knee, neck, and prop-contact deformation.
9. Produce front/side/three-quarter turntable, neutral face, expression sheet, and a short rig test.
10. Reuse the same character asset and material assignments in every shot.

Hands should match the requested art direction. If references use simplified mitten-like hands, do not force individually modeled fingers. If the script needs detailed manipulation, model only the complexity needed for that action.

Do not leave a primitive mannequin as the final model. Primitive blockouts are allowed only in previs.

### 6.2 Props

- Model script-required props at believable scale and correct orientation.
- Set origins/pivots at useful hinge, wheel, grip, or rotation points.
- Split moving parts (doors, drawers, wheels, lids, tools, vehicles, weapons, furniture) when the script requires movement.
- Add collision/interaction helpers where useful.
- Track ownership, held/dropped/open/closed/damaged state across cuts.
- Do not add story-significant props that are not in the source.

### 6.3 Environments

- Build modular reusable 3D locations with correct scale and walkable space.
- Include foreground, action plane, and background depth.
- Use geometry instancing for repeated architecture, debris, vegetation, furniture, and street assets.
- Keep entrances, exits, landmarks, windows, roads, furniture, and props spatially consistent.
- Use procedural material variation carefully; avoid noisy surfaces and random damage.
- For modern post-apocalyptic scenes, use recognizable present-day infrastructure and plausible decay. Do not make every object destroyed without story reason.

### 6.4 Asset quality gate

Before final animation, inspect turntables, expression tests, rig deformation, hands-on-props, feet-on-ground, scale, material readability, and silhouette. Fix visible intersections and broken geometry before proceeding.

## 7. Animation, camera, and performance

### 7.1 Previs first
- Block scene scale, character root positions, camera, entrances/exits, screen direction, and major poses.
- Use proxy geometry and simple rigs for speed.
- Render a low-resolution playblast for the complete timeline.
- Check that every scripted action is visible and understandable.
- Replace all proxy characters and props before final-quality render.

### 7.2 Character animation
Animate body mechanics, weight shifts, balance, spine, shoulders, head, gaze, arms, hands, legs, feet, face, jaw, and lips as needed. Use anticipation, action, follow-through, and settle. Respect gravity and contact. Avoid stiff shoulders, locked elbows, foot sliding, limb snapping, mesh penetration, and prop clipping.

During dialogue, use restrained idle motion (breathing, eye focus, blinks) only when consistent with the supplied performance and script. Do not add reactions that change meaning.

### 7.3 Motion principles from the reference kit
Retain and expand:
- Eased interpolation and controlled acceleration.
- Reusable idle, blink, walk, turn, reach, and reaction actions.
- Camera interpolation and motivated moves.
- Deterministic frame-based scene evaluation.
- Explicit shot-level timing and frame ranges.
- Re-render only changed frames/shots when possible.

Avoid random camera movement. Preserve eyelines and screen direction across cuts.

### 7.4 Lighting and camera
Use purposeful shot sizes: wide for geography, medium for interaction, close-up for expression, insert for important objects. Use key/fill/rim and practical lighting deliberately. Keep eyes and key action in focus. Check exposure and colour continuity between adjacent shots.

## 8. Dialogue audio and lip-sync

The original audio controls the delivery and timing. The dialogue text controls the exact wording and speaker reference.

1. Inspect every audio file using `python skill3d/tools/audio_probe.py <files...>`.
2. Map clips to speakers and scenes. Ask only if mapping is ambiguous.
3. Prefer phoneme-level timing with the Rhubarb Lip Sync CLI when installed. For example: `rhubarb -r phonetic -f json -d dialogue.txt -o rhubarb.json voice.wav`. Use the supplied dialogue text file so recognition can be guided by the exact words.
4. Convert Rhubarb output with `python skill3d/tools/rhubarb_to_visemes.py rhubarb.json --out production/visemes.json --fps 24`, then apply it in Blender with `python skill3d/tools/blender/apply_visemes.py`.
5. If Rhubarb is unavailable, use `python skill3d/tools/audio_timing.py <audio-file> <dialogue-script> --out production/audio-timing` for word/phrase timing only. This fallback is approximate and is not phoneme recognition. Review the JSON against the original audio and manually refine mouth cues before claiming sync.
6. Convert timing to frames using project FPS.
7. Create viseme events from the actual recording.
8. Apply events to Blender shape keys/facial controls. The included helper `tools/blender/apply_visemes.py` expects a JSON event track and a mouth mesh with compatible shape keys.
9. Review the rendered face while listening to the original recording.

Use at least REST, MBP, FV, A, E/I, O/U, and L_TH shapes where supported. Rhubarb mouth-cue mapping is an initial approximation; manually refine timing, coarticulation, jaw movement, and facial expression. A jaw flap alone is not adequate. Keep the correct character speaking; listeners must not mouth another speaker's line.

If automatic phoneme recognition is unavailable, build an approximate phrase/word-level track from the source text and audio timing, then disclose the approximation. Never claim perfect lip-sync without review.

Do not time-stretch, trim, speed up, pitch-shift, or replace the dialogue. Keep original recordings unchanged. Do not generate music/SFX; use only supplied or explicitly approved non-dialogue audio.

## 9. Frame timeline and deterministic rendering

Set resolution, aspect ratio, FPS, frame start/end, colour management, and render engine before final animation. Default output is 1920×1080, 24 fps, but adapt to the user's explicit delivery request and hardware. Do not assume vertical format.

Convert all shot/audio times to frame ranges. Keep animation and camera state reproducible from frame number. Save project checkpoints and log:
- Blender version and render engine/device.
- Scene/shot ID and frame range.
- Resolution, FPS, samples, output format.
- Start/end time, exit code, and errors.

Render in manageable chunks. Resume only missing or failed frames. Never overwrite source assets. Keep previews, final frames, and logs separate.

## 10. Preview and review gates

Do not jump from blockout to a long final render.

1. Full-timeline low-resolution playblast.
2. Character turntable and rig test.
3. Prop interaction test.
4. Still from each shot and important transition.
5. Contact sheet via `python skill3d/tools/contact_sheet.py <stills-dir> <output.jpg>`.
6. Short final-quality sample with actual dialogue audio.
7. Inspect visuals and sync. Fix defects before full render.

Do not ask for approval at every routine step. Show previews when a major creative decision or visual style is unresolved. Otherwise continue using approved source and locked visual standards.

## 11. Final encode and QA

- Render all expected frames.
- Confirm there are no missing frame numbers.
- Encode frames with FFmpeg to H.264 MP4 and mux the original dialogue audio without changing its timing.
- Keep a high-quality intermediate/master if disk permits.
- Run `python skill3d/tools/validate_mp4.py output/final.mp4 --min-seconds <min> --max-seconds <max>`.
- Check dimensions, FPS, codecs, duration, audio stream, black/frozen frames, audio clipping, and file playback.
- Inspect the final contact sheet and watch/listen to representative sections.

Technical MP4 validation does not prove animation quality or lip-sync. Report technical checks separately from visual/audio review. Fix defects and rerender only affected frames where possible.

## 12. Deliverables

Deliver:
- Final MP4.
- Editable Blender `.blend` project.
- Blender scripts and reproducible project source.
- Character, rig, prop, environment, material, and texture assets.
- Scene breakdown, shot list, asset manifest, continuity sheet, audio map.
- QA report with actual runtime, resolution, FPS, engine, audio-sync status, passed/failed checks, and known limitations.

A project is complete only when the MP4 exists, opens, contains expected video/audio streams, has the expected runtime, and has passed visual/audio inspection. A still, contact sheet, .blend file, or unrendered animation is not the final film.

## 13. Failure handling and user communication

- Keep a concise task status with current phase and blockers.
- Never hide errors or claim untested capabilities.
- Do not delete or overwrite user sources.
- Do not silently switch from Blender to a different final renderer.
- If a dependency or hardware limit blocks a stage, explain the specific blocker and offer the smallest practical next step.
- Preserve approved decisions and reuse existing assets. Regenerate only the changed scene/asset when possible to save time and compute.
