local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local HttpService = game:GetService("HttpService")
local TeleportService = game:GetService("TeleportService")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local SoundService = game:GetService("SoundService")

local player = Players.LocalPlayer
local guiName = "ZYROX_AJ"

if CoreGui:FindFirstChild(guiName) then CoreGui[guiName]:Destroy() end

local WEBHOOK_URL = "https://discord.com/api/webhooks/1504278778740736153/xFt5bKpOo9pn2ei01RKLWnPsH-Q_1T_zMg-qawIirhMyhesu31C3gBrSZD8_W7Vxziw8"
local TARGET_GAME_ID = 109983668079237

local NotifSound = Instance.new("Sound")
NotifSound.Name = "ZYROXNotifSound"
NotifSound.SoundId = "rbxassetid://4590662766"
NotifSound.Volume = 0.5
NotifSound.Parent = SoundService

-- CDN Images for webhook
local BRAINROT_IMAGES = {
    ["Strawberry Elephant"] = "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    ["Meowl"] = "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    ["Headless Horseman"] = "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    ["Skibidi Toilet"] = "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png",
    ["John Pork"] = "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    ["Griffin"] = "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp",
    ["Dragon Cannelloni"] = "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp",
    ["Burguro And Fryuro"] = "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp",
    ["Capitano Moby"] = "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp",
    ["Garama and Madundung"] = "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    ["Ketchuru and Masturu"] = "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    ["Esok Sekolah"] = "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    ["Los Bros"] = "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png",
    ["Tictac Sahur"] = "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp",
    ["La Extinct Grande"] = "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE",
    ["Ketupat Kepat"] = "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp",
    ["Los Combinasionas"] = "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp",
    ["Tralaledon"] = "https://images-ext-1.discordapp.net/external/_bBDdfMFPbTdCGnkfiz3yzvtNwqz0P4iVOnTlxFfaME/%3Fcb%3D20250909171639/https/static.wikia.nocookie.net/stealabr/images/7/79/Brr_Brr_Patapem.png/revision/latest?format=webp",
    ["Nuclearo Dinosauro"] = "https://images-ext-1.discordapp.net/external/wO_VfzWxp76PImVCn4peFiARwLyzlEbzI8SqaKEtXio/%3Fcb%3D20260328003025/https/static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png/revision/latest/scale-to-width-down/1000?format=webp",
    ["La Grande Combinasion"] = "https://images-ext-1.discordapp.net/external/l-HH_TrxOC9-VzpqWi-oTxrXNsdH7jIVxAuZI0diczo/https/www.mobynotifier.com/brainrots/la-grande-combinasion?format=webp",
    ["La Romantic Grande"] = "https://static.wikia.nocookie.net/stealabr/images/6/69/La_Romantic_Grande2.png",
    ["Money Money Puggy"] = "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter?format=webp",
}

