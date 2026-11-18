# Blender Production Pipeline

## Blender is the final 3D authority

Blender handles full 3D modeling, materials, UVs, lighting, cameras, scene assembly, armatures, facial shape keys, animation, constraints, preview/final rendering, and editable .blend files.

Three.js/Playwright from the reference kit may be used for optional previs, but never as a substitute for the full-3D final character pipeline.

## Included tools

- tools/blender_preflight.py: checks Blender, FFmpeg, FFprobe, and a background Blender invocation.
- tools/blender/build_lowpoly_character.py: procedural full-body low-poly starter with a basic armature and viseme mouth shape keys. Refine design/topology/rig before final use.
- tools/blender/build_modern_ruins_blockout.py: generic modern damaged-street blockout. Adapt to the supplied script; it is not a finished set.
- tools/blender/apply_visemes.py: applies time-coded viseme events to compatible mouth shape keys.
- tools/render_range.py: renders frame ranges in chunks and skips existing frames.
- tools/encode_mp4.py: encodes numbered frames and muxes supplied audio; refuses to silently truncate audio longer than the picture.
- tools/video_qa.py: checks streams and reports possible black/frozen spans.

## Character procedure

1. Derive a character sheet from the supplied script and references.
2. Use the starter generator only as a base if it fits the design.
3. Refine face, hair, silhouette, clothing, palette, topology, and accessories.
4. Ensure parts are rigged to perform the scripted actions.
5. Add/refine IK/FK, hand/foot controls, facial controls, and shape keys.
6. Run turntable, expression sheet, and deformation tests.
7. Save reusable asset files and link/append them into shot scenes.

Never call a starter generator output a finished character without these checks.

## Render procedure

1. Save a preview .blend with low resolution and samples.
2. Render a low-resolution playblast for all shots.
3. Render selected stills and contact sheets.
4. Fix composition, geometry, rig, and animation issues.
5. Render final frames with tools/render_range.py in manageable chunks.
6. Confirm every expected frame exists.
7. Encode with tools/encode_mp4.py using the exact supplied dialogue audio.
8. Run tools/video_qa.py and tools/validate_mp4.py.
9. Watch/listen to the result. Automated checks do not prove visual quality or lip-sync.
