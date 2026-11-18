# Character Standard: Full 3D

## Required result
A character is a complete 3D asset, not a drawing placed in a 3D scene.

## Model
- Head, torso, pelvis, arms, forearms, hands, thighs, lower legs, and feet have real volume.
- Silhouette reads clearly from front, side, and three-quarter views.
- Proportions are intentional and consistent.
- Face has modeled or layered eyes, eyelids, brows, nose, cheeks, and mouth.
- Hair is built from coherent masses/strands/clumps with a stable silhouette.
- Clothing has believable thickness and shape; avoid paper-thin surfaces.
- Hands and feet are modeled well enough for the scripted actions.

## Rig
- Deformation-friendly topology and joint placement.
- Body controls for root, pelvis, spine, chest, neck, head, shoulders, arms, wrists, fingers, legs, ankles, and feet.
- Facial controls for eye direction, blink, brows, jaw, and lip shapes.
- IK/FK where useful.
- Foot contact and hand/prop constraints for interactions.

## Performance
- Expressions must read at the final output size.
- Mouth motion must support speech and phoneme/viseme changes.
- Gestures must originate from the body, not only rotate the wrist.
- Avoid stiff shoulders, locked elbows, dead eyes, and frozen faces.
- Keep motion within the character's balance and physical ability.

## Reference matching
When a reference image is provided:
- Record visible design features separately from inferred details.
- Match broad style, proportions, palette, hair silhouette, and clothing design.
- Do not assume unseen back/side details; create coherent designs consistent with visible evidence.
- Ask only if a missing feature materially changes the result.
- Do not copy a real person's identity. Use the reference as design guidance.

## Approval checks
Before final animation, produce:
- Front/side/three-quarter turntable.
- Neutral, happy, sad, angry, surprised, and speaking face tests when relevant.
- Basic walk and hand/prop interaction tests.