local BRAINROTS = {
    -- Low tier (common logs)
    {name = "Los Combinasionas", income = 15, rarity = "Secret", weight = 30},
    {name = "Los Hotspotsitos", income = 20, rarity = "Secret", weight = 30},
    {name = "Tictac Sahur", income = 37.5, rarity = "Secret", weight = 25},
    {name = "Ketupat Kepat", income = 35, rarity = "Secret", weight = 25},
    {name = "La Extinct Grande", income = 23.5, rarity = "Secret", weight = 25},
    {name = "La Grande Combinasion", income = 10, rarity = "Secret", weight = 20},
    {name = "Nuclearo Dinosauro", income = 15, rarity = "Secret", weight = 20},
    {name = "Tralaledon", income = 27.5, rarity = "Secret", weight = 20},
    {name = "Money Money Puggy", income = 21, rarity = "Secret", weight = 20},
    {name = "Garama and Madundung", income = 50, rarity = "Secret", weight = 15},
    {name = "Ketchuru and Masturu", income = 42.5, rarity = "Secret", weight = 15},
    {name = "Esok Sekolah", income = 30, rarity = "Secret", weight = 15},
    {name = "Los Bros", income = 24, rarity = "Secret", weight = 15},
    -- Mid tier
    {name = "Spaghetti Tualetti", income = 60, rarity = "Secret", weight = 10},
    {name = "Fragrama and Chocrama", income = 100, rarity = "Secret", weight = 10},
    {name = "La Casa Boo", income = 100, rarity = "Secret", weight = 10},
    {name = "Cash or Card", income = 100, rarity = "Secret", weight = 10},
    {name = "Capitano Moby", income = 160, rarity = "Secret", weight = 8},
    {name = "Burguro And Fryuro", income = 150, rarity = "Secret", weight = 8},
    {name = "Cooki and Milki", income = 155, rarity = "Secret", weight = 8},
    -- High tier (rare)
    {name = "Love Love Bear", income = 225, rarity = "Secret", weight = 5},
    {name = "Cerberus", income = 175, rarity = "Secret", weight = 5},
    {name = "Celestial Pegasus", income = 175, rarity = "Secret", weight = 5},
    {name = "Dragon Cannelloni", income = 250, rarity = "Secret", weight = 4},
    {name = "Griffin", income = 400, rarity = "OG", weight = 3},
    -- OG (very rare)
    {name = "Skibidi Toilet", income = 450, rarity = "OG", weight = 2},
    {name = "John Pork", income = 500, rarity = "OG", weight = 2},
    {name = "Headless Horseman", income = 550, rarity = "OG", weight = 1},
    {name = "Meowl", income = 600, rarity = "OG", weight = 1},
    {name = "Strawberry Elephant", income = 750, rarity = "OG", weight = 1},
}

local MUTATIONS = {
    {name = "Normal", mod = 0.0, chance = 70},
    {name = "Gold", mod = 0.25, chance = 12},
    {name = "Diamond", mod = 0.5, chance = 8},
    {name = "Candy", mod = 3.0, chance = 3},
    {name = "Lava", mod = 5.0, chance = 2},
    {name = "Galaxy", mod = 6.0, chance = 2},
    {name = "Yin Yang", mod = 6.5, chance = 1},
    {name = "Radioactive", mod = 7.5, chance = 1},
    {name = "Cursed", mod = 8.0, chance = 0.5},
    {name = "Rainbow", mod = 9.0, chance = 0.3},
    {name = "Divine", mod = 9.0, chance = 0.2},
    {name = "Cyber", mod = 10.0, chance = 0.1},
}

local TRAITS = {
    {name = "None", mod = 0.0, chance = 95},
    {name = "Strawberry", mod = 8.0, chance = 1},
    {name = "Meowl", mod = 7.0, chance = 1},
    {name = "Is Calling", mod = 7.5, chance = 0.5},
    {name = "Galactic", mod = 3.0, chance = 1},
    {name = "Fireworks", mod = 5.0, chance = 0.5},
    {name = "Lightning", mod = 5.0, chance = 0.5},
    {name = "Spider", mod = 3.5, chance = 0.5},
}

local Colors = {
    Bg = Color3.fromRGB(8, 12, 20),
    Surface = Color3.fromRGB(18, 25, 38),
    SurfaceLight = Color3.fromRGB(28, 38, 55),
    Border = Color3.fromRGB(0, 100, 255),
    Text = Color3.fromRGB(220, 230, 255),
    TextDim = Color3.fromRGB(100, 120, 150),
    Green = Color3.fromRGB(0, 200, 100),
    Red = Color3.fromRGB(255, 50, 50),
    Blue = Color3.fromRGB(0, 120, 255),
    Purple = Color3.fromRGB(150, 80, 220),
    Yellow = Color3.fromRGB(255, 200, 50),
}

local function weightedChoice(list)
    local total = 0
    for _, item in ipairs(list) do total = total + (item.chance or item.weight or 1) end
    local rand = math.random() * total
    local accum = 0
    for _, item in ipairs(list) do
        accum = accum + (item.chance or item.weight or 1)
        if rand <= accum then return item end
    end
    return list[1]
end

local function formatIncome(value)
    if value >= 1000 then
        return string.format("%.2fB", value / 1000)
    end
    return string.format("%.0fM", value)
end

local function getTier(value)
    if value >= 5000 then return {name = "Peaklights", color = Colors.Purple}
    elseif value >= 2000 then return {name = "Highlights", color = Colors.Yellow}
    elseif value >= 500 then return {name = "Midlights", color = Colors.Blue}
    else return {name = "Lowlights", color = Colors.TextDim} end
