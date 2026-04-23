def handle_special_questions(message, author_id):
    """Handle all special questions including trades, values, and gay questions"""
    content = message.lower()
    
    # FIRST: Handle trade questions ("is X worth Y")
    trade_result = handle_trade_question(content, author_id)
    if trade_result:
        return trade_result
    
    # Handle "is X worth Y" for value checking (simple version)
    worth_match = re.search(r'is\s+(.+?)\s+worth\s+(.+?)\??$', content)
    if worth_match:
        item = worth_match.group(1).strip()
        value = worth_match.group(2).strip()
        
        # Check if it's a number (simple value check)
        if value.replace('.', '').isdigit():
            item_value = calculate_item_value(item)
            if item_value:
                if float(value) == item_value:
                    return f"Yes, {item} is worth {value} La Vacca Saturno Saturnita! 💯"
                else:
                    diff = float(value) - item_value
                    if diff > 0:
                        return f"No, {item} is worth {item_value:,}, not {value}. You're overvaluing it by {diff:.0f}!"
                    else:
                        return f"No, {item} is worth {item_value:,}, not {value}. It's actually worth more!"
            else:
                return f"I don't know what {item} is worth. Try `!value {item}`"
    
    # Handle "what is X worth"
    what_match = re.search(r'what\s+is\s+(.+?)\s+worth\??$', content)
    if what_match:
        item = what_match.group(1).strip()
        item_value = calculate_item_value(item)
        if item_value:
            return f"{item} is worth {item_value:,} La Vacca Saturno Saturnita"
        else:
            return f"I don't know what {item} is worth yet!"
    
    # Handle gay questions (existing code)
    gay_match = re.search(r'is\s+(.+?)\s+gay\??$', content)
    if gay_match:
        target = gay_match.group(1).strip().lower()
        
        if 'artful' in target:
            return "I don't talk about that. Artful is cool though. 💜"
        
        if author_id == OWNER_ID_1:
            if target in ['me', 'myself', 'i', 'fowascend']:
                return "You're the GOAT, bro. No labels needed. 👑"
            return "yes bro 💪"
        
        if author_id == OWNER_ID_2 and ('fowascend' in target or 'main owner' in target):
            return "No, main owner is straight as an arrow."
        
        if author_id == OWNER_ID_2 and target in ['me', 'myself', 'i', 'artful']:
            return "You're cool, Artful. That's all that matters. 💜"
        
        return "I don't really know. Ask the owners?"
    
    return None
