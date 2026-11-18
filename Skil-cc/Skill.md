---
name: skil-cc-full-3d-animation-production
version: 4.0.0
description: Original full-3D animated stories with consistent characters, environments, props, cinematic cameras, effects, sound and a 10-minute production timeline.
---

# SKIL-CC V4 — Full 3D Animation Production Engine

## Mission and visual standard
Create original animated stories where every visible character, item of clothing, hairstyle, prop, location and effect is volumetric 3D geometry. No 2D character cards, sprites or billboard characters. Target a polished stylized 3D cartoon film look: appealing proportions, readable silhouettes, expressive faces, controlled PBR materials and cinematic lighting. Keep the project's preference for simple rounded mitten hands without separated fingers. Never copy another creator's exact characters, shots, dialogue or assets.

The default target is a complete 10:00 film, not one ten-minute clip. Organize it as film → scenes → shots → animation clips.

## Production roles
1. Story Director: premise, cause/effect, motivation, stakes, escalation, climax and resolution.
2. Character Director: character bible, 3D model brief, wardrobe, expressions, rig and continuity.
3. World Builder: locations, architecture, terrain, props, scale and reusable sets.
4. Animation Director: blocking, body mechanics, anticipation, follow-through, weight, contact, facial acting and lip sync.
5. Cinematographer: shot sizes, lens, composition, camera path, focus and transitions.
6. Lighting & VFX Director: motivated lighting, atmosphere, particles, weather and impact effects.
7. Sound Director: dialogue, ambience, Foley, music, silence and timed cues.
8. Editor & Continuity Supervisor: shot order, rhythm, screen direction, asset continuity and runtime.
9. Technical Director: project structure, formats, rig validation, render settings and QA.

## Stage 1 — Story development
Before assets, define premise, protagonist goal, obstacle, stakes, flaw, opposing force and world rules. Build a causal chain: every major event needs a believable trigger and consequence. Plant clues and objects before payoff. Give major characters an arc or clear dramatic function. The ending must follow from the climax.

Flexible 10-minute pacing:
- 00:00–00:45 opening image and hook.
- 00:45–02:00 world, protagonist and goal.
- 02:00–04:00 inciting incident and first attempts.
- 04:00–06:30 escalation, complications and cost.
- 06:30–08:30 crisis, decision and climax.
- 08:30–09:30 consequence and resolution.
- 09:30–10:00 final image or sting.
These are targets, not rigid laws. Final runtime must match the requested duration.

## Stage 2 — Character bible and 3D models
For each character define stable ID/name, age range and role, personality/desire/fear, relationships, height and proportions, face/eyes/brows/nose/mouth, skin material, modeled hair silhouette, outfit layers/materials/colours, shoes/accessories, front/side/back/three-quarter references, expressions, voice profile and rig requirements.

Lock identity before animation. Changes between shots may include pose, expression, lighting or camera, not model identity or costume without a story reason.

3D asset requirements:
- Real meshes, not flat images. Prefer Blender source files and GLB delivery assets.
- Clean topology, object names, origins, applied transforms and consistent scale.
- Character meshes need a usable skeleton. Facial animation needs bones, shape keys or a documented control method.
- Props need real dimensions, origins and contact points.
- Validate normals, UVs, material links, textures and rig deformation.

## Stage 3 — World and set design
For each location define dimensions, scale reference, paths, architecture, terrain, foreground/midground/background geometry, hero props, time of day, weather, motivated light sources, entrances/exits, blocking zones and continuity notes. Never add props only to fill space.

## Stage 4 — Shot list and storyboard
Every shot includes scene/shot ID, start time, duration, frame range, dramatic purpose, location, characters, action, dialogue, prop interaction, camera size/lens/position/movement, lighting, VFX, audio cues, transition and continuity notes. Use wide shots to establish geography, medium shots for interaction, close-ups for emotion and inserts for story-critical details. Preserve screen direction and eyelines.

## Stage 5 — Animation
Work in passes: layout/staging; key poses/timing; blocking; body mechanics/weight; facial acting/eye direction; contact/prop interaction/foot planting; anticipation/follow-through/overlap; secondary motion/polish. Characters look before reaching, shift weight before heavy movement, make contact before objects react, and recover after impacts. Avoid floating feet, sliding hands, intersecting props, sudden snaps and unmotivated loops. Blend reusable clips such as idle, walk, run, turn, sit, reach, grab and react. Align lip sync to final audio.

## Stage 6 — Camera
Specify lens/FOV, camera height/distance/angle, framing, focus target, movement path, speed, easing, settle and cut point. Camera motion must reveal information or support emotion. Avoid geometry clipping, abrupt zooms and unreadable moves.

## Stage 7 — Lighting and VFX
Use motivated key/fill/rim and practical sources. Preserve direction/exposure between adjacent shots. Effects obey scene physics: dust follows impacts, smoke rises and disperses, rain interacts with surfaces, sparks originate at contact, debris carries momentum. Keep faces and important action visible.

## Stage 8 — Audio
Create timed cues for dialogue, room tone, ambience, Foley, designed effects, music and intentional silence. Final approved voice recording is the timing master. Adjust shot timing to performance, not the reverse.

## Stage 9 — 10-minute edit and render
Build scenes → shots → clips. At 24 fps, 10:00 = 14,400 frames; at 30 fps = 18,000 frames. Track transitions and audio tails without extending runtime. Render playblasts, low-resolution lighting tests, then final frames. Render image sequences for crash recovery; assemble MP4 with approved frame rate and audio. Keep versioned project files, asset manifest, render settings and backups.

## Required deliverables
Logline/synopsis/cause-effect outline; character bible and 3D asset list; location and prop list; timed screenplay; scene breakdown and shot list; storyboard/animatic plan; rig/animation plan; camera, lighting, VFX and audio cue sheets; continuity checklist; render/export specification; QA report with passed checks and known limits.

## Quality gates
Story causality is clear; models/costumes remain consistent; every visible character, environment, prop and effect is volumetric 3D; rigs deform cleanly; contact and weight read; cameras avoid geometry; lighting and screen direction are continuous; dialogue/audio are timed; no missing textures, broken links or black frames; runtime/frame count match; audio is present and unclipped.

## Engine boundaries
The included engine-v4 is a lightweight browser-based 3D previs/blocking tool. It creates procedural 3D cartoon placeholders, supports GLB import, camera orbit, basic character transform keyframes on a 10-minute timeline and project JSON export. It is not a replacement for Blender, professional rigging or a full offline renderer. Use Blender for final mesh authoring, UVs, rigging, detailed animation, lighting and rendering. JSON export or a preview image is not a finished MP4.

## Resource rules
Prefer free/open tools and formats. Keep preview models low-to-mid poly, use LODs/instancing and render tests before full quality. A ten-minute 3D film can be demanding on low-end hardware; never promise render speed without testing. State which generated assets still need cleanup, retopology, rigging or manual animation. Never invent platform capabilities.

## Reference policy
The supplied Stickman World Short Kit V2 is a reference for production discipline, camera movement, shot planning, easing, audio cue timing and render QA. Its own README/Skill.md describe 2D character cards in a 3D world. CC V4 deliberately changes that: characters, world, props and effects must all be 3D. Do not inherit its prohibition on 3D characters or its flat character-card implementation.
