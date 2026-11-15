# SalszATR

**AI-assisted chat translator for MoonLoader / SA-MP 0.3.7 R1**
Current version: **v1.1 (audited & patched, still NOT verified in a live game session)**

> Keep each script in its own folder. SalszATR lives in `SalszATR/`.

## 1. Purpose

- **Outgoing:** intercept normal chat, translate to the target language, send the translation.
- **Incoming:** detect `[id] Name: message` lines, translate the body to Indonesian, show it in order.
- **Provider fallback:** Gemini <-> Grok (runtime switch only; `/tr reset` returns to the configured primary).
- **Safety:** if outgoing translation fails, times out, is empty, is too long or starts with `/`, the message is **not sent** (the original is never leaked while the translator is ON).
- **Commands** (`/login`, `/report`, ...) are never translated.

## 2. Files

| File | Purpose |
|---|---|
| `SalszATR.lua` | Main script |
| `SalszATR.ini.example` | Example config (copy to `moonloader/config/SalszATR.ini`) |
| `README.md` | This document |

## 3. Dependencies

1. MoonLoader + **SAMPFUNCS** (`sampAddChatMessage`, `sampRegisterChatCommand`, `sampSendChat`)
2. `samp.events` (SAMP.Lua)
3. `mimgui` (GUI, optional)
4. `inicfg` (config)
5. `effil` + `requests` (async HTTPS; standard MoonLoader pattern)
6. `encoding` (MoonLoader built-in; UTF-8 <-> game codepage)

`effil_http` is **no longer used** (its API was unverifiable). All HTTP results are polled from `main()`, so callbacks always run on the main script thread.

## 4. Installation

1. Put `SalszATR.lua` in `moonloader/`.
2. Install the dependencies above into `moonloader/lib/`.
3. Start SA-MP, run `/str`, enter API key(s), choose language/style/provider, press **Save**.
4. Test on a quiet server with short messages first.

## 5. Commands

| Command | Action |
|---|---|
| `/str` | Toggle settings window |
| `/tr on` / `/tr off` | Enable / disable translation |
| `/tr reset` | Reset runtime provider to configured primary, clear cooldown |
| `/tr status` | Show state, provider and backend status |

## 6. Configuration

`[general]`: `enabled`, `outgoing`, `incoming`, `target` (0 English, 1 German, 2 Spanish MX, 3 Indonesian), `outStyle` (0-10), `inStyle` (0-2), `primary` (0 Gemini, 1 Grok), `codepage` (game chat codepage for the `encoding` library, default `CP1252`; use `CP1251` for Cyrillic servers).
`[keys]`: `gemini`, `grok`. `[models]`: `gemini`, `grok`.
Keys are stored in plain text in `moonloader/config/SalszATR.ini`. Never share/commit it.

## 7. Request flow

Hooks only enqueue; `main()` ticks every 50 ms: poll HTTP jobs -> start outgoing -> start/flush incoming.

- **Outgoing:** `onSendChat` -> (slash bypass) -> queue (max 3) -> translate -> validate (single line, not empty, not starting with `/`, <= 144 bytes) -> `sampSendChat` guarded by a re-entry flag.
- **Incoming:** `onServerMessage` -> match `[id] Name: text` (must contain letters, own ID skipped) -> ordered queue (max 32, 4 in flight, 20 s deadline) -> display translated line, or the original on failure/timeout. After a total failure, incoming translation backs off for 20 s.
- **Gemini:** `generateContent`, `x-goog-api-key`, `systemInstruction`; for `*2.5-flash*` thinking is disabled (`thinkingBudget=0`) so the token budget is not eaten by reasoning.
- **Grok:** `https://api.x.ai/v1/chat/completions`, Bearer key.
- **Prompt-injection hardening:** instructions are in the system role; chat text is a delimited `<msg>` data block.

## 8. v1.1 changes (audit)

Fixed:
1. **mimgui combos crashed**: Lua tables were passed to `imgui.Combo`; now `const char*[]` arrays.
2. **Untranslated leak**: stale `allowedTranslated` could let the same text through untranslated later; now one-shot with 2 s expiry.
3. **Command injection via translation**: a translation starting with `/` would run as a command; now blocked. Explicit slash bypass added.
4. **Encoding**: UTF-8/codepage conversion added (accented text was corrupted / invalid JSON).
5. **Hangs**: no timeout meant `busyOutgoing` could stay true forever; all jobs now have deadlines and watchdogs.
6. **Dropped messages** while busy -> small FIFO queue.
7. **Incoming order** could scramble; now an ordered queue. Own echoed messages are no longer re-translated.
8. **Incoming color** was RGBA passed to an ARGB function; converted.
9. **Smart-quote strip** used a byte class on multi-byte quotes (could corrupt UTF-8); replaced.
10. **Gemini 2.5 Flash** empty replies from thinking tokens; fixed (see above).
11. `grok` `max_tokens` raised (reasoning models), `ffi.copy` overflow guarded, style setup moved to `OnInitialize`.
12. Provider fallback no longer permanently overwrites the saved primary.
13. If the backend is missing, outgoing chat is blocked with a clear message (use `/tr off`) instead of silently swallowed or leaked.
14. `effil_http` removed; `effil` + `requests` used.

## 9. Still unverified (needs an in-game test)

- `effil.thread` + `requests` returning `status_code` / `text` in your MoonLoader build.
- `encoding.default = 'CP1252'` support in your build; fallback is plain pass-through.
- `sampSendChat` re-entering `onSendChat` synchronously (handled both ways).
- Chat color conversion (`rshift(color, 8)`).
- Model IDs (`gemini-2.5-flash`, `grok-4.7`) available to your account.

## 10. Manual test plan

- Loads with all dependencies; missing ones give a clear message.
- `/str` opens/closes; settings persist after restart.
- `/tr on|off|reset|status` work.
- `/login test`, `/stats` pass through untouched.
- Normal message: suppressed, translated once, sent once.
- Gemini-only, Grok-only, primary failure -> secondary.
- Both fail -> original NOT sent. Translation > 144 bytes -> blocked.
- Incoming player chat translated once and in order; system messages untouched; failure shows the original.
- Disconnect during a pending request does not crash.

Report bugs with MoonLoader/SAMP.Lua/mimgui/effil versions, provider/model and the exact error (redact keys).

## 11. Contributor rules

Read this README and the full script first. Keep files inside `SalszATR/`. Never leak untranslated outgoing text, never translate commands, never log or commit keys, do not assume library APIs, change one thing at a time, and update this README with every behavior change.

## 12. Version history

- **v1.1:** audit fixes listed above.
- **v1.0:** initial prototype.
