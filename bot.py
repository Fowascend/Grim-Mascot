import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

MUTATION_MULTIPLIERS = {
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
    "Is Calling": 7.5,
}

UNOBTAINABLE = {
    "Dragon Gingerini": True,
    "Headless Horseman": True,
    "Spooky and Pumpky": True,
    "La Supreme Combinasion": True,
}

BRAINROTS = {
    "Strawberry Elephant": {"income": 750, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp"},
    "Meowl": {"income": 600, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp"},
    "Headless Horseman": {"income": 550, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp"},
    "Skibidi Toilet": {"income": 450, "rarity": "OG", "image": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png/revision/latest?cb=20251227221221"},
    "John Pork": {"income": 500, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp"},
    "Griffin": {"income": 400, "rarity": "OG", "image": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp"},
    "Hydra Dragon Cannelloni": {"income": 350, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/xfvoBJm_MpWzP2D-q90AcpQ4EJnYcfyV763moAfMtYc/https/steal-a-brainrot.wiki/wp-content/uploads/2026/01/Steal-A-Brainrot-Wiki-HYDRA-DRAGON-Icon-.png?format=webp"},
    "Dragon Gingerini": {"income": 225, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/3puIUz4htLMUuD3hL5u4N9tIlLdxj2Gi2AVuJgtei9o/https/freebrainrots.com/assets/images/brainrots/roitems/dragon-gingerini.png?format=webp"},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp"},
    "La Supreme Combinasion": {"income": 200, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/stealabr/images/5/52/SupremeCombinasion.png/revision/latest?cb=20250825130920"},
    "Spooky and Pumpky": {"income": 80, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/stealabr/images/d/d6/Spookypumpky.png/revision/latest?cb=20251012023638"},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp"},
    "Cooki and Milki": {"income": 155, "rarity": "Secret", "image": "https://steal-a-brainrot.wiki/wp-content/uploads/2025/11/Steal-a-Brainrot-Wiki-Cooki-and-Milki-Icon-300x300.png"},
    "Capitano Moby": {"income": 160, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/stealabr/images/e/ef/Moby.png/revision/latest?cb=20251101185416"},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png/revision/latest?format=webp"},
    "La Casa Boo": {"income": 100, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/quqyy1a6ddzWi8EeljigfhNgezGLFYhD2LpWiSRMu4g/%3Fcb%3D20260505011532/https/static.wikia.nocookie.net/stealabr/images/d/de/Casa_Booo.png/revision/latest?format=webp"},
    "Cash or Card": {"income": 100, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/3--q-u9qc6iESRoNzi3nj5F8aOR0ThZ_FvPHINXrBw4/%3Fcb%3D20260428161300/https/static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png/revision/latest/scale-to-width-down/1000?format=webp"},
    "Garama and Madundung": {"income": 50, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/stealabr/images/e/ee/Garamadundung.png/revision/latest?cb=20250816022557"},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp"},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/yoOCxZMRDwqYzFcsYPY5GX2WY2wK4FvGgqB72P1VCV8/https/www.mobynotifier.com/brainrots/spaghetti-tualetti?format=webp"},
    "Esok Sekolah": {"income": 30, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp"},
    "Spinny Hammy": {"income": 90, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/BoWX4KUkY2KLFTf2mUHpMH1tDNo2PRIq19ICSrGuRo8/https/www.mobynotifier.com/brainrots/spinny-hammy?format=webp"},
    "Cerberus": {"income": 26, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp"},
    "Celestial Pegasus": {"income": 30, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp"},
    "Los Bros": {"income": 37.5, "rarity": "Secret", "image": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png?ex=6a04f472&is=6a03a2f2&hm=4d0c65bd50abea97f206777f3b11fbc785460fcad55fa0722d80df53fd028beb&=&format=webp"},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp"},
    "Los Combinasionas": {"income": 15, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp"},
    "Los Hotspotsitos": {"income": 25, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/MsbU8Cx2x5x0Uqz0KiKgYQXeugojQ7SQBjg0uY8Doh0/%3Fcb%3D20251226204212/https/static.wikia.nocookie.net/stealabr/images/6/69/Loshotspotsitos.png/revision/latest?format=webp"},
    "Money Money Puggy": {"income": 21, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter?format=webp"},
    "Los Puggies": {"income": 30, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/xSRo3cOgaMz_3bOvc-uxwnvdHvBbEI91-5o129qDE1A/%3Fcb%3D20251109012744/https/static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png/revision/latest?format=webp"},
    "Nuclearo Dinosauro": {"income": 15, "rarity": "Secret", "image": "https://images-ext-1.discordapp.net/external/wO_VfzWxp76PImVCn4peFiARwLyzlEbzI8SqaKEtXio/%3Fcb%3D20260328003025/https/static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png/revision/latest/scale-to-width-down/1000?format=webp"},
    "La Extinct Grande": {"income": 100, "rarity": "Secret", "image": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE"},
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

def send_embed(name, data, mutation, trait, final_income, bot_count):
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
    
    display_name = name
    if mutation != "Normal":
        display_name = f"{mutation} {display_name}"
    if trait != "None":
        display_name = f"{display_name} ({trait})"
    
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{display_name}** has been detected!",
        "color": color,
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {"name": "🧬 Mutation", "value": mutation, "inline": True},
            {"name": "✨ Trait", "value": trait, "inline": True},
            {"name": "💰 Income", "value": f"{formatted}/s", "inline": True},
            {"name": "🏆 Tier", "value": tier, "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
        ],
        "footer": {"text": f"Lazy AJ • {data['rarity']} Brainrot"},
    }
    
    if data.get("image") and data["image"]:
        embed["thumbnail"] = {"url": data["image"]}
    
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
        interval = random.randint(60, 180)
        if now - last_sent[name] >= interval:
            is_unobtainable = UNOBTAINABLE.get(name, False)
            
            if is_unobtainable and random.random() > 0.03:
                continue
            
            if is_unobtainable:
                mutation = "Normal"
                trait = "None"
            else:
                mutation = random.choice(list(MUTATION_MULTIPLIERS.keys()))
                trait = "None"
                if random.random() < 0.05:
                    if name == "Strawberry Elephant":
                        trait = "Strawberry"
                    elif name == "Meowl":
                        trait = "Meowl"
                    elif random.random() < 0.03:
                        trait = "Is Calling"
            
            if is_unobtainable:
                final_income = data["income"]
            else:
                final_income = data["income"] * MUTATION_MULTIPLIERS[mutation] * TRAITS[trait]
                final_income = final_income * (0.85 + random.random() * 0.3)
            
            current_bots = update_bot_count()
            send_embed(name, data, mutation, trait, final_income, current_bots)
            last_sent[name] = now
            
            time.sleep(random.randint(30, 90))
    time.sleep(5)
