# Skil-cc Project Index

## Current production
Active film source lives in `projects/active/`. Claude must read all files in that folder before planning or editing.

| File | Purpose |
|---|---|
| `SCREENPLAY.md` | Canonical story, timed scenes/shots, action and exact dialogue |
| `CHARACTERS.md` | Character identity, appearance, voice and relationships |
| `WORLD.md` | World rules, timeline and locations |
| `ASSET-MANIFEST.json` | Stable 3D asset IDs, file paths and status |
| `PRODUCTION.json` | Runtime, FPS, resolution and output settings |
| `VOICE-AUDIO.md` | Approved voice cast, recording and sound-design notes |
| `STORYBOARD.md` | Shot composition, camera and visual planning |
| `CONTINUITY.md` | Locked story facts, character/prop/set continuity |
| `PRODUCTION-NOTES.md` | Technical decisions, blockers and render tests |
| `production-plan.json` | Generated machine-readable scene/shot plan |

## Operating sequence
1. Clone the repository and open its root in Claude Code.
2. Invoke `/skil-cc-animation`.
3. Claude reads `CLAUDE.md`, the project skill, this index and every active source file.
4. Validate source:
   `python Skil-cc/scripts/validate_project.py --project Skil-cc/projects/active`
5. Run parser tests:
   `python Skil-cc/scripts/test_screenplay.py`
6. Build structured plan:
   `python Skil-cc/scripts/build_plan.py --project Skil-cc/projects/active --out Skil-cc/projects/active/production-plan.json`

## Source precedence
Explicit user instructions in the current task > active screenplay and approved project bibles > approved production plan > references > assistant inference. Record conflicts; do not silently choose between contradictory facts.

## Dialogue authority
`SCREENPLAY.md` is the only canonical source for spoken dialogue. `VOICE-AUDIO.md` stores casting, performance and recording metadata, not a rewritten copy of the dialogue.
