import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

SAB_GAME_IDS = [109983668079237, 85621847059032, 99606176102979]

BRAINROTS = {
    "Strawberry Elephant": {"income": 750, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/0/0a/Strawberry_Elephant.png"},
    "Meowl": {"income": 600, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/8/8a/Meowl.png"},
    "Headless Horseman": {"income": 550, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/9/9b/Headless_Horseman.png"},
    "Skibidi Toilet": {"income": 450, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/e/ed/Skibidi_Toilet.png"},
    "John Pork": {"income": 500, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/4/44/John_Pork.png"},
    "Griffin": {"income": 400, "rarity": "OG", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/3/3c/Griffin.png"},
    "Los Nooo My Hotspotsitos": {"income": 150, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/1/1e/Los_Nooo_My_Hotspotsitos.png"},
    "Los Chicleteiras": {"income": 150, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/4/4e/Los_Chicleteiras.png"},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/9/94/Burguro_And_Fryuro.png"},
    "Cooki and Milki": {"income": 155, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/f/f4/Cooki_and_Milki.png"},
    "Dragon Cannelloni": {"income": 100, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/b/b7/Dragon_Cannelloni.png"},
    "Los Hotspotsitos": {"income": 25, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/3/33/Los_Hotspotsitos.png"},
    "La Supreme Combinasion": {"income": 40, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/c/c5/La_Supreme_Combinasion.png"},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/5/5a/Ketchuru_and_Masturu.png"},
    "Garama and Madundung": {"income": 50, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/a/a5/Garama_and_Madundung.png"},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/a/a8/Spaghetti_Tualetti.png"},
    "Cash or Card": {"income": 100, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/8/89/Cash_or_Card.png"},
    "Money Money Puggy": {"income": 21, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/6/67/Money_Money_Puggy.png"},
    "Esok Sekolah": {"income": 30, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/3/32/Esok_Sekolah.png"},
    "La Casa Boo": {"income": 100, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/1/13/La_Casa_Boo.png"},
    "Spooky and Pumpky": {"income": 80, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/8/8a/Spooky_and_Pumpky.png"},
    "Eviledon": {"income": 31.5, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/0/05/Eviledon.png"},
    "Mieteteira Bicicleteira": {"income": 26, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/1/1e/Mieteteira_Bicicleteira.png"},
    "La Spooky Grande": {"income": 24.5, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/e/e5/La_Spooky_Grande.png"},
    "Cigno Fulgoro": {"income": 20, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/7/74/Cigno_Fulgoro.png"},
    "Dragon Gingerini": {"income": 225, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/3/3c/Dragon_Gingerini.png"},
    "Hydra Dragon Cannelloni": {"income": 350, "rarity": "Secret", "image": "https://static.wikia.nocookie.net/steal-a-brainrot/images/b/b7/Dragon_Cannelloni.png"},
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
    "Firework": 6.0,
    "Lightning": 6.0,
    "Is Calling": 7.5,
    "Spider": 4.5,
    "Galactic": 4.0,
}

bot_count = random.randint(11000, 17000)

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
        return 0xFF0000
    elif value >= 2000:
        return 0xFF6600
    elif value >= 500:
        return 0xFFFF00
    return 0x00FF00

def send_embed(brainrot, mutation, trait, final_income, target_game, bot_count):
    mutation_mult = MUTATIONS.get(mutation, 1.0)
    trait_mult = TRAITS.get(trait, 1.0)
    formatted_income = format_value(final_income)
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
        "thumbnail": {"url": brainrot["image"]},
        "fields": [
            {"name": "🧬 Mutation", "value": mutation, "inline": True},
            {"name": "✨ Trait", "value": trait if trait != "None" else "None", "inline": True},
            {"name": "💰 Income", "value": formatted_income + "/s", "inline": True},
            {"name": "🏆 Tier", "value": tier, "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
            {"name": "🎮 Teleporting To", "value": f"`{target_game}`", "inline": False},
        ],
        "footer": {"text": f"Lazy AJ • {brainrot['rarity']} Brainrot"},
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "Lazy AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

last_sent = {name: 0 for name in BRAINROTS}

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