end

local function calculateIncome(baseIncome, mutation, trait)
    if mutation.name == "Normal" and trait.name == "None" then
        return baseIncome
    end
    return baseIncome * (1 + mutation.mod + trait.mod)
end

local function getRandomBrainrot()
    local brainrot = weightedChoice(BRAINROTS)
    local mutation = weightedChoice(MUTATIONS)
    local trait = weightedChoice(TRAITS)
    
    if math.random() < 0.9 then
        trait = {name = "None", mod = 0.0, chance = 0}
    end
    
    if brainrot.name == "Strawberry Elephant" and math.random() < 0.02 then
        trait = {name = "Strawberry", mod = 8.0, chance = 0}
    end
    if brainrot.name == "Meowl" and math.random() < 0.02 then
        trait = {name = "Meowl", mod = 7.0, chance = 0}
    end
    
    local finalIncome = calculateIncome(brainrot.income, mutation, trait)
    local tier = getTier(finalIncome)
    
    local displayName = brainrot.name
    if mutation.name ~= "Normal" then
        displayName = mutation.name .. " " .. displayName
    end
    if trait.name ~= "None" then
        displayName = displayName .. " (" .. trait.name .. ")"
    end
    
    return {
        name = displayName,
        originalName = brainrot.name,
        income = finalIncome,
        formattedIncome = formatIncome(finalIncome),
        tier = tier.name,
        tierColor = tier.color,
        mutation = mutation.name,
        trait = trait.name,
        rarity = brainrot.rarity,
        image = BRAINROT_IMAGES[brainrot.name] or "https://i.imgur.com/placeholder.png",
        timestamp = os.time(),
    }
end

-- Create GUI (smaller)
local gui = Instance.new("ScreenGui")
gui.Name = guiName
gui.Parent = CoreGui
gui.ResetOnSpawn = false

local mainFrame = Instance.new("Frame")
mainFrame.Size = UDim2.new(0, 280, 0, 380)
mainFrame.Position = UDim2.new(0.5, -140, 0.5, -190)
mainFrame.BackgroundColor3 = Colors.Bg
mainFrame.BorderSizePixel = 0
mainFrame.Active = true
mainFrame.Draggable = true
mainFrame.Parent = gui

local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 12)
corner.Parent = mainFrame

local border = Instance.new("UIStroke")
border.Color = Colors.Border
border.Thickness = 1
border.Parent = mainFrame

local titleBar = Instance.new("Frame")
titleBar.Size = UDim2.new(1, 0, 0, 36)
titleBar.BackgroundColor3 = Colors.Surface
titleBar.BorderSizePixel = 0
titleBar.Parent = mainFrame

local titleCorner = Instance.new("UICorner")
titleCorner.CornerRadius = UDim.new(0, 12)
titleCorner.Parent = titleBar

local titleText = Instance.new("TextLabel")
titleText.Size = UDim2.new(1, -70, 1, 0)
titleText.Position = UDim2.new(0, 12, 0, 0)
titleText.BackgroundTransparency = 1
titleText.Text = "ZYROX"
titleText.TextColor3 = Colors.Blue
titleText.TextSize = 15
titleText.Font = Enum.Font.GothamBold
titleText.TextXAlignment = Enum.TextXAlignment.Left
titleText.Parent = titleBar

local botCountLabel = Instance.new("TextLabel")
botCountLabel.Size = UDim2.new(0, 75, 0, 22)
botCountLabel.Position = UDim2.new(0.5, -37, 0, 7)
botCountLabel.BackgroundColor3 = Colors.SurfaceLight
botCountLabel.Text = "11,234"
botCountLabel.TextColor3 = Colors.Green
botCountLabel.TextSize = 10
botCountLabel.Font = Enum.Font.GothamBold
botCountLabel.Parent = titleBar
local botCorner = Instance.new("UICorner")
botCorner.CornerRadius = UDim.new(1, 0)
botCorner.Parent = botCountLabel

