# Skill3D implementation references

This page records real APIs and open-source projects used to ground the Blender, lip-sync, and MP4 pipeline. These references demonstrate that the individual techniques exist; they do not prove that every Skill3D script is production-ready. The repository's Blender/FFmpeg smoke test is the executable evidence for the included starter pipeline.

## Blender modeling, rigging, and animation

- Blender Manual — Animation and rigging: https://docs.blender.org/manual/en/latest/animation/armatures/index.html
- Blender Manual — Shape Keys: https://docs.blender.org/manual/en/latest/animation/shape_keys/index.html
- Blender Manual — Drivers: https://docs.blender.org/manual/en/latest/animation/drivers/index.html
- Blender Python API: https://docs.blender.org/api/current/

Blender armatures provide skeletal animation; shape keys represent alternate mesh shapes such as mouth poses; drivers can connect controls. Skill3D uses these built-in Blender systems rather than inventing a custom 3D renderer.

## Audio-driven lip-sync

- Rhubarb Lip Sync (open source CLI): https://github.com/DanielSWolf/rhubarb-lip-sync
- Rhubarb mouth-shape and JSON output documentation: https://github.com/DanielSWolf/rhubarb-lip-sync/blob/master/README.adoc
- Example Blender integration: https://github.com/highmore9501/lip_sync_in_blender

Rhubarb analyzes recorded dialogue and emits timed mouth cues (A–H and X). Its phonetic recognizer can be useful when the dialogue language is not well covered by its language model, but recognition still needs review. Skill3D converts Rhubarb cues to its own Blender shape-key names using `tools/rhubarb_to_visemes.py`.

Caution: the older `scaredyfish/blender-rhubarb-lipsync` add-on README states that the add-on is not maintained and does not work with Blender 3.2+. Do not make this legacy add-on a required dependency. Use the Rhubarb CLI directly and keep the Blender import/apply step inside Skill3D.

## Frame rendering and MP4 assembly

- FFmpeg image sequence input (image2 demuxer): https://ffmpeg.org/ffmpeg-formats.html#image2
- FFmpeg filters: https://ffmpeg.org/ffmpeg-filters.html
- FFmpeg FAQ — encoding image sequences as video: https://ffmpeg.org/faq.html#How-do-I-encode-single-pictures-into-movies_003f

FFmpeg can read a numbered image sequence as video. Its `blackdetect` and `freezedetect` filters can flag potential black or frozen spans. These are technical heuristics, not artistic review.

## Skill3D test evidence

GitHub Actions runs:
- Compile every Python helper and test module.
- Run contract tests for the user-source lock, duration choices, visual standard, and required tools.
- Install Blender and FFmpeg on a clean Ubuntu runner.
- Generate a low-poly character and a modern ruined-street blockout.
- Apply viseme events and verify saved animation data.
- Render a short frame sequence in chunks.
- Encode a one-second MP4 with a synthetic QA audio track.
- Validate video/audio streams and run black/freeze detection.

The smoke test uses synthetic audio and a tiny Workbench render to test the mechanics quickly. It does not certify final character quality, natural motion, Indonesian phoneme accuracy, or a finished film. Those require project-specific reference review and watching/listening to the output.
