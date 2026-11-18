# Skil-cc V4 — Full 3D Animation Production

V4 changes the project from a 2D character preview tool into a full-3D animation production workflow.

## What's new
- Characters, clothing, hair, props, locations and effects are intended to be volumetric 3D.
- Story workflow is built around cause/effect, character motivation, escalation, climax and resolution.
- Production is organized as film → scenes → shots → animation clips.
- Default target is a complete 10-minute film with frame-accurate runtime planning.
- Includes a lightweight Three.js 3D previs/blocking studio in engine-v4.
- Previous engine-v3 is preserved as a legacy 2D studio.

## Files
- Skill.md: production workflow and quality gates.
- STYLE-GUIDE.md: 3D art direction and continuity.
- PROMPT-TEMPLATES.md: model, rig, environment, prop, shot, animation and VFX briefs.
- engine-v4/: browser 3D previs tool.
- engine-v3/: legacy 2D character studio, retained for old projects.

## Start
From the repository root run: python -m http.server 8000
Open http://localhost:8000/Skil-cc/engine-v4/

## Important
The browser studio is for 3D layout, rough blocking, basic character keyframes, GLB import and project JSON. It is not a complete Blender replacement and does not render a final 10-minute MP4. Use Blender for production modeling, rigging, animation, lighting and final rendering.

The supplied Stickman World Short Kit V2 is used for shot planning, easing, camera motion and production discipline. Its 2D character-card implementation is deliberately not used in V4.
