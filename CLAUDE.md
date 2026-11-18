# Repository instructions for Claude Code

This repository contains several unrelated tools. Do not assume the entire repository is one project.

## Skil-cc animation project
When a task mentions Skil-cc, animation, film, screenplay, dialogue, character assets, shots or rendering:
1. Read `Skil-cc/SKILL.md` completely.
2. Read `Skil-cc/PROJECT-INDEX.md`.
3. Read every relevant file in `Skil-cc/projects/active/` before planning or editing. In particular read `SCREENPLAY.md`, `CHARACTERS.md`, `WORLD.md`, `ASSET-MANIFEST.json` and `PRODUCTION.json` when present.
4. Read the relevant reference documents linked from `Skil-cc/SKILL.md`.
5. Use the `/skil-cc-animation` project skill when available.
6. Never invent dialogue, character facts, locations, props or story events that contradict source files. Ask only when a missing fact blocks production.
7. Treat the screenplay in the active project folder as the source of truth. Preserve dialogue verbatim unless asked to revise it.
8. Build the complete production plan before modifying 3D assets. Validate duration and continuity with the supplied scripts.
9. Keep all deliverables under `Skil-cc/projects/active/` or the engine directory. Do not modify `SalszATR-CC/` or unrelated projects.

## Execution rules
- Inspect existing files before overwriting.
- Prefer deterministic scripts and explicit manifests.
- Do not claim a render, rig, simulation or export succeeded unless it was actually run and checked.
- If an external 3D application or renderer is unavailable, prepare its project files and clearly report the remaining manual step.
