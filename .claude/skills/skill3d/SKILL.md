---
name: skill3d
description: Produce 3D animated videos from the user's supplied animation script, dialogue script, and dialogue audio. Automatically create 3D characters, props, environments, animate and synchronize scenes, then render MP4. Invoke with /skill3d.
---

# Skill3D entry point

Read the complete production specification at `skill3d/SKILL.md` in the repository root and follow it as the source of truth.

The user supplies the animation script, dialogue script, and dialogue audio. Do not author or rewrite those sources and do not generate replacement dialogue audio. Ask the user to choose one duration before production:
- 30–60 seconds
- 1–5 minutes
- 5–10 minutes

Then follow the full workflow for source inspection, automatic 3D character/prop/environment creation, animation, audio synchronization, quality control, and final MP4 rendering.

Do not confuse this skill with `Skil-cc/`; Skill3D is an independent skill directory.
