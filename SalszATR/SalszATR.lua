script_name('SalszATR')
script_author('SalszATR')
script_version('1.0')

require 'lib.moonloader'

local okSampev, sampev = pcall(require, 'samp.events')
local okHttp, http = pcall(require, 'effil_http')
local okImgui, imgui = pcall(require, 'mimgui')
local okInicfg, inicfg = pcall(require, 'inicfg')

local cfg = {
    general = {
        enabled = true,
        outgoing = true,
        incoming = true,
        target = 0,
        outStyle = 0,
        inStyle = 0,
        primary = 0,
    },
    keys = {
        gemini = '',
        grok = '',
    },
    models = {
        gemini = 'gemini-2.5-flash',
        grok = 'grok-4.7',
    }
}

local config = cfg
if okInicfg then
    config = inicfg.load(cfg, 'SalszATR')
    if not config then config = cfg end
    inicfg.save(config, 'SalszATR')
end

local state = {
    activeProvider = tonumber(config.general.primary) == 1 and 'Grok' or 'Gemini',
    busyOutgoing = false,
    translatedSend = false,
    allowedTranslated = nil,
    lastError = '',
    sent = 0,
    received = 0,
    showWindow = false,
    pendingIncoming = 0,
}

local function chat(msg, color)
    if isSampAvailable() then
        sampAddChatMessage('{65D6FF}[SalszATR]{FFFFFF} ' .. tostring(msg), color or -1)
    end
end

local function trim(s)
    return (tostring(s or ''):gsub('^%s+', ''):gsub('%s+$', ''))
end

local function saveConfig()
    if okInicfg then
        config.general.enabled = config.general.enabled and true or false
        inicfg.save(config, 'SalszATR')
    end
end

local function languageName(index)
    local names = {'English', 'German (Deutsch)', 'Spanish (Mexico)', 'Indonesian'}
    return names[(tonumber(index) or 0) + 1] or 'English'
end

local function styleName(index, incoming)
    if incoming then
        local names = {'Indonesia gaul', 'Indonesia natural', 'Indonesia formal'}
        return names[(tonumber(index) or 0) + 1] or names[1]
    end
    local names = {
        'American slang', 'Mexican slang', 'British slang', 'English soft',
        'Casual', 'Street', 'Drunk mode', 'Toxic', 'Professional', 'Gamer', 'Romantic'
    }
    return names[(tonumber(index) or 0) + 1] or names[1]
end

local function makePrompt(text, direction)
    if direction == 'out' then
        return 'Translate the following message into ' .. languageName(config.general.target) ..
            '. Writing style: ' .. styleName(config.general.outStyle, false) .. '. ' ..
            'Preserve the original meaning, names, numbers, roleplay context and intent. ' ..
            'Use natural native phrasing and the requested slang only where it fits. ' ..
            'Do not explain, do not add quotation marks, and return ONLY the translated message. ' ..
            'For Drunk mode, imitate a mildly intoxicated casual speaker without making the text unreadable. ' ..
            'Message: ' .. text
    end
    return 'Translate this incoming SA-MP player chat into Indonesian. Style: ' ..
        styleName(config.general.inStyle, true) ..
        '. Understand slang, abbreviations, typos and mixed-language text. ' ..
        'Preserve names, numbers and roleplay meaning. Return ONLY the Indonesian translation, no explanation. ' ..
        'Message: ' .. text
end

local function parseJson(body)
    if type(decodeJson) ~= 'function' then return nil end
    local ok, data = pcall(decodeJson, body)
    if ok then return data end
    return nil
end

