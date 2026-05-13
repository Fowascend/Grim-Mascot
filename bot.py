import requests
import random
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

SAB_GAME_IDS = [109983668079237, 85621847059032, 99606176102979]

# ============================================================
# BRAINROT BASE INCOME (from KingVisuals ANIMAL_DATA)
# Values are in MILLIONS per second
# ============================================================
BRAINROTS = {
    # OG BRAINROTS
    "Strawberry Elephant": {"income": 750, "rarity": "OG"},
    "Meowl": {"income": 600, "rarity": "OG"},
    "Headless Horseman": {"income": 550, "rarity": "OG"},
    "Skibidi Toilet": {"income": 450, "rarity": "OG"},
    "John Pork": {"income": 500, "rarity": "OG"},
    "Griffin": {"income": 400, "rarity": "OG"},
    
    # SECRET BRAINROTS (High tier)
    "Hydra Dragon Cannelloni": {"income": 300, "rarity": "Secret"},
    "Dragon Gingerini": {"income": 350, "rarity": "Secret"},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret"},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret"},
    "Cooki and Milki": {"income": 155, "rarity": "Secret"},
    "Capitano Moby": {"income": 160, "rarity": "Secret"},
    "La Supreme Combinasion": {"income": 200, "rarity": "Secret"},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret"},
    "La Casa Boo": {"income": 100, "rarity": "Secret"},
    "Cash or Card": {"income": 100, "rarity": "Secret"},
    "La Extinct Grande": {"income": 23.5, "rarity": "Secret"},
    
    # SECRET BRAINROTS (Mid tier)
    "Garama and Madundung": {"income": 50, "rarity": "Secret"},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret"},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret"},
    "Esok Sekolah": {"income": 30, "rarity": "Secret"},
    "Spinny Hammy": {"income": 17, "rarity": "Secret"},
    "Cerberus": {"income": 175, "rarity": "Secret"},
    "Celestial Pegasus": {"income": 175, "rarity": "Secret"},
    "Los Bros": {"income": 24, "rarity": "Secret"},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret"},
    "Los Combinasionas": {"income": 15, "rarity": "Secret"},
    "Los Hotspotsitos": {"income": 20, "rarity": "Secret"},
    "Money Money Puggy": {"income": 21, "rarity": "Secret"},
    "Los Puggies": {"income": 30, "rarity": "Secret"},
    "Nuclearo Dinosauro": {"income": 15, "rarity": "Secret"},
    "Tang Tang Keletang": {"income": 33.5, "rarity": "Secret"},
    "Tictac Sahur": {"income": 37.5, "rarity": "Secret"},
    "Love Love Bear": {"income": 225, "rarity": "Secret"},
    "Foxini Lanternini": {"income": 115, "rarity": "Secret"},
    "Rosey and Teddy": {"income": 165, "rarity": "Secret"},
    "Tralaledon": {"income": 27.5, "rarity": "Secret"},
    "Spooky and Pumpky": {"income": 80, "rarity": "Secret"},
}

# ============================================================
# MUTATION MULTIPLIERS (ADDITIVE - from KingVisuals)
# Formula: final = base * (1 + mutMod + traitMod)
# ============================================================
MUTATIONS = {
    "Normal": 0.0,
    "Gold": 0.25,
    "Diamond": 0.5,
    "Bloodrot": 1.0,
    "Candy": 3.0,
    "Lava": 5.0,
    "Galaxy": 6.0,
    "Yin Yang": 6.5,
    "Radioactive": 7.5,
    "Cursed": 8.0,
    "Rainbow": 9.0,
    "Divine": 9.0,
    "Cyber": 10.0,
}

# ============================================================
# TRAIT MULTIPLIERS (ADDITIVE - from KingVisuals)
# ============================================================
TRAITS = {
    "None": 0.0,
    "Strawberry": 8.0,
    "Meowl": 7.0,
    "Is Calling": 7.5,
    "Galactic": 3.0,
    "Fireworks": 5.0,
    "Lightning": 5.0,
    "Spider": 3.5,
    "Paint": 5.0,
    "Taco": 2.0,
    "Nyan": 5.0,
    "Zombie": 4.0,
    "Claws": 4.0,
    "Glitched": 4.0,
    "Bubblegum": 3.0,
    "Fire": 5.0,
    "Wet": 1.5,
    "Snowy": 2.0,
    "Cometstruck": 2.5,
    "Explosive": 3.0,
    "Disco": 4.0,
    "10B": 3.0,
    "Shark Fin": 3.0,
    "Matteo Hat": 3.5,
    "Brazil": 5.0,
    "UFO": 2.0,
    "Skeleton": 3.0,
    "Sombrero": 4.0,
    "Tie": 3.75,
    "Witch Hat": 3.0,
    "Indonesia": 4.0,
    "Santa Hat": 4.0,
    "Reindeer Pet": 5.0,
    "Skibidi": 6.0,
    "Granny": 5.5,
    "Bunny Ears": 4.5,
}