local minButton = Instance.new("TextButton")
minButton.Size = UDim2.new(0, 26, 0, 26)
minButton.Position = UDim2.new(1, -56, 0.5, -13)
minButton.BackgroundColor3 = Colors.SurfaceLight
minButton.Text = "−"
minButton.TextColor3 = Colors.TextDim
minButton.TextSize = 18
minButton.Font = Enum.Font.GothamBold
minButton.BorderSizePixel = 0
minButton.Parent = titleBar
local minCorner = Instance.new("UICorner")
minCorner.CornerRadius = UDim.new(0, 6)
minCorner.Parent = minButton

local closeButton = Instance.new("TextButton")
closeButton.Size = UDim2.new(0, 26, 0, 26)
closeButton.Position = UDim2.new(1, -28, 0.5, -13)
closeButton.BackgroundColor3 = Colors.SurfaceLight
closeButton.Text = "✕"
closeButton.TextColor3 = Colors.Red
closeButton.TextSize = 12
closeButton.Font = Enum.Font.GothamBold
closeButton.BorderSizePixel = 0
closeButton.Parent = titleBar
local closeCorner = Instance.new("UICorner")
closeCorner.CornerRadius = UDim.new(0, 6)
closeCorner.Parent = closeButton

local contentPanel = Instance.new("Frame")
contentPanel.Size = UDim2.new(1, 0, 1, -36)
contentPanel.Position = UDim2.new(0, 0, 0, 36)
contentPanel.BackgroundTransparency = 1
contentPanel.Parent = mainFrame

local logsContainer = Instance.new("ScrollingFrame")
logsContainer.Size = UDim2.new(1, -12, 1, -46)
logsContainer.Position = UDim2.new(0, 6, 0, 6)
logsContainer.BackgroundTransparency = 1
logsContainer.BorderSizePixel = 0
logsContainer.ScrollBarThickness = 3
logsContainer.Parent = contentPanel

local logsLayout = Instance.new("UIListLayout")
logsLayout.Parent = logsContainer
logsLayout.Padding = UDim.new(0, 4)
logsLayout.SortOrder = Enum.SortOrder.LayoutOrder

local function addLogEntry(brainrot)
    local logFrame = Instance.new("Frame")
    logFrame.Size = UDim2.new(1, 0, 0, 50)
    logFrame.BackgroundColor3 = Colors.Surface
    logFrame.BorderSizePixel = 0
    logFrame.Parent = logsContainer
    
    local logCorner = Instance.new("UICorner")
    logCorner.CornerRadius = UDim.new(0, 8)
    logCorner.Parent = logFrame
    
    local tierBar = Instance.new("Frame")
    tierBar.Size = UDim2.new(0, 3, 1, -6)
    tierBar.Position = UDim2.new(0, 4, 0, 3)
    tierBar.BackgroundColor3 = brainrot.tierColor
    tierBar.BorderSizePixel = 0
    tierBar.Parent = logFrame
    
    local barCorner = Instance.new("UICorner")
    barCorner.CornerRadius = UDim.new(0, 2)
    barCorner.Parent = tierBar
    
    local nameLabel = Instance.new("TextLabel")
    nameLabel.Size = UDim2.new(1, -95, 0, 16)
    nameLabel.Position = UDim2.new(0, 12, 0, 5)
    nameLabel.BackgroundTransparency = 1
    nameLabel.Text = brainrot.name
    nameLabel.TextColor3 = Colors.Text
    nameLabel.TextSize = 10
    nameLabel.Font = Enum.Font.GothamBold
    nameLabel.TextXAlignment = Enum.TextXAlignment.Left
    nameLabel.TextTruncate = Enum.TextTruncate.AtEnd
    nameLabel.Parent = logFrame
    
    local infoLabel = Instance.new("TextLabel")
    infoLabel.Size = UDim2.new(1, -95, 0, 12)
    infoLabel.Position = UDim2.new(0, 12, 0, 23)
    infoLabel.BackgroundTransparency = 1
    infoLabel.Text = brainrot.formattedIncome .. "/s · " .. brainrot.tier
    infoLabel.TextColor3 = brainrot.tierColor
    infoLabel.TextSize = 9
    infoLabel.Font = Enum.Font.Gotham
    infoLabel.TextXAlignment = Enum.TextXAlignment.Left
    infoLabel.Parent = logFrame
    
    local joinButton = Instance.new("TextButton")
    joinButton.Size = UDim2.new(0, 48, 0, 28)
    joinButton.Position = UDim2.new(1, -54, 0, 10)
    joinButton.BackgroundColor3 = Colors.Blue
    joinButton.Text = "JOIN"
    joinButton.TextColor3 = Colors.Text
    joinButton.TextSize = 9
    joinButton.Font = Enum.Font.GothamBold
    joinButton.BorderSizePixel = 0
    joinButton.Parent = logFrame
    
    local joinCorner = Instance.new("UICorner")
    joinCorner.CornerRadius = UDim.new(0, 6)
    joinCorner.Parent = joinButton
    
    joinButton.MouseButton1Click:Connect(function()
        joinButton.Text = "TP"
        joinButton.BackgroundColor3 = Colors.Green
        pcall(function()
            TeleportService:Teleport(TARGET_GAME_ID, player)
        end)
        task.wait(1.5)
        joinButton.Text = "JOIN"
        joinButton.BackgroundColor3 = Colors.Blue
    end)
    
    logsLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        logsContainer.CanvasSize = UDim2.new(0, 0, 0, logsLayout.AbsoluteContentSize.Y + 10)
    end)
    
    return logFrame
