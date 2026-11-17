# Skil-cc Character Engine v3

A lightweight, browser-based 2D character preview/composer built with vanilla HTML Canvas and ES modules. No dependencies, account, API key, or generation credits required.

## Run
Open `index.html` in a modern browser. If the browser blocks ES modules on file URLs, run a local static server from this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Features
- Original human-cartoon explainer character renderer.
- Editable skin, hair, shirt, pants and background colors.
- Six facial expressions and five poses.
- Rounded mitten hands with no individual fingers.
- Subtle idle breathing and blinking.
- PNG preview export and JSON character profile export.
- Responsive interface; no external assets or paid services.

## Limits
This is a procedural 2D preview/composition engine, not a full skeletal animation editor or AI video generator. The pose and expression set can be extended in `character.js`; motion behavior is in `motion.js`. The engine is intentionally lightweight and does not modify the existing v2 ZIP archive.
