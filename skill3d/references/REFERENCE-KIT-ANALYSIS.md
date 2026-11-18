# Reference Kit Analysis

Source: user-supplied `stickman-world-short-kit-v2.zip`.

## What the kit actually contains

The archive has 16 files:
- `Skill.md`: 18 KB workflow and production instructions.
- `engine/main.js`: Three.js renderer, stylized 3D world, toon materials, normal/depth pass, outlines, depth of field, cards, frame rendering.
- `engine/paint.js`: deterministic procedural painted textures for wood, stone, moss, grass, and other surfaces.
- `engine/motion.js`: easing, camera interpolation, idle motion, blink timing, walking, and quantization helpers.
- `engine/stickman.js`: 2D cartoon character artwork drawn to transparent canvas cards.
- `engine/roman.js`: 2D illustrated Roman characters and hand-drawn props/effects.
- `tools/setup.sh`: creates a working project, copies engine and tools, provisions Three.js and Playwright.
- `tools/timing.py`: voice duration, speech segmentation, optional Whisper word timestamps, phrase-to-segment dynamic-programming alignment.
- `tools/render.mjs`: Playwright-driven deterministic frame capture.
- `tools/sheet.py`: contact-sheet generation from rendered stills.
- `tools/mix.py`: voice-relative music/SFX level matching and peak control.
- `tools/finish.sh`: final encode and freeze/black/loudness QA.
- `example/soldier/story.js`: worked shot/camera/light/world/actor/effect timeline.
- `example/soldier/audio.py`: procedural music and SFX stems for the example.

## Concepts Skill3D adopts

1. **A staged workflow**: intake → source/script lock → timing → shot plan → assets → animation → preview → audio → render → QA.
2. **Exact source timing**: audio duration and speech timing determine visual timing; the voice is not forced to fit a predetermined picture.
3. **Shot-level planning**: every shot has frame range, action, camera, lighting, characters, props, effects, and audio cue.
4. **Deterministic frame timeline**: scene state can be reproduced from frame number, allowing targeted rerenders.
5. **Reusable systems**: shared character rigs, props, materials, sets, motion helpers, and lighting presets.
6. **Visual review gates**: render stills at shot middles and transitions, make a contact sheet, inspect before full render.
7. **Resumable rendering**: render in frame ranges and resume interrupted jobs.
8. **Technical QA**: check black/frozen frames, output encoding, loudness, and file integrity.
9. **Separate source and generated material**: keep voice recordings and user scripts intact; generated assets and outputs live separately.
10. **Task visibility**: maintain a task list and tell the user what stage is active.

## Concepts Skill3D intentionally does not copy

The source kit is explicitly a hybrid **2D stickman characters + 3D cartoon environment** pipeline. Its main cast is drawn as transparent 2D canvas cards. Skill3D's requirement is full 3D characters, so it must not use:
- `stickman.js` as the final character system.
- `roman.js` as the final character system.
- Flat billboard cards as substitutes for 3D bodies.
- The source kit's fixed 1080×1920 / 30 fps defaults for every project.

The source kit's renderer is Three.js/Playwright. Skill3D uses Blender as the primary full-3D production environment. Reuse the workflow principles, not an incompatible character representation.

## Audio policy difference

The reference kit includes optional generated music/SFX and a voice-relative mix script. Skill3D does not generate or replace dialogue audio. Music and SFX are omitted unless the user supplies them or explicitly approves adding them. Original dialogue recordings remain authoritative.

## Design conclusion

Skill3D is a full-3D expansion inspired by the source kit's production discipline, not a rename or blind copy of its 2D character engine.