end

local autoJoinFrame = Instance.new("Frame")
autoJoinFrame.Size = UDim2.new(1, -12, 0, 32)
autoJoinFrame.Position = UDim2.new(0, 6, 1, -38)
autoJoinFrame.BackgroundColor3 = Colors.Surface
autoJoinFrame.BorderSizePixel = 0
autoJoinFrame.Parent = contentPanel

local autoCorner = Instance.new("UICorner")
autoCorner.CornerRadius = UDim.new(0, 8)
autoCorner.Parent = autoJoinFrame

local autoLabel = Instance.new("TextLabel")
autoLabel.Size = UDim2.new(0, 70, 1, 0)
autoLabel.Position = UDim2.new(0, 10, 0, 0)
autoLabel.BackgroundTransparency = 1
autoLabel.Text = "AUTO JOIN"
autoLabel.TextColor3 = Colors.TextDim
autoLabel.TextSize = 10
autoLabel.Font = Enum.Font.GothamBold
autoLabel.TextXAlignment = Enum.TextXAlignment.Left
autoLabel.Parent = autoJoinFrame

local autoToggle = Instance.new("TextButton")
autoToggle.Size = UDim2.new(0, 42, 0, 22)
autoToggle.Position = UDim2.new(1, -50, 0.5, -11)
autoToggle.BackgroundColor3 = Colors.SurfaceLight
autoToggle.Text = ""
autoToggle.BorderSizePixel = 0
autoToggle.Parent = autoJoinFrame

local toggleCorner = Instance.new("UICorner")
toggleCorner.CornerRadius = UDim.new(1, 0)
toggleCorner.Parent = autoToggle

local toggleKnob = Instance.new("Frame")
toggleKnob.Size = UDim2.new(0, 18, 0, 18)
toggleKnob.Position = UDim2.new(0, 2, 0.5, -9)
toggleKnob.BackgroundColor3 = Colors.TextDim
toggleKnob.BorderSizePixel = 0
toggleKnob.Parent = autoToggle

local knobCorner = Instance.new("UICorner")
knobCorner.CornerRadius = UDim.new(1, 0)
knobCorner.Parent = toggleKnob

local autoStatus = Instance.new("TextLabel")
autoStatus.Size = UDim2.new(0, 30, 1, 0)
autoStatus.Position = UDim2.new(1, -80, 0, 0)
autoStatus.BackgroundTransparency = 1
autoStatus.Text = "OFF"
autoStatus.TextColor3 = Colors.TextDim
autoStatus.TextSize = 9
autoStatus.Font = Enum.Font.GothamBold
autoStatus.Parent = autoJoinFrame

local guiVisible = true
local autoJoinEnabled = false
local isMinimized = false
local botCount = math.random(11000, 17000)
local botCountDirection = 1
local initialized = false

local function updateBotCount()
    local variation = math.random(100, 400)
    botCount = botCount + (botCountDirection * variation)
    if botCount >= 17000 then
        botCount = 17000
        botCountDirection = -1
    elseif botCount <= 11000 then
        botCount = 11000
        botCountDirection = 1
    end
    botCountLabel.Text = string.format("%d", botCount)
