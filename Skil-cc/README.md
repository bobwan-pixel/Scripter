# SKIL-CC — Full 3D Animation Production

Skil-cc is a repository-driven production skill for original 3D animated films with a target runtime of 5–10 minutes.

## Claude Code integration
- Repository root `CLAUDE.md` points Claude to the project.
- `.claude/skills/skil-cc-animation/SKILL.md` exposes the `/skil-cc-animation` skill.
- `Skil-cc/SKILL.md` contains the full production workflow.
- `Skil-cc/projects/active/` stores screenplay, dialogue, characters, world rules and asset manifest.
- `Skil-cc/scripts/` validates source and generates a timed production-plan JSON.

## Start with Claude Code
Clone this repository, open the local repository root in Claude Code, then invoke:
```text
/skil-cc-animation
```
Or ask: "Baca seluruh naskah dan file proyek Skil-cc, validasi durasi, lalu susun production plan 3D tanpa mengubah dialog."

A GitHub URL alone is not an execution environment. Claude Code needs the repository checked out in its workspace (or a connected filesystem/tool that exposes the files).

## Production target
- 3D characters, hair, clothes, props, environments and effects.
- Cinematic storytelling, camera, lighting, sound and continuity.
- 5–10 minute final runtime.
- Default 24 FPS; 7,200–14,400 frames.
- Blender for final modeling, rigging, animation and rendering.
- Three.js engine-v4 for lightweight browser previs and blocking only.

## Directory map
- `SKILL.md`: main production instructions.
- `PROJECT-INDEX.md`: source file map and execution order.
- `projects/active/`: film source of truth.
- `references/`: production documentation.
- `scripts/`: deterministic project utilities.
- `engine-v4/`: 3D previs prototype.
- `engine-v3/`: archived 2D studio, retained for old files.
