# SalszATR

**AI-assisted chat translator for MoonLoader / SA-MP 0.3.7 R1**  
Current package version: **v1.0 (prototype, not yet verified in a live game session)**

> This repository is a library of scripts being developed. Keep each script in its own folder. SalszATR lives at `SalszATR/`; do not place its files in the repository root.

## 1. Purpose

SalszATR is intended to translate SA-MP player chat in both directions:

- **Outgoing:** intercept a player's normal chat message, translate it to the configured target language, then send the translated text.
- **Incoming:** detect common player-chat lines, translate the message body into Indonesian, and display the translated line.
- **Provider fallback:** try the active provider (Gemini or Grok), then try the other provider if the first request fails.
- **Safety rule:** if outgoing translation fails, the original outgoing message must remain blocked. The script must never silently send the untranslated original.
- **Command safety:** slash commands such as `/login`, `/report`, `/stats` must not be translated.

The intended use is ordinary player communication and roleplay chat. The script does not modify server data or bypass server permissions.

## 2. Current files

| File | Purpose |
|---|---|
| `SalszATR.lua` | Main MoonLoader script: event hooks, translation prompts, provider requests, fallback, commands and GUI. |
| `SalszATR.ini.example` | Example local configuration. Copy/rename it to `SalszATR.ini`; never commit real API keys. |
| `README.md` | This technical handoff and maintenance document. |

Runtime configuration is stored locally at `moonloader/config/SalszATR.ini` when `inicfg` is available. The example INI contains blank API-key fields only.

## 3. Runtime dependencies

The script expects the following libraries in the MoonLoader Lua library path:

1. `samp.events` from SAMP.Lua.
2. `mimgui` for the settings window.
3. `inicfg` for persistent settings.
4. `effil_http` for asynchronous HTTP requests.
5. `effil` and its compatible native dependencies.
6. MoonLoader JSON helpers `encodeJson` and `decodeJson`.

Useful upstream projects:

- SAMP.Lua: https://github.com/THE-FYP/SAMP.Lua
- effil-http: https://github.com/t9foon1337/effil-http
- MoonLoader: https://github.com/BlastHackNet/moonloader

**Important:** `effil_http` is not bundled. Its native dependencies and LuaJIT compatibility must match the user's GTA San Andreas / MoonLoader installation. A library being present does not prove that its API or worker setup is compatible.

## 4. Installation

1. Install MoonLoader for the target GTA San Andreas installation.
2. Install the dependencies listed above.
3. Copy `SalszATR.lua` into `GTA San Andreas/moonloader/`.
4. Start SA-MP and allow the script to initialize.
5. Open the interface with `/str`.
6. Enter Gemini and/or Grok API keys in the GUI, select language/style/provider, and save.
7. Test on a quiet server with short, non-sensitive messages before relying on it.

If the script creates its configuration automatically, it should be under `moonloader/config/SalszATR.ini`. Otherwise copy `SalszATR.ini.example` there and rename it to `SalszATR.ini`.

## 5. Commands

| Command | Intended/current action |
|---|---|
| `/str` | Toggle the SalszATR settings window. |
| `/tr on` | Enable translation globally. |
| `/tr off` | Disable translation globally. |
| `/tr reset` | Reset the runtime active provider to the configured primary provider. |
| `/tr status` | Show enabled state and active provider. |

The GUI exposes master enable, outgoing/incoming toggles, target language, outgoing style, incoming Indonesian style, primary provider, API keys, counters and last error.

## 6. Configuration reference

### `[general]`

- `enabled`: master switch.
- `outgoing`: translate normal messages typed by the local player.
- `incoming`: translate detected incoming player chat.
- `target`: outgoing target language index:
  - `0` English
  - `1` German
  - `2` Spanish (Mexico)
  - `3` Indonesian
- `outStyle`: outgoing style index:
  - `0` American slang
  - `1` Mexican slang
  - `2` British slang
  - `3` English soft
  - `4` Casual
  - `5` Street
  - `6` Drunk mode
  - `7` Toxic
  - `8` Professional
  - `9` Gamer
  - `10` Romantic
