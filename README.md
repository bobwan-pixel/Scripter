# Scripter — Bobwan

Repository for the author's scripts and experiments.

## Projects
- `SalszATR-CC/`: SA-MP chat translation script.
- `Skil-cc/`: repository-driven full-3D animation production skill for 5–10 minute films.

## Claude Code: Skil-cc
Clone and open the repository locally:
```bash
git clone https://github.com/bobwan-pixel/Scripter.git
cd Scripter
claude
```
Then invoke:
```text
/skil-cc-animation
```

Project instructions are in `CLAUDE.md`; the invocable skill is `.claude/skills/skil-cc-animation/SKILL.md`. Claude should read the actual screenplay, dialogue and production files under `Skil-cc/projects/active/` before creating a production plan. See `Skil-cc/README.md`.

A GitHub URL by itself does not execute scripts or expose a local Blender workspace. Claude Code needs the repository checked out in its workspace, or a connected filesystem/tool that exposes those files.
