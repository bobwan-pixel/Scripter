# Skil-cc Character Engine v3

A lightweight browser-based 2D character preview/composer built with vanilla HTML Canvas and ES modules. No dependencies, account, API key, or generation credits required.

## Run
Open `index.html` in a modern browser. If the browser blocks ES modules on file URLs, run a local static server from this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Features
- Original human-cartoon explainer character renderer.
- Editable skin, hair, shirt, pants and background colors.
- Four reusable starting presets: Bobwan Casual, Narrator, Student and Worker.
- Six facial expressions and five poses.
- Rounded mitten hands with no individual fingers.
- Subtle idle breathing and blinking with one shared animation loop.
- Export character preview as PNG.
- Export and import reusable character profiles as JSON.
- Imported profiles are validated before being applied.
- Responsive interface; no external assets or paid services.

## Reuse workflow
1. Choose a preset and customize the character.
2. Export the PNG for visual reference.
3. Export the JSON profile to preserve colors, pose, expression and character name.
4. In a later session, import that JSON to restore the same profile and continue editing.

Keep each character's JSON profile alongside its reference PNG. This creates a small reusable character library without spending AI generation credits.

## Limits
This is a procedural 2D preview/composition engine, not a full skeletal animation editor or AI video generator. The current pose set is drawn from fixed shapes rather than a deformable bone rig. The engine is intentionally lightweight and does not modify the existing v2 ZIP archive.
