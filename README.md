# Scripter — Bobwan

Repository for the author's scripts and experiments.

## Projects
- `SalszATR-CC/`: SA-MP chat translation script.
- `Skil-cc/`: separate legacy/general animation skill project. Skill3D does not depend on it.
- `skill3d/`: independent full-3D animation production skill.

## Claude Code: Skill3D

Clone and open the repository locally:
```bash
git clone https://github.com/bobwan-pixel/Scripter.git
cd Scripter
claude
```

Invoke:
```text
/skill3d
```

The user supplies the animation script, dialogue script, and dialogue audio. Skill3D creates full 3D characters, props, environments, animation, audio synchronization, previews, QA, and final MP4. It does not write or rewrite the user's source script/dialogue or generate replacement dialogue audio.

Choose one duration when prompted:
- 30–60 seconds
- 1–5 minutes
- 5–10 minutes

Read `skill3d/SKILL.md` and its `references/` and `templates/` directories for the full specification. The project bootstrap helper is:
```bash
python skill3d/tools/new_project.py "project-name" --root ./projects
```

Blender must be installed and available in Claude Code's workspace for full 3D modeling, rigging, animation, and rendering. A GitHub URL by itself does not execute Blender or expose a local filesystem.
