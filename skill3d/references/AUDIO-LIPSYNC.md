# Dialogue Audio and Lip-Sync

## Authority
The supplied dialogue audio is the timing authority. The supplied dialogue script is the wording and speaker reference. Neither is rewritten by Skill3D.

## Mapping
Create a mapping of:
- Audio file.
- Speaker.
- Scene/shot.
- Dialogue line or range.
- Start and end time.
- Confidence/notes.

If a clip cannot be mapped unambiguously, ask the user.

## Alignment
1. Read audio metadata.
2. Measure exact duration.
3. Run speech-to-text timestamps if available, using the user's script as the transcript reference.
4. Otherwise detect speech segments and align script phrases to segments.
5. Review ambiguous boundaries manually.
6. Convert timecodes to frame numbers using project FPS.

## Visemes
Use a practical viseme set, for example:
- Rest/closed.
- MBP (closed lips).
- FV (teeth on lower lip).
- Wide vowels.
- Open vowels.
- Rounded vowels.
- Tongue/teeth shapes where the rig supports them.

Map phoneme intervals to mouth controls. Add jaw motion and subtle cheek/brow motion. Do not animate lips only by opening and closing the jaw.

## Timing rules
- Preserve silence and pauses.
- Keep breaths and natural delivery.
- Do not time-stretch or cut dialogue.
- Do not move a line to another character.
- Listening characters should not visibly mouth the active speaker's words.
- Check sync by watching rendered frames while listening to the original audio.

## Missing tools
If phoneme extraction or automatic lip-sync is unavailable, use script/audio timestamps to build a best-effort viseme track and disclose that it is approximate. Never label approximate sync as perfect.
