# Dialogue Audio, Timing, and Lip-Sync

## Source authority

- Dialogue script = exact words and speaker labels.
- Dialogue audio = actual voice, delivery, pauses, timing, and duration.
- Animation script = visual events and intended performance.

Do not create or rewrite dialogue/audio. Never replace the user's recording with generated speech. If the text and audio differ, preserve both and report the exact conflict.

## Timing pipeline

1. Inspect audio with `tools/audio_probe.py` / FFprobe.
2. Keep originals unchanged in `input/audio/`.
3. Match each clip to a speaker, scene, and line.
4. Prefer word/phoneme timestamps from an installed speech recognizer.
5. Otherwise use waveform energy, silence segmentation, phrase alignment, and manual review.
6. Convert seconds to frames using the project's actual FPS.
7. Preserve pauses, breaths, overlaps, hesitations, and natural delivery.

The script helps identify words and speakers; the recording determines when the mouth moves. Do not estimate audio duration from word count alone.

## Viseme model

Use a compact practical set:
- REST: relaxed/closed neutral.
- MBP: lips closed for M/B/P.
- FV: lower lip against upper teeth.
- A: open jaw.
- E/I: wide/front vowel.
- O/U: rounded/pursed vowel.
- L/TH: tongue/teeth shape if the model supports it.

Blend jaw opening with lip shape. A single jaw flap is not sufficient lip-sync. Add subtle cheek/brow/head performance only when it matches the script and recorded delivery.

## Automation and honesty

- If phoneme recognition is available, create timed phoneme/viseme events.
- If only word timestamps are available, map words to approximate viseme sequences and mark the result as approximate.
- If only phrase/silence alignment is available, use phrase-level mouth movement and disclose the lower precision.
- Never claim perfect sync without checking the rendered face alongside the original audio.
- Use `tools/blender/apply_visemes.py` for a prepared viseme-event JSON track on a compatible Blender mouth shape-key object.

## Audio mix

- Preserve the original dialogue stem and timing.
- Do not add music or SFX unless supplied or explicitly approved.
- Keep dialogue intelligible and avoid clipping.
- Mux audio only after picture frames are complete.
- Verify final audio duration and stream presence with FFprobe.
