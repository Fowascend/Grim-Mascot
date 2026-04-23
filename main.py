@bot.command(name='mutation')
async def mutation_info(ctx, *, name: str = None):
    """Get info about a mutation. Example: !mutation rainbow"""
    if not name:
        await ctx.send("Usage: `!mutation rainbow` or `!mutation list`")
        return
    
    name_lower = name.lower()
    if name_lower == "list":
        msg = "**📋 Mutations List:**\n"
        for m, data in sorted(mutations.items(), key=lambda x: -x[1]["mult"]):
            msg += f"• **{m.title()}**: {data['mult']}x - {data['desc']}\n"
        await ctx.send(msg)
        return
    
    if name_lower in mutations:
        data = mutations[name_lower]
        await ctx.send(f"**{name.title()} Mutation**\n• Multiplier: {data['mult']}x\n• Rarity: {data['rarity']}\n• {data['desc']}")
    else:
        await ctx.send(f"Unknown mutation: {name}. Use `!mutation list` to see all.")

@bot.command(name='trait')
async def trait_info(ctx, *, name: str = None):
    """Get info about a trait. Example: !trait strawberry"""
    if not name:
        await ctx.send("Usage: `!trait strawberry` or `!trait list`")
        return
    
    name_lower = name.lower()
    if name_lower == "list":
        msg = "**📋 Traits List (Best to Worst):**\n"
        for t, data in sorted(traits.items(), key=lambda x: -x[1]["mult"]):
            mult_display = f"{data['mult']}x" if data['mult'] >= 1 else f"÷{int(1/data['mult'])}"
            msg += f"• **{t.title()}**: {mult_display} - {data['desc']}\n"
        await ctx.send(msg)
        return
    
    if name_lower in traits:
        data = traits[name_lower]
        mult_display = f"{data['mult']}x" if data['mult'] >= 1 else f"÷{int(1/data['mult'])}"
        await ctx.send(f"**{name.title()} Trait**\n• Multiplier: {mult_display}\n• {data['desc']}")
    else:
        await ctx.send(f"Unknown trait: {name}. Use `!trait list` to see all.")

@bot.command(name='bestcombo')
async def best_combo(ctx):
    """Shows the best mutation + trait combo"""
    best_mut, best_trait, total = get_best_combo()
    await ctx.send(f"**🏆 Best Income Combo:**\n• Mutation: **{best_mut.title()}** ({mutations[best_mut]['mult']}x)\n• Trait: **{best_trait.title()}** ({traits[best_trait]['mult']}x)\n• **Total: {total}x multiplier!**")
