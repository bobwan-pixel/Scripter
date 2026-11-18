# Skill3D

Skill3D is an independent full-3D animation production skill for Claude Code. It lives beside `Skil-cc/` and does not depend on NXL-019 or any other film-specific project.

## Core contract

The user supplies:
- Animation script.
- Dialogue script.
- Dialogue audio.

Claude does not write or rewrite those sources and does not generate replacement dialogue audio. Claude builds the 3D production around them: characters, rigs, props, environments, shot layouts, animation, lip-sync, lighting, rendering, and QA.

## Duration choices

At the beginning of a new production, Claude asks for one target:
- 30–60 seconds
- 1–5 minutes
- 5–10 minutes

## Visual standard

Full 3D characters with volume, anatomy, expressive faces, designed hair, clothing, rigs, and facial controls. Full 3D props and environments. The supplied Stickman World Short Kit V2 is the production-workflow reference, not the final character-rendering method: its shot planning, deterministic frame timing, motion principles, contact sheets, audio handling, render resumption, and QA are useful; its 2D character cards are not used as Skill3D's final character system.

## Invoke

From the repository root:
```text
/skill3d
```

Claude Code entry point: `.claude/skills/skill3d/SKILL.md`

Full production rules: `skill3d/SKILL.md`

Read the references and templates before beginning a project. Blender must be installed for full 3D modeling, rigging, animation, and rendering.