# ============================================================
# UNOBTAINABLE BRAINROTS (only Normal mutation, very rare)
# ============================================================
UNOBTAINABLE = {
    "Dragon Gingerini": True,
    "Headless Horseman": True,
    "Spooky and Pumpky": True,
    "La Supreme Combinasion": True,
}

bot_count = random.randint(11000, 17000)
last_sent = {name: 0 for name in BRAINROTS}

def format_value(value_in_millions):
    if value_in_millions >= 1000:
        return f"{value_in_millions/1000:.2f}B"
    return f"{value_in_millions:.0f}M"

def update_bot_count():
    global bot_count
    change = random.randint(-500, 500)
    bot_count += change
    if bot_count > 17000:
        bot_count = 17000
    elif bot_count < 11000:
        bot_count = 11000
    return bot_count

def get_color(value_in_millions):
    if value_in_millions >= 5000:
        return 0xAF52DE  # Purple - Peaklights
    elif value_in_millions >= 2000:
        return 0xFFD60A  # Yellow - Highlights
    elif value_in_millions >= 500:
        return 0x0A84FF  # Blue - Midlights
    return 0x8E8E93      # Gray - Lowlights

def get_tier(value_in_millions):
    if value_in_millions >= 5000:
        return "Peaklights"
    elif value_in_millions >= 2000:
        return "Highlights"
    elif value_in_millions >= 500:
        return "Midlights"
    return "Lowlights"

def calculate_income(base_income, mutation, trait):
    """KingVisuals formula: final = base * (1 + mutMod + traitMod)"""
    mut_mod = MUTATIONS.get(mutation, 0.0)
    trait_mod = TRAITS.get(trait, 0.0)
    
    final = base_income * (1 + mut_mod + trait_mod)
    
    # Add random variance (85% to 115%)
    variance = 0.85 + (random.random() * 0.3)
    final = final * variance
    
    return final

def send_embed(name, data, mutation, trait, final_income, bot_count):
    formatted = format_value(final_income)
    color = get_color(final_income)
    tier = get_tier(final_income)
    
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
            {"name": "✨ Trait", "value": trait if trait != "None" else "None", "inline": True},
            {"name": "💰 Income", "value": f"{formatted}/s", "inline": True},
            {"name": "🏆 Tier", "value": tier, "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
        ],
        "footer": {"text": f"Lazy AJ • {data['rarity']} Brainrot"},
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "Lazy AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

print("=" * 50)
print("LAZY AJ BOT - STARTING")
print("=" * 50)
print(f"Monitoring {len(BRAINROTS)} brainrots")
print("Using KingVisuals calculation formula")
print("=" * 50)

while True:
    now = time.time()
    
    for name, data in BRAINROTS.items():
        interval = random.randint(45, 120)
        
        if now - last_sent[name] >= interval:
            is_unobtainable = UNOBTAINABLE.get(name, False)
            
            # Unobtainable brainrots: 5% chance to appear, Normal mutation only, no traits
            if is_unobtainable and random.random() > 0.05:
                continue
            
            if is_unobtainable:
                mutation = "Normal"
                trait = "None"
                final_income = data["income"]
            else:
                # Pick random mutation
                mutation_list = list(MUTATIONS.keys())
                mutation = random.choice(mutation_list)
                
                # Pick random trait (70% chance of None)
                trait_list = list(TRAITS.keys())
                trait = random.choice(trait_list)
                if random.random() < 0.7:
                    trait = "None"
                
                # Special traits for specific brainrots
                if name == "Strawberry Elephant" and random.random() < 0.05:
                    trait = "Strawberry"
                elif name == "Meowl" and random.random() < 0.05:
                    trait = "Meowl"
                
                final_income = calculate_income(data["income"], mutation, trait)
            
            current_bots = update_bot_count()
            send_embed(name, data, mutation, trait, final_income, current_bots)
            last_sent[name] = now
            
            time.sleep(random.randint(30, 90))
    
    time.sleep(5)
