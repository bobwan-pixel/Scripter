# Skill3D Production Pipeline

## Gate 0 — Intake
- Detect already supplied source files before asking for anything.
- Ask the duration choice: 30–60 seconds, 1–5 minutes, or 5–10 minutes.
- Identify animation script, dialogue script, dialogue audio, and visual references.
- Ask only for missing required items.
- Detect Blender, FFmpeg, Python, disk, RAM, and render device.

## Gate 1 — Lock source
- Copy or reference originals without modifying them.
- Create source manifest and audio metadata report.
- Confirm speaker/clip mapping.
- Record contradictions and missing information; do not invent story facts.

## Gate 2 — Breakdown
- Scene breakdown in supplied order.
- Shot list with time/frame ranges, camera, blocking, action, expressions, props, lighting, and audio.
- Asset manifest for characters, outfits, props, sets, and effects.
- Continuity sheet for identity, wardrobe, prop state, screen direction, and location geography.

## Gate 3 — Previs
- Build proxy 3D geometry and simple rigs.
- Block camera, screen direction, entrances/exits, and action.
- Render low-cost playblast and contact sheet.
- Confirm every scripted beat is represented and no new story event was invented.

## Gate 4 — Asset creation
- Model full 3D low-poly medium-detail characters.
- Build reusable armatures and facial controls.
- Model props with pivots and moving parts.
- Build modular environments and reusable materials.
- Create turntables and interaction tests.
- Replace proxies before final render.

## Gate 5 — Performance and sync
- Animate blocking, body mechanics, facial expression, and prop interactions.
- Align mouth shapes to supplied audio.
- Check speaker assignment, pauses, breaths, and timing.
- Verify contact, balance, foot planting, and camera eyelines.

## Gate 6 — Preview approval
- Render key stills, transitions, contact sheet, and short full-quality sample.
- Inspect identity, staging, action readability, lighting, clipping, lip-sync, and sound.
- Resolve material defects before final render.

## Gate 7 — Final render
- Render Blender frames in manageable chunks.
- Record frame ranges and logs.
- Resume only missing/failed frames.
- Do not mux until expected frames exist.
- Keep a high-quality intermediate/master when storage permits.

## Gate 8 — Encode and QA
- Encode MP4 H.264 + AAC with FFmpeg.
- Check container, codecs, dimensions, FPS, duration, audio stream, black/frozen frames, and playback.
- Inspect the final contact sheet and sample playback with audio.
- Report any failed or approximate checks.

## Gate 9 — Deliver
- MP4, editable .blend, source project/scripts, assets, audio map, shot list, and QA report.
- Report actual runtime, resolution, FPS, render engine, and known limitations.
