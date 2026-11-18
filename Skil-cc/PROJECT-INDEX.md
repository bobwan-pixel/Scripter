# Skil-cc Project Index

## Current production
Active film source lives in `projects/active/`. Claude must read those files before creating or changing scenes.

| File | Purpose |
|---|---|
| `projects/active/SCREENPLAY.md` | Main story and exact dialogue |
| `projects/active/CHARACTERS.md` | Character identity, appearance, voice and relationships |
| `projects/active/WORLD.md` | Locations, rules, timeline and world details |
| `projects/active/ASSET-MANIFEST.json` | 3D asset IDs, file paths and status |
| `projects/active/PRODUCTION.json` | Runtime, FPS, resolution and output settings |
| `projects/active/production-plan.json` | Generated scene/shot plan; created by build_plan.py |

## Operating sequence
1. Open the repository root in Claude Code.
2. Invoke `/skil-cc-animation`, or ask Claude to produce the next Skil-cc film.
3. Claude reads `CLAUDE.md`, `SKILL.md` and the active project source files.
4. Validate source:
   `python Skil-cc/scripts/validate_project.py --project Skil-cc/projects/active`
5. Build structured plan:
   `python Skil-cc/scripts/build_plan.py --project Skil-cc/projects/active --out Skil-cc/projects/active/production-plan.json`

## Source precedence
Explicit user instructions in the current task > active screenplay and project bibles > approved production plan > references > assistant inference. Record conflicts; do not silently choose between contradictory facts.
