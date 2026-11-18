# Skil-cc Character Engine v3

Lightweight procedural 2D character studio using vanilla HTML Canvas and ES modules. No dependencies, API keys, paid generation credits, or external assets.

## Run
From this directory:
```bash
python -m http.server 8000
```
Open `http://localhost:8000`.

## Rig System v3
- Transform controls for head tilt and torso lean.
- Independent shoulder rotation for both arms.
- Separate elbow bend controls for both arms.
- Independent thigh rotation and knee bend controls.
- Capsule-style limb segments with visible elbow and knee pivots.
- Optional automatic walk cycle with alternating arm and leg swing.
- Mitten hands remain fingerless and rounded.
- Timeline editor with adjustable duration (0.5–15 seconds).
- Add, replace and delete pose keyframes at the current playhead.
- Smooth interpolation between rig values; pose and expression switch at keyframe boundaries.
- Play, pause, stop, scrub and click saved keyframes.
- Timeline is included in character JSON export/import.
- Rig data is normalized, exported, and restored through character JSON profiles.

## Character tools
- Four presets, six expressions, five poses.
- Editable skin, hair, shirt, pants and background colors.
- PNG export and JSON profile import/export.
- Responsive controls; no external libraries.

## Reuse
Export both PNG and JSON for each character. Keep them together as a reusable character library.

## Limits
This is a lightweight procedural 2D rig and basic keyframe timeline, not a full inverse-kinematics, mesh-deformation, audio-sync, or video-rendering editor. Elbow and knee controls rotate connected capsule segments; they do not deform a hand-drawn mesh. The walk cycle is a simple looping procedural motion. Browser visual QA is still required after pulling the update. Timeline playback previews motion on the canvas; it does not export MP4/GIF.
