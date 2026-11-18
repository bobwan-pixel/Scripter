# Skil-cc Engine V4 — Full 3D Previsualization

Three.js browser-based 3D previs/blocking prototype. It is one component of the repository-driven 5–10 minute film pipeline.

## Run
From repository root:
```bash
python -m http.server 8000
```
Open `http://localhost:8000/Skil-cc/engine-v4/`.

## Current features
- Real 3D viewport, orbit camera, lights and shadows.
- Procedural stylized 3D character placeholder with modeled volumes and rounded mitten hands.
- Environment presets for studio, village, city and room.
- GLB/GLTF model import.
- 10-minute transform-keyframe timeline and playback.
- Project JSON import/export and PNG viewport capture.

## Production limits
This is previs/blocking, not a full DCC. It does not yet provide production skeletal rigging, IK, detailed facial/lip-sync animation, physically simulated VFX, audio timeline, nonlinear editing or final MP4 rendering. Use Blender for final meshes, rigging, animation, VFX, lighting and rendering. Never claim the browser prototype rendered a finished film.