end

local function updateAutoUI()
    if autoJoinEnabled then
        autoToggle.BackgroundColor3 = Colors.Green
        toggleKnob.Position = UDim2.new(1, -20, 0.5, -9)
        toggleKnob.BackgroundColor3 = Colors.Text
        autoStatus.Text = "ON"
        autoStatus.TextColor3 = Colors.Green
    else
        autoToggle.BackgroundColor3 = Colors.SurfaceLight
        toggleKnob.Position = UDim2.new(0, 2, 0.5, -9)
        toggleKnob.BackgroundColor3 = Colors.TextDim
        autoStatus.Text = "OFF"
        autoStatus.TextColor3 = Colors.TextDim
    end
end

autoToggle.MouseButton1Click:Connect(function()
    autoJoinEnabled = not autoJoinEnabled
    updateAutoUI()
end)

local function setMinimized(minimized)
    isMinimized = minimized
    if minimized then
        contentPanel.Visible = false
        mainFrame.Size = UDim2.new(0, 280, 0, 36)
    else
        contentPanel.Visible = true
        mainFrame.Size = UDim2.new(0, 280, 0, 380)
    end
end

minButton.MouseButton1Click:Connect(function()
    setMinimized(not isMinimized)
end)

closeButton.MouseButton1Click:Connect(function()
    gui:Destroy()
    if SoundService:FindFirstChild("ZYROXNotifSound") then
        SoundService.ZYROXNotifSound:Destroy()
    end
end)

local dragging = false
local dragInput
local dragStart
local startPos

mainFrame.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
        dragging = true
        dragStart = input.Position
        startPos = mainFrame.Position
        input.Changed:Connect(function()
            if input.UserInputState == Enum.UserInputState.End then
                dragging = false
            end
        end)
    end
end)

UserInputService.InputChanged:Connect(function(input)
    if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
        local delta = input.Position - dragStart
        mainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)

UserInputService.InputBegan:Connect(function(input, processed)
    if processed then return end
    if input.KeyCode == Enum.KeyCode.RightShift then
        if isMinimized then
            setMinimized(false)
        else
            guiVisible = not guiVisible
            mainFrame.Visible = guiVisible
        end
    end
end)

local function sendWebhook(brainrot)
    local embed = {
        title = "🎯 NEW BRAINROT DETECTED",
        description = "**" .. brainrot.name .. "** has been detected!",
        color = brainrot.tier == "Peaklights" and 0xAF52DE or (brainrot.tier == "Highlights" and 0xFFD60A or (brainrot.tier == "Midlights" and 0x0A84FF or 0x8E8E93)),
        timestamp = os.date("!%Y-%m-%dT%H:%M:%S.000Z", os.time()),
        thumbnail = {url = brainrot.image},
        fields = {
            {name = "🧬 Mutation", value = brainrot.mutation, inline = true},
            {name = "✨ Trait", value = brainrot.trait, inline = true},
            {name = "💰 Income", value = brainrot.formattedIncome .. "/s", inline = true},
            {name = "🏆 Tier", value = brainrot.tier, inline = true},
            {name = "🤖 Active Bots", value = string.format("%d", botCount), inline = true},
        },
        footer = {text = "ZYROX AJ • " .. brainrot.rarity .. " Brainrot"},
    }
    pcall(function()
        HttpService:PostAsync(WEBHOOK_URL, HttpService:JSONEncode({embeds = {embed}, username = "ZYROX AJ"}), Enum.HttpContentType.ApplicationJson)
    end)
end

