# Reference Kit Analysis

Primary reference: user-supplied `stickman-world-short-kit-v2.zip` (16 files).

## Archive inventory

- `Skill.md`: full production workflow and operating rules.
- `engine/main.js`: Three.js scene renderer, world setup, materials, camera/render pipeline, post-processing, deterministic frame rendering.
- `engine/paint.js`: procedural painted surface/material helpers.
- `engine/motion.js`: easing, camera interpolation, idle motion, blinking, walking, and motion helpers.
- `engine/stickman.js`: 2D stickman character drawing on transparent canvas.
- `engine/roman.js`: 2D illustrated character/prop/effect drawing.
- `tools/setup.sh`: project setup and dependency provisioning.
- `tools/timing.py`: audio duration, speech segmentation, optional Whisper timestamps, and phrase-to-speech alignment.
- `tools/render.mjs`: deterministic browser-driven frame capture.
- `tools/sheet.py`: rendered-frame contact sheet.
- `tools/mix.py`: voice-relative music/SFX level matching and peak control.
- `tools/finish.sh`: encode and technical QA.
- `example/soldier/story.js`: worked example of shots, camera, lighting, world, actors, and effects.
- `example/soldier/audio.py`: procedural example music/SFX stems.

## Keep and improve

1. Staged workflow with explicit gates.
2. Script and source preservation.
3. Audio-first timing and exact duration measurement.
4. Shot table with frame ranges, staging, camera, light, actors, props, and audio cues.
5. Deterministic frame/time evaluation for reproducible rerenders.
6. Reusable characters, motion, materials, props, environments, and lighting.
7. Procedural environment/material generation where appropriate.
8. Preview renders, shot contact sheets, and review before full-quality output.
9. Rendering in ranges with resume/checkpoint behavior.
10. Separate dialogue, optional music/SFX, frame rendering, final mux, and QA.
11. A worked example and project setup tools.
12. Clear reporting of failures and incomplete stages.

## Replace, do not copy

The original kit is a hybrid 3D environment plus 2D drawn character-card pipeline. Skill3D is full 3D:
- Do not use `stickman.js` or `roman.js` as the final character renderer.
- Do not use flat billboards or 2D sprites in place of 3D character models.
- Replace the Three.js/Playwright final character path with Blender geometry, armatures, facial controls, animation, and Blender rendering.
- Preserve useful camera, motion, deterministic timeline, contact-sheet, timing, and QA concepts.
- Keep Three.js only as an optional separate previs tool if it provides value; it is not the final renderer.

## Skill3D-specific additions

- Full-body low-poly medium-detail character modeling and reusable rigs.
- Character identity sheets, turntables, expressions, and outfit continuity.
- Props with correct pivots, articulated parts, and interaction states.
- Modular full-3D environments.
- Facial shape keys/controls and audio-driven viseme tracks.
- Blender batch rendering, frame-range resume, and render logs.
- Technical validation of MP4 plus human inspection of visual quality and lip-sync.

## Source audio rule

The reference kit can generate example audio/music. Skill3D does not generate or replace dialogue. The user's dialogue audio and script are locked inputs. Music/SFX are not added unless supplied or explicitly approved.
