import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

BRAINROTS = [
    {"name": "Strawberry Elephant", "income": 750, "rarity": "OG", "rarity_value": 4, "image": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp"},
    {"name": "Meowl", "income": 600, "rarity": "OG", "rarity_value": 4, "image": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp"},
    {"name": "Headless Horseman", "income": 550, "rarity": "OG", "rarity_value": 4, "image": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp"},
    {"name": "Skibidi Toilet", "income": 450, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png"},
    {"name": "John Pork", "income": 500, "rarity": "OG", "rarity_value": 4, "image": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp"},
    {"name": "Griffin", "income": 400, "rarity": "OG", "rarity_value": 4, "image": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp"},
    
    {"name": "Dragon Cannelloni", "income": 250, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp"},
    {"name": "Burguro And Fryuro", "income": 150, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp"},
    {"name": "Capitano Moby", "income": 160, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp"},
    {"name": "Love Love Bear", "income": 225, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png"},
    {"name": "Cerberus", "income": 175, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp"},
    {"name": "Celestial Pegasus", "income": 175, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp"},
    {"name": "La Supreme Combinasion", "income": 200, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/KQBRtzBT3aoWc6WTjvoOhl2Tf64FvbWhyFW4VWbQGhQ/https/www.mobynotifier.com/brainrots/la-secret-combinasion?format=webp"},
    {"name": "Fragrama and Chocrama", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png/revision/latest?format=webp"},
    {"name": "La Casa Boo", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/quqyy1a6ddzWi8EeljigfhNgezGLFYhD2LpWiSRMu4g/%3Fcb%3D20260505011532/https/static.wikia.nocookie.net/stealabr/images/d/de/Casa_Booo.png/revision/latest?format=webp"},
    {"name": "Cash or Card", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/3--q-u9qc6iESRoNzi3nj5F8aOR0ThZ_FvPHINXrBw4/%3Fcb%3D20260428161300/https/static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png/revision/latest/scale-to-width-down/1000?format=webp"},
    {"name": "Garama and Madundung", "income": 50, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp"},
    {"name": "Ketchuru and Masturu", "income": 42.5, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp"},
    {"name": "Spaghetti Tualetti", "income": 60, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/yoOCxZMRDwqYzFcsYPY5GX2WY2wK4FvGgqB72P1VCV8/https/www.mobynotifier.com/brainrots/spaghetti-tualetti?format=webp"},
    {"name": "Esok Sekolah", "income": 30, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp"},
    {"name": "La Extinct Grande", "income": 23.5, "rarity": "Secret", "rarity_value": 2, "image": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE"},
    {"name": "Los Bros", "income": 24, "rarity": "Secret", "rarity_value": 2, "image": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png"},
    {"name": "Ketupat Kepat", "income": 35, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp"},
    {"name": "Tang Tang Keletang", "income": 33.5, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/4qWYUdmCoa0zhqxH2MKwV7Or5U9Xif8yw-AB_Gy5Lig/https/www.mobynotifier.com/brainrots/tang-tang-keletang?format=webp"},
    {"name": "Tictac Sahur", "income": 37.5, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp"},
    {"name": "Foxini Lanternini", "income": 115, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/4/41/Foxini_Lanternini.png"},
    {"name": "Rosey and Teddy", "income": 165, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Rosey_and_Teddy.png"},
    {"name": "Tralaledon", "income": 27.5, "rarity": "Secret", "rarity_value": 2, "image": "https://images-ext-1.discordapp.net/external/_bBDdfMFPbTdCGnkfiz3yzvtNwqz0P4iVOnTlxFfaME/%3Fcb%3D20250909171639/https/static.wikia.nocookie.net/stealabr/images/7/79/Brr_Brr_Patapem.png/revision/latest?format=webp"},
    {"name": "Spooky and Pumpky", "income": 80, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/d/d6/Spookypumpky.png/revision/latest?cb=20251012023638"},
    {"name": "Los Combinasionas", "income": 15, "rarity": "Secret", "rarity_value": 1, "image": "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp"},
    {"name": "Los Hotspotsitos", "income": 20, "rarity": "Secret", "rarity_value": 1, "image": "https://images-ext-1.discordapp.net/external/MsbU8Cx2x5x0Uqz0KiKgYQXeugojQ7SQBjg0uY8Doh0/%3Fcb%3D20251226204212/https/static.wikia.nocookie.net/stealabr/images/6/69/Loshotspotsitos.png/revision/latest?format=webp"},
    {"name": "Money Money Puggy", "income": 21, "rarity": "Secret", "rarity_value": 1, "image": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter?format=webp"},
    {"name": "Los Puggies", "income": 30, "rarity": "Secret", "rarity_value": 1, "image": "https://images-ext-1.discordapp.net/external/xSRo3cOgaMz_3bOvc-uxwnvdHvBbEI91-5o129qDE1A/%3Fcb%3D20251109012744/https/static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png/revision/latest?format=webp"},
    {"name": "Nuclearo Dinosauro", "income": 15, "rarity": "Secret", "rarity_value": 1, "image": "https://images-ext-1.discordapp.net/external/wO_VfzWxp76PImVCn4peFiARwLyzlEbzI8SqaKEtXio/%3Fcb%3D20260328003025/https/static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png/revision/latest/scale-to-width-down/1000?format=webp"},
    {"name": "Hydra Dragon Cannelloni", "income": 300, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/xfvoBJm_MpWzP2D-q90AcpQ4EJnYcfyV763moAfMtYc/https/steal-a-brainrot.wiki/wp-content/uploads/2026/01/Steal-A-Brainrot-Wiki-HYDRA-DRAGON-Icon-.png?format=webp"},
    {"name": "Dragon Gingerini", "income": 350, "rarity": "Secret", "rarity_value": 3, "image": "https://images-ext-1.discordapp.net/external/3puIUz4htLMUuD3hL5u4N9tIlLdxj2Gi2AVuJgtei9o/https/freebrainrots.com/assets/images/brainrots/roitems/dragon-gingerini.png?format=webp"},
    {"name": "Cooki and Milki", "income": 155, "rarity": "Secret", "rarity_value": 3, "image": "https://steal-a-brainrot.wiki/wp-content/uploads/2025/11/Steal-a-Brainrot-Wiki-Cooki-and-Milki-Icon-300x300.png"},
]

MUTATIONS = [
    {"name": "Normal", "mod": 0.0, "chance": 60},
    {"name": "Gold", "mod": 0.25, "chance": 15},
    {"name": "Diamond", "mod": 0.5, "chance": 10},
    {"name": "Candy", "mod": 3.0, "chance": 3},
    {"name": "Lava", "mod": 5.0, "chance": 3},
    {"name": "Galaxy", "mod": 6.0, "chance": 3},
    {"name": "Yin Yang", "mod": 6.5, "chance": 2},
    {"name": "Radioactive", "mod": 7.5, "chance": 1.5},
    {"name": "Cursed", "mod": 8.0, "chance": 1},
    {"name": "Rainbow", "mod": 9.0, "chance": 0.8},
    {"name": "Divine", "mod": 9.0, "chance": 0.8},
    {"name": "Cyber", "mod": 10.0, "chance": 0.5},
]

TRAITS = [
    {"name": "None", "mod": 0.0, "chance": 85},
    {"name": "Strawberry", "mod": 8.0, "chance": 3},
    {"name": "Meowl", "mod": 7.0, "chance": 3},
    {"name": "Is Calling", "mod": 7.5, "chance": 1},
    {"name": "Galactic", "mod": 3.0, "chance": 2},
    {"name": "Fireworks", "mod": 5.0, "chance": 2},
    {"name": "Lightning", "mod": 5.0, "chance": 2},
    {"name": "Spider", "mod": 3.5, "chance": 2},
]

UNOBTAINABLE = ["Dragon Gingerini", "Headless Horseman", "Spooky and Pumpky"]

def weighted_choice(items):
    total = sum(item.get("chance", 1) for item in items)
    r = random.random() * total
    accum = 0
    for item in items:
        accum += item.get("chance", 1)
        if r <= accum:
            return item
    return items[0]

def format_income(value):
    if value >= 1000:
        return f"{value/1000:.2f}B"
    return f"{value:.0f}M"

def get_tier(value):
    if value >= 5000:
        return "Peaklights"
    elif value >= 2000:
        return "Highlights"
    elif value >= 500:
        return "Midlights"
    return "Lowlights"

def get_color(value):
    if value >= 5000:
        return 0xAF52DE
    elif value >= 2000:
        return 0xFFD60A
    elif value >= 500:
        return 0x0A84FF
    return 0x8E8E93

def calculate_income(base_income, mutation, trait):
    if mutation["name"] == "Normal" and trait["name"] == "None":
        return base_income
    return base_income * (1 + mutation["mod"] + trait["mod"])

def get_random_brainrot():
    brainrot = random.choice(BRAINROTS)
    
    if brainrot["name"] in UNOBTAINABLE and random.random() > 0.03:
        return None
    
    if brainrot["rarity_value"] == 4:
        mutation = {"name": "Normal", "mod": 0.0}
        trait = {"name": "None", "mod": 0.0}
    else:
        mutation = weighted_choice(MUTATIONS)
        trait = weighted_choice(TRAITS)
    
    final_income = calculate_income(brainrot["income"], mutation, trait)
    tier = get_tier(final_income)
    color = get_color(final_income)
    
    display_name = brainrot["name"]
    if mutation["name"] != "Normal":
        display_name = f"{mutation['name']} {display_name}"
    if trait["name"] != "None":
        display_name = f"{display_name} ({trait['name']})"
    
    return {
        "name": display_name,
        "income": final_income,
        "formatted_income": format_income(final_income),
        "tier": tier,
        "color": color,
        "mutation": mutation["name"],
        "trait": trait["name"],
        "rarity": brainrot["rarity"],
        "image": brainrot["image"],
        "timestamp": datetime.now().isoformat(),
    }

def send_embed(brainrot, bot_count):
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{brainrot['name']}** has been detected!",
        "color": brainrot["color"],
        "timestamp": brainrot["timestamp"],
        "thumbnail": {"url": brainrot["image"]},
        "fields": [
            {"name": "🧬 Mutation", "value": brainrot["mutation"], "inline": True},
            {"name": "✨ Trait", "value": brainrot["trait"], "inline": True},
            {"name": "💰 Income", "value": f"{brainrot['formatted_income']}/s", "inline": True},
            {"name": "🏆 Tier", "value": brainrot["tier"], "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
        ],
        "footer": {"text": f"Lazy AJ • {brainrot['rarity']} Brainrot"},
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "Lazy AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

bot_count = random.randint(11000, 17000)
last_og_time = time.time()
next_og_interval = random.randint(14400, 21600)

def update_bot_count():
    global bot_count
    change = random.randint(-500, 500)
    bot_count += change
    if bot_count > 17000:
        bot_count = 17000
    elif bot_count < 11000:
        bot_count = 11000
    return bot_count

print("=" * 50)
print("LAZY AJ BOT - STARTING")
print("=" * 50)
print(f"Monitoring {len(BRAINROTS)} brainrots")
print("Normal logs: 30-60 seconds")
print("OG logs: 4-6 hours (random)")
print("=" * 50)

while True:
    now = time.time()
    is_og_time = (now - last_og_time) >= next_og_interval
    
    if is_og_time:
        interval = 1
        last_og_time = now
        next_og_interval = random.randint(14400, 21600)
    else:
        interval = random.randint(30, 60)
    
    time.sleep(interval)
    
    brainrot = None
    
    if is_og_time:
        og_brainrots = [b for b in BRAINROTS if b["rarity"] == "OG"]
        if og_brainrots:
            selected = random.choice(og_brainrots)
            brainrot = {
                "name": selected["name"],
                "income": selected["income"],
                "formatted_income": format_income(selected["income"]),
                "tier": get_tier(selected["income"]),
                "color": get_color(selected["income"]),
                "mutation": "Normal",
                "trait": "None",
                "rarity": selected["rarity"],
                "image": selected["image"],
                "timestamp": datetime.now().isoformat(),
            }
    else:
        brainrot = get_random_brainrot()
    
    if brainrot:
        current_bots = update_bot_count()
        send_embed(brainrot, current_bots)
        time_remaining = next_og_interval - (time.time() - last_og_time)
        hours_remaining = int(time_remaining // 3600)
        mins_remaining = int((time_remaining % 3600) // 60)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {brainrot['name']} | {brainrot['formatted_income']}/s")
        if is_og_time:
            print(f"Next OG log in: {next_og_interval//3600}h {next_og_interval%3600//60}m (randomized)")
