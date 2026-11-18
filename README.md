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


## Claude Code: Skill3D

`skill3d/` is a separate 3D animation production skill. Unlike a writing assistant, it expects the user to provide the animation script, dialogue script, and dialogue audio. Claude follows those sources, automatically creates 3D characters and props, animates and synchronizes scenes to the supplied audio, then renders an MP4.

Invoke it from Claude Code with:

```text
/skill3d
```

Full rules: `skill3d/SKILL.md`. The invocable entry point is `.claude/skills/skill3d/SKILL.md`.

This is separate from `Skil-cc/`; do not mix their instructions or project files.