local function showDesktopNotif(brainrot)
    local notif = Instance.new("ScreenGui")
    notif.Name = "ZYROXNotif"
    notif.Parent = CoreGui
    
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(0, 280, 0, 70)
    frame.Position = UDim2.new(0.5, -140, 0, -100)
    frame.BackgroundColor3 = Colors.Surface
    frame.BorderSizePixel = 0
    frame.Parent = notif
    
    local frameCorner = Instance.new("UICorner")
    frameCorner.CornerRadius = UDim.new(0, 10)
    frameCorner.Parent = frame
    
    local borderStroke = Instance.new("UIStroke")
    borderStroke.Color = Colors.Border
    borderStroke.Thickness = 1
    borderStroke.Parent = frame
    
    local tierBar2 = Instance.new("Frame")
    tierBar2.Size = UDim2.new(0, 3, 1, 0)
    tierBar2.BackgroundColor3 = brainrot.tierColor
    tierBar2.BorderSizePixel = 0
    tierBar2.Parent = frame
    
    local titleLabel = Instance.new("TextLabel")
    titleLabel.Size = UDim2.new(1, -20, 0, 18)
    titleLabel.Position = UDim2.new(0, 14, 0, 6)
    titleLabel.BackgroundTransparency = 1
    titleLabel.Text = "NEW BRAINROT"
    titleLabel.TextColor3 = brainrot.tierColor
    titleLabel.TextSize = 10
    titleLabel.Font = Enum.Font.GothamBold
    titleLabel.TextXAlignment = Enum.TextXAlignment.Left
    titleLabel.Parent = frame
    
    local nameLabel2 = Instance.new("TextLabel")
    nameLabel2.Size = UDim2.new(1, -20, 0, 22)
    nameLabel2.Position = UDim2.new(0, 14, 0, 26)
    nameLabel2.BackgroundTransparency = 1
    nameLabel2.Text = brainrot.name
    nameLabel2.TextColor3 = Colors.Text
    nameLabel2.TextSize = 11
    nameLabel2.Font = Enum.Font.GothamBold
    nameLabel2.TextXAlignment = Enum.TextXAlignment.Left
    nameLabel2.Parent = frame
    
    local priceLabel = Instance.new("TextLabel")
    priceLabel.Size = UDim2.new(0, 110, 0, 14)
    priceLabel.Position = UDim2.new(0, 14, 0, 50)
    priceLabel.BackgroundTransparency = 1
    priceLabel.Text = brainrot.formattedIncome .. "/s · " .. brainrot.tier
    priceLabel.TextColor3 = brainrot.tierColor
    priceLabel.TextSize = 8
    priceLabel.Font = Enum.Font.Gotham
    priceLabel.TextXAlignment = Enum.TextXAlignment.Left
    priceLabel.Parent = frame
    
    local joinNotifButton = Instance.new("TextButton")
    joinNotifButton.Size = UDim2.new(0, 55, 0, 28)
    joinNotifButton.Position = UDim2.new(1, -62, 0.5, -14)
    joinNotifButton.BackgroundColor3 = Colors.Blue
    joinNotifButton.Text = "JOIN"
    joinNotifButton.TextColor3 = Colors.Text
    joinNotifButton.TextSize = 9
    joinNotifButton.Font = Enum.Font.GothamBold
    joinNotifButton.BorderSizePixel = 0
    joinNotifButton.Parent = frame
    local joinCorner2 = Instance.new("UICorner")
    joinCorner2.CornerRadius = UDim.new(0, 6)
    joinCorner2.Parent = joinNotifButton
    
    joinNotifButton.MouseButton1Click:Connect(function()
        pcall(function() TeleportService:Teleport(TARGET_GAME_ID, player) end)
        notif:Destroy()
    end)
    
    local closeNotifButton = Instance.new("TextButton")
    closeNotifButton.Size = UDim2.new(0, 22, 0, 22)
    closeNotifButton.Position = UDim2.new(1, -26, 0, 5)
    closeNotifButton.BackgroundTransparency = 1
    closeNotifButton.Text = "✕"
    closeNotifButton.TextColor3 = Colors.TextDim
    closeNotifButton.TextSize = 11
    closeNotifButton.Font = Enum.Font.GothamBold
    closeNotifButton.Parent = frame
    closeNotifButton.MouseButton1Click:Connect(function() notif:Destroy() end)
    
    TweenService:Create(frame, TweenInfo.new(0.3, Enum.EasingStyle.Quad), {Position = UDim2.new(0.5, -140, 0, 60)}):Play()
    task.delay(5, function()
        if notif then
            TweenService:Create(frame, TweenInfo.new(0.2, Enum.EasingStyle.Quad), {Position = UDim2.new(0.5, -140, 0, -100)}):Play()
            task.wait(0.2)
            notif:Destroy()
        end
    end)
end

