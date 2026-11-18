# Render, Encoding, and Quality Assurance

## Preflight
- Blender version and executable detected.
- Render engine/device available.
- Project opens in background mode.
- All linked assets resolve.
- Expected frame range is continuous.
- Disk space is sufficient.
- Dialogue clips and timeline mapping are verified.

## Preview gates
1. Low-resolution playblast for all shots.
2. Character turntable and rig deformation test.
3. Prop contact test.
4. Still from each shot and every important transition.
5. Contact sheet inspection.
6. Short full-quality render with final materials and audio sync.

## Visual QA
- All scripted shots and actions exist in order.
- Character identity, proportions, hair, outfit, and props remain consistent.
- No missing, duplicated, floating, or intersecting objects.
- No obvious foot sliding, limb snapping, broken deformation, or prop clipping.
- Camera does not pass through geometry.
- No unintended black, frozen, flickering, or missing frames.
- Lighting, exposure, and colour are coherent between cuts.
- Important faces and actions are readable at final resolution.

## Audio QA
- Every required clip is present and assigned correctly.
- No changed/reordered/cut dialogue.
- No accidental silence, clipping, distortion, or abrupt cutoff.
- Lip-sync checked against the original recording.
- Music/SFX only when user-supplied or approved.

## Technical output QA
Use `tools/validate_mp4.py` and FFprobe:
- MP4 opens and contains video and audio streams.
- Runtime is within the selected duration range, allowing only a documented small tail/intro tolerance.
- Dimensions and FPS match the project configuration.
- H.264 video and AAC audio are present unless the user selected another format.
- No zero-byte or truncated file.

Technical checks cannot prove artistic quality or lip-sync accuracy. A human visual/audio review is still required.

## Delivery report
List output paths, runtime, dimensions, FPS, scene/shot count, render engine, audio sync status (verified/approximate/not tested), technical QA, visual QA, and known limitations.