- `inStyle`: incoming Indonesian style index:
  - `0` Indonesia gaul
  - `1` Indonesia natural
  - `2` Indonesia formal
- `primary`: `0` Gemini first, `1` Grok first.

### `[keys]`

- `gemini`: Google Gemini API key.
- `grok`: xAI API key.

### `[models]`

- `gemini`: Gemini model identifier.
- `grok`: xAI model identifier.

Model identifiers are configuration values, not guarantees that the provider currently offers that model to a given account. Check the provider's current model catalogue if the API returns a model-not-found or access error.

## 7. Architecture and request flow

### Outgoing flow

1. `samp.events.onSendChat(message)` receives the player's chat text.
2. `handleOutgoing` checks the global and outgoing switches.
3. A message currently recognized as a slash command should bypass translation. **This behavior is part of the intended contract and must be verified/fixed in the implementation; do not assume it is fully covered by this prototype.**
4. The script marks the outgoing pipeline busy and returns `false` to suppress the original message.
5. `translateWithFallback` builds a prompt and calls the active provider.
6. If the primary request fails, the other provider is tried.
7. If a translation is returned, `sendTranslated` sends it through `sampSendChat`.
8. If both providers fail, the script reports the error and leaves the original message unsent.

The game chat limit is treated as 144 bytes by the current implementation. The script rejects a translated result above that limit rather than truncating it and potentially corrupting Unicode.

### Incoming flow

1. `samp.events.onServerMessage(color, text)` receives a server message.
2. `handleIncoming` currently looks for the common pattern `[playerId] PlayerName: message`.
3. It extracts the prefix and message body, then requests an Indonesian translation.
4. On success, it displays the preserved prefix plus translated body.
5. On failure, it is intended to display the original line.

Incoming chat formats differ between servers and custom chat systems. Never broaden the matcher casually: translating server notices, command feedback, advertisements or system messages creates noise. Add explicit format tests before supporting another pattern.

### Provider request flow

**Gemini**
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- Authentication: `x-goog-api-key` header.
- Request body: Gemini `contents[].parts[].text` structure.
- Response parsing: `candidates[1].content.parts[].text`.

**Grok / xAI**
- Endpoint: `https://api.x.ai/v1/chat/completions`
- Authentication: `Authorization: Bearer {key}`.
- Request body: OpenAI-compatible `model`, `messages`, `temperature`, `max_tokens`.
- Response parsing: `choices[1].message.content`.

### Automatic fallback

The configured primary provider is attempted first. Any request failure currently triggers the secondary provider, including network errors, HTTP errors, parsing failures and empty responses. If the secondary succeeds, it becomes the runtime active provider and is saved as the new primary preference.

A future implementation should classify errors more carefully:
- Retry/fallback: rate limit / quota, timeout, connection failure, 5xx, malformed or empty response.
- Usually do not retry blindly: invalid API key, permission denied, unsupported model, malformed request.
- Preserve the original error from both providers for diagnosis.
- Add a short cooldown/backoff to avoid hammering a provider that has just rate-limited the client.

## 8. Current implementation status and known risks

This v1.0 package is a **prototype**. It has not been confirmed through a live SA-MP session. The presence of code is not evidence that all paths work.

Known items that must be tested or corrected before calling it stable:

