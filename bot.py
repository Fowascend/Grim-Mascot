@bot.tree.command(name="whitelist", description="Whitelist a user to access a script")
@app_commands.describe(user="User to whitelist", project="Project name", days="Days of access (leave empty for lifetime)", note="Optional note")
async def whitelist(interaction: discord.Interaction, user: discord.User, project: str, days: int = None, note: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, buyer_role_id, api_key FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id, buyer_role_id, api_key = project_data
    
    # Check if already whitelisted
    c.execute("SELECT id FROM whitelist WHERE user_id = ? AND project_id = ?", (user.id, project_id))
    existing = c.fetchone()
    
    if existing:
        await interaction.response.send_message(f"❌ {user.mention} is already whitelisted for {project}.", ephemeral=True)
        return
    
    # Get an available key
    c.execute("SELECT id, key_code FROM keys WHERE project_id = ? AND redeemed_by IS NULL LIMIT 1", (project_id,))
    key_data = c.fetchone()
    
    if not key_data:
        await interaction.response.send_message(f"❌ No available keys for project '{project}'. Generate some with /generatekey first.", ephemeral=True)
        return
    
    key_id, key_code = key_data
    is_lifetime = days is None
    expires_at = int(time.time()) + (days * 86400) if days else None
    
    # Update key as redeemed
    c.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (user.id, int(time.time()), key_id))
    c.execute("INSERT INTO whitelist (user_id, project_id, key_id, whitelisted_by, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (user.id, project_id, key_id, interaction.user.id, int(time.time()), expires_at, is_lifetime))
    conn.commit()
    
    # Add buyer role if set
    role_added = False
    if buyer_role_id and interaction.guild:
        member = interaction.guild.get_member(user.id)
        if member:
            role_added = await add_buyer_role(member, buyer_role_id, interaction.guild.id)
    
    # Get control panel channel
    control_channel = bot.get_channel(CONTROL_PANEL_CHANNEL_ID)
    
    # Create control panel embed
    panel_embed = discord.Embed(
        title="🎮 GrimPot Control Panel",
        description=f"**User:** {user.mention}\n**Project:** {project}\n**Whitelisted by:** {interaction.user.mention}\n**Access Type:** {'Lifetime' if is_lifetime else f'{days} days'}",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    panel_embed.add_field(name="🔑 Key", value=f"`{key_code}`", inline=False)
    panel_embed.add_field(name="👑 Role Added", value="✅ Yes" if role_added else "❌ No (role not set or user not in server)", inline=False)
    panel_embed.add_field(name="📝 Note", value=note or "No note", inline=False)
    panel_embed.set_footer(text="GrimPot Licensing System")
    
    # Send to control panel channel
    if control_channel:
        panel_msg = await control_channel.send(embed=panel_embed)
        panel_link = panel_msg.jump_url
    else:
        panel_link = "Channel not found"
    
    # Send whitelist message in the same channel
    whitelist_embed = discord.Embed(
        title="✅ USER WHITELISTED",
        description=f"**{user.mention}** has been whitelisted for **{project}**!\n\n**Access Type:** {'Lifetime' if is_lifetime else f'{days} days'}\n**Key:** `{key_code}`\n**Control Panel:** [Click Here]({panel_link})",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    if role_added:
        whitelist_embed.add_field(name="👑 Role", value="Buyer role automatically assigned!", inline=False)
    if note:
        whitelist_embed.add_field(name="📝 Note", value=note, inline=False)
    
    await interaction.response.send_message(embed=whitelist_embed)

@bot.tree.command(name="blacklist", description="Remove a user's access to a project")
@app_commands.describe(user="User to blacklist", project="Project name", reason="Reason for blacklist")
async def blacklist(interaction: discord.Interaction, user: discord.User, project: str, reason: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, buyer_role_id FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id, buyer_role_id = project_data
    
    c.execute("DELETE FROM whitelist WHERE user_id = ? AND project_id = ?", (user.id, project_id))
    
    if c.rowcount == 0:
        await interaction.response.send_message(f"❌ {user.mention} is not whitelisted for {project}.", ephemeral=True)
        return
    
    # Remove buyer role if set
    role_removed = False
    if buyer_role_id and interaction.guild:
        member = interaction.guild.get_member(user.id)
        if member:
            role_removed = await remove_buyer_role(member, buyer_role_id, interaction.guild.id)
    
    # Mark key as unused
    c.execute("UPDATE keys SET redeemed_by = NULL, redeemed_at = NULL WHERE redeemed_by = ? AND project_id = ?", (user.id, project_id))
    conn.commit()
    
    blacklist_embed = discord.Embed(
        title="⛔ USER BLACKLISTED",
        description=f"**{user.mention}** has been blacklisted from **{project}**!\n**Reason:** {reason or 'No reason provided'}",
        color=0xFF0000,
        timestamp=datetime.now()
    )
    if role_removed:
        blacklist_embed.add_field(name="👑 Role", value="Buyer role automatically removed!", inline=False)
    
    await interaction.response.send_message(embed=blacklist_embed)

@bot.tree.command(name="listusers", description="List all whitelisted users for a project")
@app_commands.describe(project="Project name")
async def listusers(interaction: discord.Interaction, project: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id = project_data[0]
    
    c.execute("SELECT user_id, whitelisted_at, expires_at, is_lifetime FROM whitelist WHERE project_id = ?", (project_id,))
    users = c.fetchall()
    
    if not users:
        await interaction.response.send_message(f"No users whitelisted for {project}.", ephemeral=True)
        return
    
    user_list = []
    for user_id, whitelisted_at, expires_at, is_lifetime in users:
        try:
            member = interaction.guild.get_member(user_id) if interaction.guild else None
            name = member.display_name if member else f"<@{user_id}>"
        except:
            name = f"Unknown ({user_id})"
        
        if is_lifetime:
            status = "🟢 Lifetime"
        elif expires_at and expires_at < int(time.time()):
            status = "🔴 Expired"
        else:
            status = f"🟢 Expires <t:{expires_at}:R>"
        
        user_list.append(f"{status} - {name} - Whitelisted <t:{whitelisted_at}:R>")
    
    embed = discord.Embed(
        title=f"📋 Whitelisted Users - {project} ({len(users)})",
        description="\n".join(user_list[:25]),
        color=0x00FF00,
        timestamp=datetime.now()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="keys", description="Show all keys for a project")
@app_commands.describe(project="Project name")
async def keys(interaction: discord.Interaction, project: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id = project_data[0]
    
    c.execute("SELECT key_code, redeemed_by, redeemed_at, is_lifetime, expires_at FROM keys WHERE project_id = ?", (project_id,))
    keys_data = c.fetchall()
    
    used = [k for k in keys_data if k[1] is not None]
    unused = [k for k in keys_data if k[1] is None]
    
    embed = discord.Embed(
        title=f"🔑 Key Management - {project}",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.add_field(name="📊 Total Keys", value=str(len(keys_data)), inline=True)
    embed.add_field(name="✅ Used Keys", value=str(len(used)), inline=True)
    embed.add_field(name="🆓 Unused Keys", value=str(len(unused)), inline=True)
    
    if unused:
        unused_text = "\n".join([f"`{k[0]}`" for k in unused[:10]])
        if len(unused) > 10:
            unused_text += f"\n... and {len(unused) - 10} more"
        embed.add_field(name="🆓 Unused Keys", value=unused_text, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="checkuser", description="Check if a user is whitelisted")
@app_commands.describe(user="User to check", project="Project name")
async def checkuser(interaction: discord.Interaction, user: discord.User, project: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id = project_data[0]
    
    c.execute("SELECT is_lifetime, expires_at, whitelisted_at FROM whitelist WHERE user_id = ? AND project_id = ?", (user.id, project_id))
    data = c.fetchone()
    
    if not data:
        await interaction.response.send_message(f"❌ {user.mention} is NOT whitelisted for {project}.", ephemeral=True)
        return
    
    is_lifetime, expires_at, whitelisted_at = data
    
    if is_lifetime:
        status = "✅ Lifetime Access"
    elif expires_at < int(time.time()):
        status = "❌ EXPIRED"
    else:
        status = f"✅ Active until <t:{expires_at}:F>"
    
    embed = discord.Embed(
        title="👤 User Status",
        description=f"**User:** {user.mention}\n**Project:** {project}\n**Status:** {status}\n**Whitelisted:** <t:{whitelisted_at}:R>",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="resetkey", description="Reset a user's key and generate a new one")
@app_commands.describe(user="User to reset key for", project="Project name")
async def resetkey(interaction: discord.Interaction, user: discord.User, project: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE name = ?", (project,))
    project_data = c.fetchone()
    
    if not project_data:
        await interaction.response.send_message(f"❌ Project '{project}' not found.", ephemeral=True)
        return
    
    project_id = project_data[0]
    
    c.execute("SELECT key_id FROM whitelist WHERE user_id = ? AND project_id = ?", (user.id, project_id))
    data = c.fetchone()
    
    if not data:
        await interaction.response.send_message(f"❌ {user.mention} is not whitelisted for {project}.", ephemeral=True)
        return
    
    key_id = data[0]
    
    # Generate new key
    new_key = generate_key()
    
    # Update key
    c.execute("UPDATE keys SET key_code = ?, redeemed_at = ? WHERE id = ?", (new_key, int(time.time()), key_id))
    conn.commit()
    
    embed = discord.Embed(
        title="🔄 Key Reset",
        description=f"**User:** {user.mention}\n**Project:** {project}\n**New Key:** `{new_key}`",
        color=0xFFA500,
        timestamp=datetime.now()
    )
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
