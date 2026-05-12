import requests
import random
import time
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# SAB Game IDs
SAB_GAME_IDS = [109983668079237, 85621847059032, 99606176102979]

# Brainrot list with base values (in MILLIONS)
BRAINROTS = {
    "Dragon Cannelloni": 250,
    "Strawberry Elephant": 750,
    "Meowl": 650,
    "Skibidi Toilet": 450,
    "Headless Horseman": 550,
    "Burguro And Fryuro": 2475,
    "Garama and Madundung": 50,
    "Sammyni Fattini": 70,
    "Frograma & Chocrama": 100,
    "Capitano Moby": 165,
    "Hydra Bunny": 185,
    "Ketchuru & Masturu": 200,
    "Los Chicleteiras": 150,
    "Noo My Eggs": 120,
    "Money Money Puggy": 75,
    "Los Bunitos": 95,
    "Los Burritos": 110,
    "Esok Sekolah": 55,
    "Los Mi Gatitos": 85,
    "Quesadillo Vampiro": 180,
    "Spinny Hammy": 90,
    "Burrito Bandito": 110,
    "Granny": 60,
    "Cash or Card": 500,
    "Cigno Fulgoro": 210,
    "La T": 180,
    "Noo My Gold": 60,
}

# Mutation multipliers
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

# Trait multipliers
TRAITS = {
    "None": 1.0,
    "Strawberry": 8.0,
    "Meowl": 7.0,
    "Skibidi": 6.5,
    "Firework": 6.0,
    "Lightning": 6.0,
    "Spider": 4.5,
    "Galactic": 4.0,
    "Crab Rave": 4.0,
    "Bubblegum": 4.0,
    "Extinct": 4.0,
}

last_sent = {name: 0 for name in BRAINROTS}
bot_count = random.randint(11000, 17000)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def format_value(value_in_millions):
    """Format value to B (billions) or M (millions)"""
    if value_in_millions >= 1000:
        return f"{value_in_millions/1000:.2f}B"
    return f"{value_in_millions:.0f}M"

def calculate_price(base_value, mutation, trait):
    """Calculate final price with multipliers"""
    mutation_mult = MUTATIONS.get(mutation, 1.0)
    trait_mult = TRAITS.get(trait, 1.0)
    
    final_value = base_value * mutation_mult * trait_mult
    
    # Add random variance (85% to 115%)
    variance = 0.85 + (random.random() * 0.3)
    final_value = final_value * variance
    
    return final_value

def get_color_from_value(value):
    """Get embed color based on value"""
    if value >= 5000:
        return 0xFF0000  # Red - Peaklights
    elif value >= 2000:
        return 0xFF6600  # Orange - Highlights
    elif value >= 500:
        return 0xFFFF00  # Yellow - Midlights
    else:
        return 0x00FF00  # Green - Lowlights

def get_tier_from_value(value):
    """Get tier name based on value"""
    if value >= 5000:
        return "Peaklights"
    elif value >= 2000:
        return "Highlights"
    elif value >= 500:
        return "Midlights"
    else:
        return "Lowlights"

def update_bot_count():
    global bot_count
    # Fluctuate between 11000 and 17000
    change = random.randint(-500, 500)
    bot_count = bot_count + change
    if bot_count > 17000:
        bot_count = 17000
    elif bot_count < 11000:
        bot_count = 11000
    return bot_count

# ============================================================
# SEND EMBED FUNCTION
# ============================================================
def send_embed(title, description, fields, color, footer=None):
    """Send a Discord embed"""
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.now().isoformat(),
        "fields": fields
    }
    
    if footer:
        embed["footer"] = {"text": footer}
    
    data = {"embeds": [embed], "username": "Lazy AJ"}
    
    try:
        requests.post(WEBHOOK_URL, json=data)
        return True
    except Exception as e:
        print(f"Webhook error: {e}")
        return False

# ============================================================
# SEND DETECTION
# ============================================================
def send_detection(name, mutation, trait, value, target_game):
    tier = get_tier_from_value(value)
    formatted_value = format_value(value)
    color = get_color_from_value(value)
    current_bots = update_bot_count()
    
    fields = [
        {"name": "🧬 Mutation", "value": mutation, "inline": True},
        {"name": "✨ Trait", "value": trait, "inline": True},
        {"name": "💰 Value", "value": formatted_value, "inline": True},
        {"name": "🏆 Tier", "value": tier, "inline": True},
        {"name": "🤖 Active Bots", "value": f"{current_bots:,}", "inline": True},
        {"name": "🎮 Teleporting To", "value": f"`{target_game}`", "inline": False},
    ]
    
    send_embed(
        title=f"🎯 NEW BRAINROT DETECTED",
        description=f"**{name}** has been detected!",
        fields=fields,
        color=color,
        footer="Lazy AJ • Auto Join Enabled"
    )
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} | {mutation} | {trait} | {formatted_value} | Bots: {current_bots:,}")

# ============================================================
# SEND STATUS
# ============================================================
def send_status():
    current_bots = update_bot_count()
    
    fields = [
        {"name": "🤖 Active Bots", "value": f"{current_bots:,}", "inline": True},
        {"name": "🎮 Active Games", "value": str(len(SAB_GAME_IDS)), "inline": True},
        {"name": "🧠 Brainrots", "value": str(len(BRAINROTS)), "inline": True},
        {"name": "🟢 VPS Status", "value": "CONNECTED", "inline": True},
    ]
    
    send_embed(
        title="🟢 LAZY AJ STATUS",
        description="Bot is online and monitoring for brainrots!",
        fields=fields,
        color=0x00FF00,
        footer="Lazy AJ • 24/7 Monitoring"
    )

# ============================================================
# MAIN LOOP
# ============================================================
print("=" * 50)
print("LAZY AJ BOT - STARTING")
print("=" * 50)
print(f"Webhook: {WEBHOOK_URL[:50]}...")
print(f"Monitoring {len(BRAINROTS)} brainrots")
print(f"SAB Game IDs: {SAB_GAME_IDS}")
print("=" * 50)

# Send startup status
send_status()

while True:
    now = time.time()
    
    for name, base_value in BRAINROTS.items():
        interval = random.randint(45, 120)
        
        if now - last_sent[name] >= interval:
            mutation = random.choice(list(MUTATIONS.keys()))
            trait = random.choice(list(TRAITS.keys()))
            
            if random.random() < 0.7:
                trait = "None"
            
            price = calculate_price(base_value, mutation, trait)
            target_game = random.choice(SAB_GAME_IDS)
            
            if mutation == "Normal":
                full_name = name
            else:
                full_name = f"{mutation} {name}"
            
            send_detection(full_name, mutation, trait, price, target_game)
            last_sent[name] = now
            
            time.sleep(random.randint(30, 90))
    
    time.sleep(5)
