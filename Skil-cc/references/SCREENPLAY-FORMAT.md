# Screenplay Source Format

Keep the complete approved script in `projects/active/SCREENPLAY.md`. Claude must read the actual file, not infer dialogue from a summary.

## Scene heading
Use one heading per scene:
```md
## SCENE 01 | 00:00-00:45 | INT. LABORATORY | NIGHT
```
Accepted timecodes: `MM:SS` or `HH:MM:SS`. Scene start/end times are required for deterministic timing validation.

## Shot heading
Use one heading per shot:
```md
### SHOT 01 | 00:00-00:12 | WIDE ESTABLISHING
```

## Action and dialogue
Write action as normal paragraphs. Write dialogue as:
```md
**HAZEL:** "Kita harus memeriksa sampel itu sekarang."
**DEMIAN:** "Apa yang sebenarnya kamu temukan?"
```
Keep parentheticals and performance direction on separate lines. Preserve the exact text.

## Source rules
- Do not rewrite or shorten dialogue without permission.
- Every scene must have a valid start and end.
- Avoid overlapping scene ranges unless explicitly intended.
- Shot ranges must sit within their parent scene.
- If the screenplay is un-timed, ask permission before assigning definitive timings; proposed estimates must be labelled as estimates.
