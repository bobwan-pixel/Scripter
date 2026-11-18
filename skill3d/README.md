# Skill3D

A standalone Claude Code skill for producing complete low-poly 3D animated films with Blender. It lives at `skill3d/`, beside (not inside) `Skil-cc/`. It is generic and is not tied to OUTBREAK: NXL-019 or another film.

## The user provides the story assets

Required source inputs:
- Animation script: scenes, visual actions, blocking, and camera/action instructions.
- Dialogue script: exact spoken words and speaker labels.
- Dialogue audio: the actual recorded voice files.

Claude does **not** write, rewrite, shorten, reorder, translate, or generate these source materials or replacement dialogue audio. It builds the 3D film around them. If source files conflict, it flags the exact mismatch rather than inventing a fix.

## Duration selection

At the beginning of a new production, ask for exactly one:
- 30–60 seconds
- 1–5 minutes
- 5–10 minutes

The selected range is a runtime target, not permission to cut or speed up dialogue.

## Visual baseline

- Full 3D characters, props, and environments.
- Low-poly style, medium detail.
- Real geometry, materials, camera, lighting, rigging, and animation in Blender.
- Character identity, outfit, proportions, and props remain consistent between shots.
- World setting follows the supplied script. Modern post-apocalyptic environments are supported when requested; low-poly is a rendering style, not a fantasy setting.

## Based on the supplied reference kit

The Stickman World Short Kit V2 is the primary workflow reference. Skill3D preserves its shot-level planning, deterministic frame timing, motion/easing concepts, reusable environment/prop systems, audio timing and mixing discipline, contact sheets, resumable frame rendering, final encoding, and QA.

Its 2D stickman/illustrated character-card system is not used for final Skill3D characters. It is replaced by Blender full-3D modeling, rigging, facial controls, and viseme animation.

## Start

From the repository root in Claude Code:

```text
/skill3d
```

Claude Code entry point: `.claude/skills/skill3d/SKILL.md`

Full specification: `skill3d/SKILL.md`

## Tool requirements

For full production, install Blender and FFmpeg. Python 3 is used for project utilities; Pillow is required for contact sheets. Optional speech-recognition/phoneme tools may improve timing, but are not allowed to change the user's dialogue. Skill3D must report unavailable dependencies and must not pretend a preview is a finished film.
