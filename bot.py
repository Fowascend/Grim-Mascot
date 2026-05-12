import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

SAB_GAME_IDS = [109983668079237, 85621847059032, 99606176102979]

BRAINROTS = {
    "Strawberry Elephant": {"income": 750, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp"},
    "Meowl": {"income": 600, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp"},
    "Headless Horseman": {"income": 550, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp"},
    "Skibidi Toilet": {"income": 450, "rarity": "OG", "image": ""},
    "John Pork": {"income": 500, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp"},
    "Griffin": {"income": 400, "rarity": "OG", "image": ""},
    "Hydra Dragon Cannelloni": {"income": 350, "rarity": "Secret", "image": ""},
    "Dragon Gingerini": {"income": 225, "rarity": "Secret", "image": ""},
    "Los Nooo My Hotspotsitos": {"income": 150, "rarity": "Secret", "image": ""},
    "Los Chicleteiras": {"income": 150, "rarity": "Secret", "image": ""},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp"},
    "Cooki and Milki": {"income": 155, "rarity": "Secret", "image": "https://steal-a-brainrot.wiki/wp-content/uploads/2025/11/Steal-a-Brainrot-Wiki-Cooki-and-Milki-Icon-300x300.png"},
    "Capitano Moby": {"income": 160, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp"},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp"},
    "La Supreme Combinasion": {"income": 200, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/KQBRtzBT3aoWc6WTjvoOhl2Tf64FvbWhyFW4VWbQGhQ/https/www.mobynotifier.com/brainrots/la-secret-combinasion?format=webp"},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret", "image": ""},
    "La Casa Boo": {"income": 100, "rarity": "Secret", "image": ""},
    "Cash or Card": {"income": 100, "rarity": "Secret", "image": ""},
    "Los Hotspotsitos": {"income": 25, "rarity": "Secret", "image": ""},
    "Los Bros": {"income": 37.5, "rarity": "Secret", "image": ""},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp"},
    "Tralaledon": {"income": 27.5, "rarity": "Secret", "image": ""},
    "La Karkerkar Kombinasion": {"income": 17.5, "rarity": "Secret", "image": ""},
    "Nuclearo Dinosauro": {"income": 15, "rarity": "Secret", "image": ""},
    "Los Combinasionas": {"income": 15, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp"},
    "Garama and Madundung": {"income": 50, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp"},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp"},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/yoOCxZMRDwqYzFcsYPY5GX2WY2wK4FvGgqB72P1VCV8/https/www.mobynotifier.com/brainrots/spaghetti-tualetti?format=webp"},
    "Esok Sekolah": {"income": 30, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp"},
    "Money Money Puggy": {"income": 21, "rarity": "Secret", "image": ""},
    "Cigno Fulgoro": {"income": 20, "rarity": "Secret", "image": ""},
    "La Extinct Grande": {"income": 100, "rarity": "Secret", "image": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE"},
    "Los Puggies": {"income": 30, "rarity": "Secret", "image": ""},
    "Popuru and Fizzuru": {"income": 55, "rarity": "Secret", "image": ""},
    "Cerberus": {"income": 26, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp"},
    "Spinny Hammy": {"income": 90, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/BoWX4KUkY2KLFTf2mUHpMH1tDNo2PRIq19ICSrGuRo8/https/www.mobynotifier.com/brainrots/spinny-hammy?format=webp"},
    "Mieteteira Bicicleteira": {"income": 26, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/vAAWVq--XN7-z7-XSdiqyaCW5QGpLqa9tr_NNHpt_Yk/https/www.mobynotifier.com/brainrots/mieteteira-bicicleteira?format=webp"},
    "Tang Tang Keletang": {"income": 20, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/4qWYUdmCoa0zhqxH2MKwV7Or5U9Xif8yw-AB_Gy5Lig/https/www.mobynotifier.com/brainrots/tang-tang-keletang?format=webp"},
    "La Grande Combinasion": {"income": 10, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/l-HH_TrxOC9-VzpqWi-oTxrXNsdH7jIVxAuZI0diczo/https/www.mobynotifier.com/brainrots/la-grande-combinasion?format=webp"},
    "Bacuru and Egguru": {"income": 25, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/flzi1jBXX-CAptIqAJjRlYEiRZabV6i7l6YJSZrY2LA/https/www.mobynotifier.com/brainrots/bacuru-and-egguru?format=webp"},
    "Celestial Pegasus": {"income": 30, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp"},
    "Tictac Sahur": {"income": 15, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp"},
}

MUTATIONS = {
    "Normal": 1.0,
    "Gold": 1.25,
    "Diamond": 1.5,
    "Candy": 4.0,
    "Lava": 6.0,
    "Galaxy": 7.0,
    "Yin Yang": 7.5,
    "Radioactive": 8.5,
    "Cursed": 9.0,
    "Rainbow": 10.0,
    "Divine": 10.0,
    "Cyber": 11.0,
}

TRAITS = {
    "None": 1.0,
    "Strawberry": 8.0,
    "Meowl": 7.0,
    "Skibidi": 6.5,
    "Is Calling": 7.5,
    "Firework": 6.0,
    "Lightning": 6.0,
    "Spider": 4.5,
    "Galactic": 4.0,
}

bot_count = random.randint(11000, 17000)
last_sent = {name: 0 for name in BRAINROTS}

def format_value(value):
    if value >= 1000:
        return f"{value/1000:.2f}B"
    return f"{value:.0f}M"

def update_bot_count():
    global bot_count
    change = random.randint(-500, 500)
    bot_count += change
    if bot_count > 17000:
        bot_count = 17000
    elif bot_count < 11000:
        bot_count = 11000
    return bot_count

def get_color(value):
    if value >= 5000:
        return 0xAF52DE
    elif value >= 2000:
        return 0xFFD60A
    elif value >= 500:
        return 0x0A84FF
    return 0x8E8E93

def send_embed(brainrot, mutation, trait, final_income, target_game, bot_count):
    formatted = format_value(final_income)
    color = get_color(final_income)
    
    if final_income >= 5000:
        tier = "Peaklights"
    elif final_income >= 2000:
        tier = "Highlights"
    elif final_income >= 500:
        tier = "Midlights"
    else:
        tier = "Lowlights"
    
    name_display = brainrot["name"]
    if mutation != "Normal":
        name_display = f"{mutation} {name_display}"
    if trait != "None":
        name_display = f"{name_display} ({trait})"
    
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{name_display}** has been detected!",
        "color": color,
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {"name": "🧬 Mutation", "value": mutation, "inline": True},
            {"name": "✨ Trait", "value": trait if trait != "None" else "None", "inline": True},
            {"name": "💰 Income", "value": formatted + "/s", "inline": True},
            {"name": "🏆 Tier", "value": tier, "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
            {"name": "🎮 Teleporting To", "value": f"`{target_game}`", "inline": False},
        ],
        "footer": {"text": f"Lazy AJ • {brainrot['rarity']} Brainrot"},
    }
    
    if brainrot["image"] and brainrot["image"] != "":
        embed["thumbnail"] = {"url": brainrot["image"]}
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "Lazy AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

print("Lazy AJ Bot Started")
print(f"Monitoring {len(BRAINROTS)} brainrots")

while True:
    now = time.time()
    for name, data in BRAINROTS.items():
        interval = random.randint(45, 120)
        if now - last_sent[name] >= interval:
            mutation = random.choice(list(MUTATIONS.keys()))
            trait = random.choice(list(TRAITS.keys()))
            if random.random() < 0.7:
                trait = "None"
            
            final_income = data["income"] * MUTATIONS[mutation] * TRAITS[trait]
            final_income = final_income * (0.85 + random.random() * 0.3)
            
            target_game = random.choice(SAB_GAME_IDS)
            current_bots = update_bot_count()
            
            send_embed(
                {"name": name, "income": data["income"], "rarity": data["rarity"], "image": data["image"]},
                mutation, trait, final_income, target_game, current_bots
            )
            last_sent[name] = now
            time.sleep(random.randint(30, 90))
    time.sleep(5)
