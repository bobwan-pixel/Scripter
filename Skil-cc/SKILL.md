---
name: skil-cc-animation-production
description: Produces original full-3D animated films lasting 5–10 minutes from repository screenplays, dialogue, character bibles, world guides and asset manifests. Use when planning, scripting, storyboarding, modeling, rigging, animating, editing, validating or rendering a Skil-cc film.
---

# SKIL-CC — Full 3D Film Production Skill

## Mandatory startup: read the project, not just this file
Before doing any work:
1. Read `PROJECT-INDEX.md`.
2. Read all active project source files that exist:
   - `projects/active/SCREENPLAY.md`
   - `projects/active/CHARACTERS.md`
   - `projects/active/WORLD.md`
   - `projects/active/ASSET-MANIFEST.json`
   - `projects/active/PRODUCTION.json`
   - Any additional dialogue, reference, sound, storyboard or continuity files in that folder.
3. Inspect the full `Skil-cc/` directory and current engine files before editing.
4. Read `references/PRODUCTION-PIPELINE.md`, `references/SCREENPLAY-FORMAT.md`, `references/3D-STYLE.md`, `references/CONTINUITY-QA.md`.
5. Treat the active project's screenplay and character/world bibles as authoritative. Preserve exact dialogue and scene intent. Do not silently rewrite story facts.

If active project source files contain only templates or placeholders, stop before inventing a film. Prepare the production structure and report exactly which source information is missing.

## Goal and scope
Create original stylized cinematic full-3D animation with a final runtime between 05:00 and 10:00. Every visible character, clothing item, hair mass, prop, environment and effect must be actual volumetric 3D. No 2D character cards, sprites or billboard characters. Use the visual quality target described in the style guide: strong composition, readable silhouettes, expressive acting, purposeful camera, consistent lighting and clean sound design. The goal is an original explainer/story film with polished pacing, not a copy of another channel's exact work.

Keep the project's established rounded mitten hands without individually modeled fingers unless the character bible explicitly overrides it.

## Runtime and frame math
- Accept requested runtime only within 300–600 seconds unless the user explicitly changes the range.
- Default timeline: 24 fps. At 24 fps, 5 minutes = 7,200 frames; 10 minutes = 14,400 frames.
- At 30 fps, 5 minutes = 9,000 frames; 10 minutes = 18,000 frames.
- Set one project-wide FPS and keep it consistent.
- Include scene durations, shot durations, transitions and audio tails in the runtime calculation.
- Validate the final sum. Never label a rough estimate as exact runtime.

## Workflow: execute in order
### 1. Source audit
Read the screenplay and every supporting source. Inventory named characters, dialogue, locations, props, time jumps, cause/effect, unresolved questions and constraints. Produce a source map with file paths and note conflicts instead of guessing.

### 2. Story breakdown
Create logline, synopsis, character goals, opposition, stakes, causal beat sheet and ending. Preserve the source's premise. Each major event needs a trigger, a consequence and a visible result. Seed clues before payoffs. Avoid arbitrary time skips and unexplained character arrivals.

### 3. Timed screenplay
Break the source into scenes and shots. Assign timecodes and duration. Keep every line of dialogue verbatim. Add action, blocking, emotional intention, sound and camera notes in separate fields. If dialogue timing is too short, adjust shot duration or ask for approval; do not speed-read dialogue.

### 4. 3D pre-production
Build character bible, model sheets, environment bible, prop list, asset manifest, material palette, rig requirements and continuity IDs. Every asset receives a stable ID. Distinguish assets already present from assets still to create.

### 5. Storyboard and animatic
Create shot-by-shot visual descriptions and camera plans. Confirm geography, eyelines, screen direction, staging and pacing. Generate a low-cost animatic before final animation.

### 6. 3D production
Use Blender as the primary production DCC unless the user specifies another compatible tool. Create real meshes, materials, UVs, rigs, animation actions, cameras, lighting, VFX and audio. Import GLB/GLTF into the browser previs tool when useful. Do not pretend the lightweight Three.js previs editor is a full renderer or automatic model generator.

### 7. Animation direction
Animate in passes: layout, key poses, blocking, body mechanics, weight shift, anticipation, contact, follow-through, overlap, facial performance, eye direction, prop interaction and polish. Avoid floating feet, sliding contact, weightless impacts, sudden snaps and mesh intersections. Align mouth animation to approved voice audio when available.

### 8. Edit and sound
Assemble scenes and shots in order. Add dialogue, ambience, Foley, designed effects, music and intentional silence. Mix for intelligibility. Keep audio and picture duration aligned.

### 9. Validation
Run:
`python Skil-cc/scripts/validate_project.py --project Skil-cc/projects/active`
Then generate a plan:
`python Skil-cc/scripts/build_plan.py --project Skil-cc/projects/active --out Skil-cc/projects/active/production-plan.json`
Review all warnings. These scripts validate structured source and timing; they do not render a film.

### 10. Final delivery
Deliver the editable 3D project, asset manifest, final screenplay/shot list, audio, render settings, final video and QA report when available. State exact runtime, FPS, frame count, resolution, codecs, render status and known limitations. Never claim files exist unless verified.

## Required deliverables
- Source audit and story beat sheet.
- Timed screenplay and shot breakdown.
- Character and environment bibles.
- 3D asset manifest.
- Storyboard/animatic.
- Rig and animation plan.
- Camera, lighting, VFX and sound cue sheets.
- Editable scene/project files.
- Final render and QA report.

## Repository navigation
- `projects/active/`: current film screenplay and production data.
- `references/`: workflow, formatting, style and QA rules.
- `scripts/`: deterministic validation and plan generation.
- `engine-v4/`: browser-based 3D previs/blocking prototype.
- `engine-v3/`: archived 2D character studio; do not use for new film production.

## Boundaries
A GitHub repository stores the screenplay and project files; it does not itself run Blender or render video. Claude Code must be opened in a local clone/workspace with this repository available. Use tools actually installed in that workspace. Ask before installing dependencies, using paid APIs or deleting source assets.