1. **Slash-command bypass:** the current outgoing handler does not yet contain a reliable explicit slash-command check. Add it before translation, and test common commands.
2. **HTTP library contract:** verify the exact `effil_http` function signatures, callback thread context, timeout behavior and response field names against the installed library version.
3. **Incoming callback behavior:** returning `false` and asynchronously re-adding chat may affect ordering and duplicate display. Test original/translated display, failures and bursts.
4. **Outgoing send guard:** verify that `sampSendChat` does not recurse into the interception path or accidentally allow the original message. The guard must be robust even if callbacks are delayed.
5. **Incoming queue cap:** when the pending incoming count reaches its cap, the current code may leave later messages untouched. Review counter handling and ordering.
6. **mimgui API compatibility:** validate `imgui.OnFrame`, `imgui.new`, combo/input signatures and style enum availability with the installed mimgui build.
7. **Provider model IDs:** the default Grok model string may become invalid or unavailable. Keep model IDs configurable and verify them against the current xAI catalogue. Verify Gemini model access too.
8. **Unicode length:** Lua byte length is not character length. The 144-byte guard is conservative but must be checked against the server's actual chat limit and encoding.
9. **Prompt injection / untrusted chat:** treat every player message as untrusted text. The model must translate it, not follow instructions contained inside it. Strengthen prompts and consider structured delimiters.
10. **Sensitive data:** API keys are stored as plain text in the local INI. Never upload a real INI or paste keys into issue reports, screenshots or commits.

Do not advertise v1.0 as production-ready until the test plan below passes.

## 9. Manual test plan

Run these tests on a non-critical server:

- Script loads with all dependencies installed.
- Missing `samp.events`, `effil_http`, mimgui or JSON helpers produce a clear diagnostic.
- `/str` opens and closes the GUI without a Lua error.
- GUI settings save and persist after reconnect/restart.
- `/tr on`, `/tr off`, `/tr reset`, `/tr status` behave as documented.
- `/login test`, `/report test`, `/stats` and other slash commands are passed through unchanged.
- A normal outgoing message is suppressed, translated once and sent once.
- Primary Gemini success works.
- Primary Grok success works.
- Simulated primary quota/rate-limit failure switches to secondary.
- Primary timeout / connection error switches to secondary.
- Both providers failing never sends the original outgoing text.
- Translation longer than the chat limit is blocked with a clear message.
- Incoming supported player chat is translated exactly once.
- Incoming system/server messages remain untouched.
- Incoming translation failure leaves the original message visible.
- Rapid incoming messages do not reorder, duplicate or disappear.
- Disconnect/reconnect while a request is pending does not crash the script.

Record MoonLoader version, SAMP.Lua version, mimgui version, effil_http version, provider/model, exact error and reproduction steps when reporting a bug. Redact API keys.

## 10. Development rules for future contributors / AI assistants

1. Read this README and the full current `SalszATR.lua` before editing.
2. Preserve the folder boundary: all SalszATR files stay inside `SalszATR/`.
3. Do not rename commands or config keys without updating this README and migration logic.
4. Never allow untranslated outgoing text to leak when translation is enabled.
5. Never translate slash commands or server/system messages.
6. Keep provider credentials out of source code, commits, logs and screenshots.
7. Do not assume an external library's API. Inspect its actual version/source or ask for the exact error.
8. Make one focused change at a time. Explain the root cause, changed files and manual test steps.
9. Do not claim a test passed unless it was actually run in SA-MP with the relevant dependencies.
10. When changing behavior, update the architecture, limitations, configuration reference and test plan here.
11. Prefer backwards-compatible config changes. If a key or index changes, add migration/default handling.
12. Keep the script compatible with the user's target environment: SA-MP 0.3.7 R1, MoonLoader, LuaJIT, and low-spec Windows hardware.

### Handoff prompt

When another AI assistant takes over, use this brief:

> You are maintaining SalszATR, a MoonLoader Lua translator for SA-MP 0.3.7 R1. First read the entire README and SalszATR.lua. Treat the current code as an unverified v1.0 prototype. Do not claim it works without in-game tests. Preserve the safety rule that translated outgoing chat is sent only after successful translation and the original is never sent on failure. Explicitly bypass slash commands. Verify SAMP.Lua event semantics, effil_http API/thread behavior and mimgui compatibility before changing asynchronous logic. Keep API keys private. Make focused changes, update this README, and provide complete files plus a reproducible test checklist.

## 11. Version history

- **v1.0:** initial prototype with Gemini/Grok requests, automatic secondary-provider attempt, outgoing/incoming translation handlers, commands, mimgui settings UI and INI configuration. Live-game validation is pending.
