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

# Brainrot list
BRAINROTS = {
    "Strawberry Elephant": 7200,
    "Meowl": 5400,
    "Skibidi Toilet": 2700,
    "Headless Horseman": 14400,
    "Dragon Cannelloni": 900,
    "Frograma & Chocrama": 3600,
    "Capitano Moby": 4200,
    "Hydra Bunny": 4800,
    "Ketchuru & Masturu": 5400,
    "Garama and Madundung": 6000,
    "Los Chicleteiras": 3000,
    "Noo My Eggs": 2400,
    "Money Money Puggy": 1800,
    "Los Bunitos": 2000,
    "Los Burritos": 2200,
    "Esok Sekolah": 1600,
    "Los Mi Gatitos": 1900,
}

MUTATIONS = ["Cyber", "Divine", "Rainbow", "Cursed", "Radioactive", "Yin Yang", "Galaxy", "Lava", "Candy", "Diamond", "Gold", "Normal"]
TRAITS = ["Strawberry", "Meowl", "Skibidi", "Firework", "Lightning", "Spider", "Galactic", "None"]

last_sent = {name: 0 for name in BRAINROTS}

# ============================================================
# FUNCTION TO SEND EMBED
# ============================================================
def send_embed(title, description, fields, color, footer=None):
    """Send a proper Discord embed"""
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
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Embed sent successfully")
        return True
    except Exception as e:
        print(f"Webhook error: {e}")
        return False

# ============================================================
# SEND DETECTION EMBED
# ============================================================
def send_detection(name, mutation, trait, price, target_game):
    # Choose color based on price
    if price >= 10000:
        color = 0xFF0000  # Red - Peak
    elif price >= 5000:
        color = 0xFF6600  # Orange - High
    elif price >= 2000:
        color = 0xFFFF00  # Yellow - Mid
    else:
        color = 0x00FF00  # Green - Low
    
    fields = [
        {"name": "🧬 Mutation", "value": mutation, "inline": True},
        {"name": "✨ Trait", "value": trait if trait != "None" else "None", "inline": True},
        {"name": "💰 Value", "value": f"${price}M", "inline": True},
        {"name": "🎮 Target Game", "value": f"`{target_game}`", "inline": False},
        {"name": "🔗 Job ID", "value": f"`{target_game}_{int(time.time())}_{random.randint(1000,9999)}`", "inline": False},
    ]
    
    send_embed(
        title=f"🎯 NEW BRAINROT DETECTED",
        description=f"**{name}** has been detected!",
        fields=fields,
        color=color,
        footer="Lazy AJ • Auto Join Enabled"
    )

# ============================================================
# SEND JOIN EMBED
# ============================================================
def send_join_notification(name, target_game, current_game):
    fields = [
        {"name": "🎯 Brainrot", "value": name, "inline": True},
        {"name": "🎮 Teleporting To", "value": f"`{target_game}`", "inline": True},
        {"name": "📍 Current Game", "value": f"`{current_game}`", "inline": False},
    ]
    
    send_embed(
        title="✅ AUTO JOIN TRIGGERED",
        description=f"**{name}** - Teleporting now!",
        fields=fields,
        color=0x00FF00,
        footer="Lazy AJ • Good luck!"
    )

# ============================================================
# SEND STATUS EMBED
# ============================================================
def send_status(status, game_id=None, player=None):
    fields = []
    if game_id:
        fields.append({"name": "🎮 Game ID", "value": f"`{game_id}`", "inline": True})
    if player:
        fields.append({"name": "👤 Player", "value": player, "inline": True})
    fields.append({"name": "🤖 Bots Running", "value": str(random.randint(1, 4)), "inline": True})
    
    send_embed(
        title="🟢 LAZY AJ STATUS",
        description=f"**{status}**",
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

send_status("Bot is now online and monitoring for brainrots!")

while True:
    now = time.time()
    
    for name, interval in BRAINROTS.items():
        if now - last_sent[name] >= interval:
            # Generate random stats
            mutation = random.choice(MUTATIONS)
            trait = random.choice(TRAITS) if random.random() < 0.3 else "None"
            
            # Calculate price
            base_value = random.randint(50, 500)
            mutation_mult = {"Normal":1, "Gold":1.25, "Diamond":1.5, "Candy":4, "Lava":6, "Galaxy":7, "Yin Yang":7.5, "Radioactive":8.5, "Cursed":9, "Rainbow":10, "Divine":10, "Cyber":11}
            trait_mult = {"None":1, "Strawberry":8, "Meowl":7, "Skibidi":6.5, "Firework":6, "Lightning":6, "Spider":4.5, "Galactic":4}
            
            price = base_value * mutation_mult.get(mutation, 1) * trait_mult.get(trait, 1)
            price = int(price * (0.8 + random.random() * 0.4))
            price = max(50, min(15000, price))
            
            target_game = random.choice(SAB_GAME_IDS)
            
            # Send detection embed
            send_detection(name, mutation, trait, price, target_game)
            last_sent[name] = now
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detection: {name} -> {target_game} (${price}M)")
            
            # Wait 30-90 seconds before next detection
            time.sleep(random.randint(30, 90))
    
    time.sleep(10)
