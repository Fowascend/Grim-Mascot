import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

BRAINROTS = [
    {"name": "Strawberry Elephant", "income": 750, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/0/0a/Strawberry_Elephant.png"},
    {"name": "Meowl", "income": 600, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/8/8a/Meowl.png"},
    {"name": "Headless Horseman", "income": 550, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Headless_Horseman.png"},
    {"name": "Skibidi Toilet", "income": 450, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png"},
    {"name": "John Pork", "income": 500, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/4/44/John_Pork.png"},
    {"name": "Griffin", "income": 400, "rarity": "OG", "rarity_value": 4, "image": "https://static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png"},
    {"name": "Hydra Dragon Cannelloni", "income": 300, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/b/b7/Dragon_Cannelloni.png"},
    {"name": "Dragon Gingerini", "income": 350, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/3/3c/Dragon_Gingerini.png"},
    {"name": "Dragon Cannelloni", "income": 250, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/b/b7/Dragon_Cannelloni.png"},
    {"name": "Burguro And Fryuro", "income": 150, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/9/94/Burguro_And_Fryuro.png"},
    {"name": "Cooki and Milki", "income": 155, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/f/f4/Cooki_and_Milki.png"},
    {"name": "Capitano Moby", "income": 160, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/e/ef/Moby.png"},
    {"name": "Love Love Bear", "income": 225, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png"},
    {"name": "Cerberus", "income": 175, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/4/44/Cerberus.png"},
    {"name": "Celestial Pegasus", "income": 175, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/3/3c/Celestial_Pegasus.png"},
    {"name": "La Supreme Combinasion", "income": 200, "rarity": "Secret", "rarity_value": 3, "image": "https://static.wikia.nocookie.net/stealabr/images/5/52/SupremeCombinasion.png"},
    {"name": "Fragrama and Chocrama", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png"},
    {"name": "La Casa Boo", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/d/de/Casa_Booo.png"},
    {"name": "Cash or Card", "income": 100, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png"},
    {"name": "Garama and Madundung", "income": 50, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/e/ee/Garamadundung.png"},
    {"name": "Ketchuru and Masturu", "income": 42.5, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/5/5a/Ketchuru_and_Masturu.png"},
    {"name": "Spaghetti Tualetti", "income": 60, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/a/a8/Spaghetti_Tualetti.png"},
    {"name": "Esok Sekolah", "income": 30, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/3/32/Esok_Sekolah.png"},
    {"name": "Los Bros", "income": 24, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/4/4d/Ketupat_Bros.png"},
    {"name": "Ketupat Kepat", "income": 35, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/4/4d/Ketupat_Bros.png"},
    {"name": "Tang Tang Keletang", "income": 33.5, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/8/88/Tang_Tang_Keletang.png"},
    {"name": "Tictac Sahur", "income": 37.5, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/b/b6/Tictac_Sahur.png"},
    {"name": "Foxini Lanternini", "income": 115, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/4/41/Foxini_Lanternini.png"},
    {"name": "Rosey and Teddy", "income": 165, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Rosey_and_Teddy.png"},
    {"name": "Tralaledon", "income": 27.5, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/7/79/Brr_Brr_Patapem.png"},
    {"name": "Spooky and Pumpky", "income": 80, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/d/d6/Spookypumpky.png"},
    {"name": "La Extinct Grande", "income": 23.5, "rarity": "Secret", "rarity_value": 2, "image": "https://static.wikia.nocookie.net/stealabr/images/1/1f/La_Extinct_Grande.png"},
    {"name": "Los Combinasionas", "income": 15, "rarity": "Secret", "rarity_value": 1, "image": "https://static.wikia.nocookie.net/stealabr/images/1/13/Los_Combinasionas.png"},
    {"name": "Los Hotspotsitos", "income": 20, "rarity": "Secret", "rarity_value": 1, "image": "https://static.wikia.nocookie.net/stealabr/images/3/33/Los_Hotspotsitos.png"},
    {"name": "Money Money Puggy", "income": 21, "rarity": "Secret", "rarity_value": 1, "image": "https://static.wikia.nocookie.net/stealabr/images/6/67/Money_Money_Puggy.png"},
    {"name": "Los Puggies", "income": 30, "rarity": "Secret", "rarity_value": 1, "image": "https://static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png"},
    {"name": "Nuclearo Dinosauro", "income": 15, "rarity": "Secret", "rarity_value": 1, "image": "https://static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png"},
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
        "original_name": brainrot["name"],
        "income": final_income,
        "formatted_income": format_income(final_income),
        "tier": tier,
        "color": color,
        "mutation": mutation["name"],
        "trait": trait["name"],
        "rarity": brainrot["rarity"],
        "rarity_value": brainrot["rarity_value"],
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
print("Logs every 30-60 seconds")
print("OG brainrots every 4 hours")
print("With images from wiki")
print("=" * 50)

while True:
    now = time.time()
    is_og_time = (now - last_og_time) >= 14400
    
    if is_og_time:
        interval = 1
        last_og_time = now
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
                "original_name": selected["name"],
                "income": selected["income"],
                "formatted_income": format_income(selected["income"]),
                "tier": get_tier(selected["income"]),
                "color": get_color(selected["income"]),
                "mutation": "Normal",
                "trait": "None",
                "rarity": selected["rarity"],
                "rarity_value": selected["rarity_value"],
                "image": selected["image"],
                "timestamp": datetime.now().isoformat(),
            }
    else:
        brainrot = get_random_brainrot()
    
    if brainrot:
        current_bots = update_bot_count()
        send_embed(brainrot, current_bots)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {brainrot['name']} | {brainrot['formatted_income']}/s | {brainrot['tier']}")
