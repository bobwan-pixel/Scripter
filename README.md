# Scripter — Bobwan

Repository for the author's scripts and experiments.

## Projects
- `SalszATR-CC/`: SA-MP chat translation script.
- `Skil-cc/`: repository-driven full-3D animation production skill for 5–10 minute films.

## Claude Code: Skil-cc
Open the local repository root in Claude Code. Project instructions are in `CLAUDE.md`, and the invocable skill is `.claude/skills/skil-cc-animation/SKILL.md`.

Invoke:
```text
/skil-cc-animation
```

Claude should read the actual screenplay, dialogue and production files under `Skil-cc/projects/active/` before creating a production plan. See `Skil-cc/README.md`.

A GitHub URL by itself does not execute scripts or expose a local Blender workspace. Clone the repository or connect a filesystem/tool that makes its files available to Claude Code.