local function extractText(provider, body)
    local data = parseJson(body)
    if type(data) ~= 'table' then return nil, 'Invalid JSON response' end

    local result
    if provider == 'Gemini' then
        local candidates = data.candidates
        if type(candidates) == 'table' and type(candidates[1]) == 'table' then
            local content = candidates[1].content
            if type(content) == 'table' and type(content.parts) == 'table' then
                local chunks = {}
                for _, part in ipairs(content.parts) do
                    if type(part.text) == 'string' then
                        chunks[#chunks + 1] = part.text
                    end
                end
                result = table.concat(chunks, '')
            end
        end
        if not result and data.error and data.error.message then
            return nil, tostring(data.error.message)
        end
    else
        if data.choices and data.choices[1] and data.choices[1].message then
            result = data.choices[1].message.content
        end
        if not result and data.error then
            return nil, tostring(data.error.message or 'Grok API error')
        end
    end

    result = trim(result)
    if result == '' then return nil, 'Empty translation response' end
    result = result:gsub('^```[%w_%-]*%s*', ''):gsub('%s*```$', '')
    result = result:gsub('^["“](.-)["”]$', '%1')
    return trim(result)
end

local function providerRequest(provider, prompt, callback)
    if not okHttp or type(http) ~= 'table' or type(http.request) ~= 'function' then
        callback(nil, 'Library effil_http belum terpasang atau tidak kompatibel')
        return
    end

    local key, url, payload, headers
    headers = {['Content-Type'] = 'application/json'}

    if provider == 'Gemini' then
        key = trim(config.keys.gemini)
        if key == '' then callback(nil, 'Gemini API key belum diisi'); return end
        url = 'https://generativelanguage.googleapis.com/v1beta/models/' ..
            tostring(config.models.gemini) .. ':generateContent'
        headers['x-goog-api-key'] = key
        payload = {
            contents = {{
                role = 'user',
                parts = {{text = prompt}}
            }},
            generationConfig = {temperature = 0.35, maxOutputTokens = 180}
        }
    else
        key = trim(config.keys.grok)
        if key == '' then callback(nil, 'Grok API key belum diisi'); return end
        url = 'https://api.x.ai/v1/chat/completions'
        headers['Authorization'] = 'Bearer ' .. key
        payload = {
            model = tostring(config.models.grok),
            messages = {
                {role = 'system', content = 'You are a precise multilingual game chat translator. Return only the translation.'},
                {role = 'user', content = prompt}
            },
            temperature = 0.35,
            max_tokens = 180
        }
    end

    local okEncode, body = pcall(encodeJson, payload)
    if not okEncode or type(body) ~= 'string' then
        callback(nil, 'Gagal membuat JSON request')
        return
    end

    http.request({
        url = url,
        method = 'POST',
        headers = headers,
        body = body,
        timeout = 28
    }, function(response, err)
        if err then callback(nil, tostring(err)); return end
        if not response then callback(nil, 'Tidak ada response API'); return end
        if response.status < 200 or response.status >= 300 then
            local detail = 'HTTP ' .. tostring(response.status)
            local data = parseJson(response.body)
            if data and data.error and data.error.message then
                detail = detail .. ': ' .. tostring(data.error.message)
            end
            callback(nil, detail, response.status)
            return
        end
        local translated, parseErr = extractText(provider, response.body)
        callback(translated, parseErr, response.status)
    end)
end

local function translateWithFallback(text, direction, callback)
    local primary = state.activeProvider
    local secondary = primary == 'Gemini' and 'Grok' or 'Gemini'
    local prompt = makePrompt(text, direction)

    providerRequest(primary, prompt, function(result, err, status)
        if result then
            callback(result, primary)
            return
        end

        state.lastError = primary .. ': ' .. tostring(err)
        providerRequest(secondary, prompt, function(fallbackResult, fallbackErr)
            if fallbackResult then
                state.activeProvider = secondary
                config.general.primary = secondary == 'Grok' and 1 or 0
                saveConfig()
                chat(primary .. ' gagal, otomatis pindah ke ' .. secondary .. '.', 0xFFFFC857)
                callback(fallbackResult, secondary)
            else
                state.lastError = tostring(err) .. ' | ' .. secondary .. ': ' .. tostring(fallbackErr)
                callback(nil, nil, state.lastError)
            end
        end)
    end)
end

local function sendTranslated(text)
    if not isSampAvailable() then return end
    if #text > 144 then
        chat('Hasil terjemahan lebih dari 144 byte. Pesan ditahan, tidak dikirim.', 0xFFFF6666)
        return
    end
    state.allowedTranslated = text
    state.translatedSend = true
    sampSendChat(text)
    state.translatedSend = false
end

local function handleOutgoing(message)
    if not config.general.enabled or not config.general.outgoing then return nil end
    if state.translatedSend then return nil end
    if state.allowedTranslated and message == state.allowedTranslated then
        state.allowedTranslated = nil
        return nil
    end
    if state.busyOutgoing then
        chat('Masih menerjemahkan pesan sebelumnya. Tunggu sebentar.', 0xFFFFC857)
        return false
    end

    message = trim(message)
    if message == '' then return false end
    state.busyOutgoing = true
    chat('Menerjemahkan... pesan asli ditahan.', 0xFF9AA7B2)

    translateWithFallback(message, 'out', function(translated, provider, err)
        state.busyOutgoing = false
        if translated then
            state.sent = state.sent + 1
            chat('[' .. provider .. '] ' .. translated, 0xFF65D6FF)
            sendTranslated(translated)
        else
            state.lastError = tostring(err or 'Unknown error')
            chat('GAGAL. Pesan asli TIDAK dikirim. ' .. state.lastError, 0xFFFF6666)
        end
    end)
    return false
end

local function handleIncoming(color, text)
    if not config.general.enabled or not config.general.incoming then return nil end

    -- Only intercept common player-chat format: [playerId] PlayerName: message.
    -- Server/system notifications are deliberately left untouched.
    local prefix, body = tostring(text):match('^(.-%[%d+%].-:%s*)(.+)$')
    if not prefix or not body or trim(body) == '' then return nil end

    state.pendingIncoming = state.pendingIncoming + 1
    if state.pendingIncoming > 8 then
        state.pendingIncoming = 8
        return nil
    end

    translateWithFallback(body, 'in', function(translated)
        state.pendingIncoming = math.max(0, state.pendingIncoming - 1)
        if translated and isSampAvailable() then
            state.received = state.received + 1
            sampAddChatMessage(prefix .. translated, color)
        else
            if isSampAvailable() then sampAddChatMessage(text, color) end
        end
    end)
    return false
end

local function registerCommands()
    sampRegisterChatCommand('str', function()
        if okImgui then
            state.showWindow = not state.showWindow
        else
            chat('mimgui belum terpasang.')
        end
    end)

    sampRegisterChatCommand('tr', function(arg)
        arg = trim(arg):lower()
        if arg == 'on' then
            config.general.enabled = true
            saveConfig()
            chat('Translator aktif.')
        elseif arg == 'off' then
            config.general.enabled = false
            saveConfig()
            chat('Translator nonaktif.')
        elseif arg == 'reset' then
            state.activeProvider = tonumber(config.general.primary) == 1 and 'Grok' or 'Gemini'
            chat('Provider aktif di-reset ke ' .. state.activeProvider .. '.')
        elseif arg == 'status' or arg == '' then
            chat('Status: ' .. (config.general.enabled and 'ON' or 'OFF') ..
                ' | Provider: ' .. state.activeProvider .. ' | /str untuk pengaturan')
        else
            chat('Gunakan /tr on, /tr off, /tr reset, /tr status')
        end
    end)
end

local function setupImgui()
    if not okImgui then return end
    local ffi = require 'ffi'
    local show = imgui.new.bool(true)
    local enabled = imgui.new.bool(config.general.enabled)
    local outgoing = imgui.new.bool(config.general.outgoing)
    local incoming = imgui.new.bool(config.general.incoming)
    local target = imgui.new.int(config.general.target)
    local outStyle = imgui.new.int(config.general.outStyle)
    local inStyle = imgui.new.int(config.general.inStyle)
    local primary = imgui.new.int(config.general.primary)
    local geminiKey = imgui.new.char[256]()
    local grokKey = imgui.new.char[256]()
    ffi.copy(geminiKey, tostring(config.keys.gemini or ''))
    ffi.copy(grokKey, tostring(config.keys.grok or ''))

    local targets = {'English', 'German', 'Spanish (Mexico)', 'Indonesian'}
    local outStyles = {'American slang', 'Mexican slang', 'British slang', 'English soft',
        'Casual', 'Street', 'Drunk mode', 'Toxic', 'Professional', 'Gamer', 'Romantic'}
    local inStyles = {'Indonesia gaul', 'Indonesia natural', 'Indonesia formal'}
    local providers = {'Gemini first', 'Grok first'}

    pcall(function()
        local style = imgui.GetStyle()
        style.WindowRounding = 9
        style.ChildRounding = 7
        style.FrameRounding = 6
        style.GrabRounding = 6
        style.ScrollbarRounding = 8
        style.WindowPadding = imgui.ImVec2(14, 12)
        style.FramePadding = imgui.ImVec2(8, 6)
        style.ItemSpacing = imgui.ImVec2(8, 8)
        style.Colors[imgui.Col.WindowBg] = imgui.ImVec4(0.035, 0.065, 0.085, 0.98)
        style.Colors[imgui.Col.TitleBg] = imgui.ImVec4(0.025, 0.045, 0.060, 1.00)
        style.Colors[imgui.Col.TitleBgActive] = imgui.ImVec4(0.045, 0.105, 0.135, 1.00)
        style.Colors[imgui.Col.FrameBg] = imgui.ImVec4(0.075, 0.115, 0.140, 1.00)
        style.Colors[imgui.Col.FrameBgHovered] = imgui.ImVec4(0.100, 0.190, 0.225, 1.00)
        style.Colors[imgui.Col.Button] = imgui.ImVec4(0.055, 0.245, 0.310, 1.00)
        style.Colors[imgui.Col.ButtonHovered] = imgui.ImVec4(0.075, 0.355, 0.430, 1.00)
        style.Colors[imgui.Col.CheckMark] = imgui.ImVec4(0.25, 0.82, 1.00, 1.00)
        style.Colors[imgui.Col.Header] = imgui.ImVec4(0.055, 0.245, 0.310, 0.85)
    end)

    imgui.OnFrame(
        function() return state.showWindow end,
        function()
            imgui.SetNextWindowSize(imgui.ImVec2(520, 510), imgui.Cond.FirstUseEver)
            imgui.Begin('SalszATR  |  AI Translator', show)
            imgui.TextColored(imgui.ImVec4(0.38, 0.82, 1.0, 1.0), 'SA-MP 0.3.7 R1  /  v1.0')
            imgui.Separator()

            if imgui.Checkbox('Master switch', enabled) then
                config.general.enabled = enabled[0]
                saveConfig()
            end
            if imgui.Checkbox('Outgoing translation', outgoing) then
                config.general.outgoing = outgoing[0]
                saveConfig()
            end
            if imgui.Checkbox('Incoming translation', incoming) then
                config.general.incoming = incoming[0]
                saveConfig()
            end

            imgui.Separator()
            imgui.Text('OUTGOING')
            if imgui.Combo('Target language', target, targets, #targets) then
                config.general.target = target[0]
                saveConfig()
            end
            if imgui.Combo('Writing style', outStyle, outStyles, #outStyles) then
                config.general.outStyle = outStyle[0]
                saveConfig()
            end

            imgui.Separator()
            imgui.Text('INCOMING')
            if imgui.Combo('Indonesian style', inStyle, inStyles, #inStyles) then
                config.general.inStyle = inStyle[0]
                saveConfig()
            end

            imgui.Separator()
            imgui.Text('AI PROVIDERS')
            if imgui.Combo('Primary provider', primary, providers, #providers) then
                config.general.primary = primary[0]
                state.activeProvider = primary[0] == 1 and 'Grok' or 'Gemini'
                saveConfig()
            end
            imgui.Text('Active: ' .. state.activeProvider .. '  |  Sent: ' .. state.sent ..
                '  |  Received: ' .. state.received)
            imgui.InputText('Gemini API key', geminiKey, 256, imgui.InputTextFlags.Password)
            imgui.InputText('Grok API key', grokKey, 256, imgui.InputTextFlags.Password)

            if imgui.Button('Save API keys and settings', imgui.ImVec2(-1, 30)) then
                config.keys.gemini = ffi.string(geminiKey)
                config.keys.grok = ffi.string(grokKey)
                config.general.enabled = enabled[0]
                config.general.outgoing = outgoing[0]
                config.general.incoming = incoming[0]
                config.general.target = target[0]
                config.general.outStyle = outStyle[0]
                config.general.inStyle = inStyle[0]
                config.general.primary = primary[0]
                state.activeProvider = primary[0] == 1 and 'Grok' or 'Gemini'
                saveConfig()
                chat('Konfigurasi disimpan.')
            end

            if imgui.Button('Close', imgui.ImVec2(-1, 26)) then
                state.showWindow = false
            end
            if state.lastError ~= '' then
                imgui.TextWrapped('Last error: ' .. state.lastError)
            end
            imgui.End()
            if not show[0] then
                state.showWindow = false
                show[0] = true
            end
        end
    )
end

function main()
    repeat wait(100) until isSampAvailable()

    if not okSampev then
        chat('Library samp.events tidak ditemukan. Install SAMP.Lua.')
        return
    end
    -- Register commands before optional network-library checks.
    -- This keeps /str and /tr available even when effil_http is missing.
    setupImgui()
    registerCommands()

    if not okImgui then
        chat('mimgui belum terpasang. GUI /str belum tersedia, tetapi /tr tetap aktif.')
    end

    if type(encodeJson) ~= 'function' or type(decodeJson) ~= 'function' then
        chat('Fungsi encodeJson/decodeJson MoonLoader tidak tersedia. Fitur AI belum bisa digunakan.')
        return
    end

    if not okHttp or type(http) ~= 'table' or type(http.run) ~= 'function' then
        chat('effil_http belum terpasang/kompatibel. Command /str dan /tr tetap aktif; fitur terjemahan menunggu library.')
    else
        local okRun, runErr = pcall(http.run, 50)
        if not okRun then
            chat('Gagal menjalankan effil_http: ' .. tostring(runErr))
        end
    end

    chat('SalszATR v1.0 loaded. /str untuk menu, /tr status untuk status.')
    while true do
        wait(250)
    end
end

if okSampev then
    function sampev.onSendChat(message)
        return handleOutgoing(message)
    end

    function sampev.onServerMessage(color, text)
        return handleIncoming(color, text)
    end
end
