# SKIL-CC — Full 3D Animation Production

Skil-cc is a repository-driven production skill for original stylized 3D animated films with a target runtime of 5–10 minutes.

## Start with Claude Code
Clone the repository and open its root:
```bash
git clone https://github.com/bobwan-pixel/Scripter.git
cd Scripter
claude
```
Invoke the project skill:
```text
/skil-cc-animation
```
Or ask: "Baca seluruh naskah dan file proyek Skil-cc, validasi durasi, lalu susun production plan 3D tanpa mengubah dialog."

Claude reads `CLAUDE.md`, `.claude/skills/skil-cc-animation/SKILL.md`, `Skil-cc/SKILL.md` and the active project source files. A GitHub URL alone is not an execution environment; Claude Code needs the repository checked out locally or exposed through a connected filesystem.

## Active film source files
- `projects/active/SCREENPLAY.md`: full story, scene/shot timing, action and exact dialogue.
- `projects/active/CHARACTERS.md`: approved character bible.
- `projects/active/WORLD.md`: world rules and locations.
- `projects/active/ASSET-MANIFEST.json`: stable 3D asset IDs and status.
- `projects/active/PRODUCTION.json`: runtime, FPS, resolution and output settings.

The screenplay and character/world bibles are templates until populated with the approved film material. Claude must not invent a replacement story or dialogue.

## Validation and plan generation
From repository root:
```bash
python Skil-cc/scripts/test_screenplay.py
python Skil-cc/scripts/validate_project.py --project Skil-cc/projects/active
python Skil-cc/scripts/build_plan.py --project Skil-cc/projects/active --out Skil-cc/projects/active/production-plan.json
```
Validation checks timed scenes/shots, runtime (300–600 seconds), overlaps, FPS metadata and JSON manifests. Plan generation reads the actual screenplay and writes structured scene, shot, action and dialogue data.

## Production target
- Full volumetric 3D characters, hair, clothes, props, environments and effects.
- Cinematic storytelling, camera, lighting, sound and continuity.
- Runtime 300–600 seconds.
- Default 24 FPS; 7,200–14,400 frames.
- Blender for final modeling, rigging, animation, VFX and rendering.
- Three.js engine-v4 for lightweight browser previs and blocking only.

## Directory map
- `SKILL.md`: main production instructions.
- `PROJECT-INDEX.md`: source file map and execution order.
- `projects/active/`: film source of truth.
- `references/`: workflow, screenplay, style and QA rules.
- `scripts/`: screenplay parser, validation, plan generation and tests.
- `engine-v4/`: 3D previs prototype.
- `engine-v3/`: archived 2D studio, retained for old projects.
