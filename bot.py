import requests
import random
import time
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# SAB Game IDs that auto join teleports to
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
}

MUTATIONS = ["Cyber", "Divine", "Rainbow", "Cursed", "Radioactive", "Galaxy", "Lava", "Gold"]
TRAITS = ["Strawberry", "Meowl", "Skibidi", "Firework", "Lightning", "Spider", "Galactic"]

last_sent = {name: 0 for name in BRAINROTS}

# ============================================================
# FUNCTIONS
# ============================================================
def send_webhook(message):
    try:
        data = {"content": message, "username": "Lazy AJ"}
        requests.post(WEBHOOK_URL, json=data)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {message[:60]}...")
    except Exception as e:
        print(f"Webhook error: {e}")

def send_detection(name, mutation, trait, price, target_game):
    msg = f"""**🎯 NEW BRAINROT DETECTED**
**Name:** {name}
**Mutation:** {mutation}
**Trait:** {trait if trait else 'None'}
**Value:** ${price}M
**Teleporting to Game:** `{target_game}`"""
    send_webhook(msg)

def send_join_notification(name, target_game, current_game):
    msg = f"""**✅ AUTO JOIN TRIGGERED**
**Brainrot:** {name}
**Teleporting to:** `{target_game}`
**Current Game:** `{current_game}`"""
    send_webhook(msg)

def send_status(status, game_id=None, player=None):
    msg = f"**🟢 LAZY AJ STATUS**\n**Status:** {status}"
    if game_id:
        msg += f"\n**Game ID:** `{game_id}`"
    if player:
        msg += f"\n**Player:** {player}"
    send_webhook(msg)

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
            trait = random.choice(TRAITS) if random.random() < 0.3 else ""
            price = random.randint(500, 15000)
            target_game = random.choice(SAB_GAME_IDS)
            
            # Send detection
            send_detection(name, mutation, trait, price, target_game)
            last_sent[name] = now
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detection: {name} -> Game {target_game}")
            
            # Wait 30-90 seconds before next detection
            time.sleep(random.randint(30, 90))
    
    # Check every 10 seconds
    time.sleep(10)