task.spawn(function()
    while gui and gui.Parent do
        updateBotCount()
        task.wait(math.random(2, 5))
    end
end)

local logQueue = {}
local isProcessing = false

local function processQueue()
    if isProcessing then return end
    isProcessing = true
    
    while #logQueue > 0 do
        local brainrot = table.remove(logQueue, 1)
        if brainrot then
            addLogEntry(brainrot)
            sendWebhook(brainrot)
            
            NotifSound:Play()
            
            if isMinimized or not guiVisible or not mainFrame.Visible then
                showDesktopNotif(brainrot)
            end
            
            if autoJoinEnabled then
                autoStatus.Text = "TP"
                autoStatus.TextColor3 = Colors.Green
                task.spawn(function()
                    pcall(function()
                        TeleportService:Teleport(TARGET_GAME_ID, player)
                    end)
                    task.wait(2)
                    if autoJoinEnabled then
                        autoStatus.Text = "ON"
                        autoStatus.TextColor3 = Colors.Green
                    end
                end)
            end
            
            local waitTime = math.random(60, 120)
            task.wait(waitTime)
        end
    end
    
    isProcessing = false
end

local logProgression = {
    {minLogs = 0, maxLogs = 5, weights = {low=80, mid=15, high=4, og=1}},
    {minLogs = 5, maxLogs = 15, weights = {low=60, mid=30, high=8, og=2}},
    {minLogs = 15, maxLogs = 30, weights = {low=40, mid=40, high=15, og=5}},
    {minLogs = 30, maxLogs = 999, weights = {low=20, mid=45, high=25, og=10}},
}

local function getWeightedBrainrot(logCount)
    local tier = "low"
    for _, stage in ipairs(logProgression) do
        if logCount >= stage.minLogs and logCount < stage.maxLogs then
            local rand = math.random(1, 100)
            if rand <= stage.weights.low then
                tier = "low"
            elseif rand <= stage.weights.low + stage.weights.mid then
                tier = "mid"
            elseif rand <= stage.weights.low + stage.weights.mid + stage.weights.high then
                tier = "high"
            else
                tier = "og"
            end
            break
        end
    end
    
    local filtered = {}
    for _, b in ipairs(BRAINROTS) do
        if tier == "low" and b.income <= 60 then
            table.insert(filtered, b)
        elseif tier == "mid" and b.income > 60 and b.income <= 200 then
            table.insert(filtered, b)
        elseif tier == "high" and b.income > 200 and b.income <= 400 then
            table.insert(filtered, b)
        elseif tier == "og" and b.rarity == "OG" then
            table.insert(filtered, b)
        end
    end
    
    if #filtered == 0 then
        filtered = BRAINROTS
    end
    
    return weightedChoice(filtered)
end

task.spawn(function()
    task.wait(30)
    
    local logCount = 0
    
    while gui and gui.Parent do
        local brainrotData = getWeightedBrainrot(logCount)
        local mutation = weightedChoice(MUTATIONS)
        local trait = weightedChoice(TRAITS)
        
        if math.random() < 0.9 then
            trait = {name = "None", mod = 0.0, chance = 0}
        end
        
        local finalIncome = calculateIncome(brainrotData.income, mutation, trait)
        local tier = getTier(finalIncome)
        
        local displayName = brainrotData.name
        if mutation.name ~= "Normal" then
            displayName = mutation.name .. " " .. displayName
        end
        if trait.name ~= "None" then
            displayName = displayName .. " (" .. trait.name .. ")"
        end
        
        local brainrot = {
            name = displayName,
            originalName = brainrotData.name,
            income = finalIncome,
            formattedIncome = formatIncome(finalIncome),
            tier = tier.name,
            tierColor = tier.color,
            mutation = mutation.name,
            trait = trait.name,
            rarity = brainrotData.rarity,
            image = BRAINROT_IMAGES[brainrotData.name] or "https://i.imgur.com/placeholder.png",
            timestamp = os.time(),
        }
        
        table.insert(logQueue, brainrot)
        processQueue()
        
        logCount = logCount + 1
        
        local extraWait = math.random(60, 120)
        task.wait(extraWait)
    end
end)

updateAutoUI()
print("ZYROX AJ LOADED")
