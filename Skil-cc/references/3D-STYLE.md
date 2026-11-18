# Full 3D Asset and Animation Standards

## Character assets
Use volumetric meshes for head, torso, limbs, hair, clothing and accessories. Keep proportions and materials stable. A character asset must include ID, model path, rig path, texture/material references, scale and status.

## Rig and animation
Use named bones/controls, root motion, foot contact, prop contact and facial controls where available. Test neutral, walk, run, turn, reach, grab, sit, talk and emotional poses. Document unsupported controls instead of claiming they exist.

## Environment
Use real 3D geometry for locations, architecture, terrain and story props. Use consistent dimensions and named collections. Provide collision/blocking notes where relevant.

## Camera
Record focal length or FOV, camera transform, focus target, framing, movement and easing. Maintain continuity between adjacent shots.

## Export
Prefer Blender source files and GLB/GLTF for interchange. Verify texture links, normals, scale, animation tracks and material assignment after export.
