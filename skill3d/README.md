# Skill3D

Standalone Claude Code skill for producing polished 3D animation from user-provided source materials.

## What the user provides

1. Animation script (scene and visual directions).
2. Dialogue script.
3. Dialogue audio files.

Skill3D does **not** author or rewrite these materials and does **not** generate replacement dialogue audio. It follows the supplied sources and synchronizes character performance and animation to the supplied audio.

## Duration choices

At the start of production Claude asks the user to choose one:
- 30–60 seconds
- 1–5 minutes
- 5–10 minutes

## What Claude produces

- Automatically created 3D characters, props, and environments.
- Animated scenes and shots following the animation script.
- Character performance and lip-sync aligned to supplied dialogue audio.
- Final MP4.
- Editable Blender project and reproducible production assets/scripts.

## Run

From the repository root, start Claude Code and invoke:

```text
/skill3d
```

The invocable entry point is `.claude/skills/skill3d/SKILL.md`. Full production rules live in this directory's `SKILL.md`.

## Important

Blender must be installed and available to Claude Code for local 3D modeling, animation, and rendering. Skill3D must report missing tools or incomplete outputs honestly; it must not claim a film is complete until a final MP4 has been rendered and checked.
