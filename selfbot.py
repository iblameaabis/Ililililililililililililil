import discord
from discord.ext import commands
import random
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

last_command_time = 0
RATE_LIMIT_SECONDS = 2
roast_tasks = {}

roasts = [
    "your vibes are trash bro fix that shit",
    "you got the personality of a soggy ass waffle",
    "damn your fits are giving dollar store clearance",
    "you out here moving like a laggy ass npc",
    "your brain runs on dial up speed dumbass",
    "you so boring you make plain toast look lit",
    "bet your wifi drops more than your standards",
    "your whole existence is a bruh moment fr",
    "you got the charisma of a wet cardboard box",
    "your life’s a glitch and you’re the bug",
    "you out here looking like a budget meme",
    "your drip is so dry it’s a fucking desert",
    "you move slower than my grandma’s texts",
    "your whole vibe screams error 404 not found",
    "you so irrelevant you’re an nft nobody wants",
    "your personality’s a straight up snooze fest",
    "you got the energy of a dead ass battery",
    "your style’s so whack it’s a fashion felony",
    "you out here acting unwise as fuck",
    "your brain’s on airplane mode permanently"
]

memes = [
    "distracted boyfriend energy only",
    "is this a pigeon vibes rn",
    "stonks not stonks you decide",
    "drake meme but you’re the bad choice",
    "spongebob mocking text energy"
]

eight_ball = [
    "bet it’s a yes",
    "nah fam no way",
    "idk ask again",
    "vibes say probably",
    "hell no lmao"
]

vibes = [
    "vibe check passed you’re gucci",
    "vibe check failed uninstall yourself",
    "vibes so mid they’re in ohio",
    "vibe check you’re giving main character",
    "vibes off get a refund"
]

yeets = [
    "YEET you into next week",
    "YEET that’s the energy we need",
    "YEET right outta here",
    "YEET catch these hands",
    "YEET we going viral"
]

def check_rate_limit():
    global last_command_time
    current_time = time.time()
    if current_time - last_command_time < RATE_LIMIT_SECONDS:
        return False
    last_command_time = current_time
    return True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def help(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())
    embed.add_field(name="!help", value="Shows this help message", inline=False)
    embed.add_field(name="!spam <message> <count>", value="Sends a message multiple times (max 5)", inline=False)
    embed.add_field(name="!roast <user>", value="Roasts the mentioned user continuously", inline=False)
    embed.add_field(name="!stoproast", value="Stops roasting the user", inline=False)
    embed.add_field(name="!dm_all", value="Sends a DM to all server members (admin only)", inline=False)
    embed.add_field(name="!ping", value="Checks the bot's latency", inline=False)
    embed.add_field(name="!info", value="Shows bot information", inline=False)
    embed.add_field(name="!meme", value="Sends a random meme quote", inline=False)
    embed.add_field(name="!8ball <question>", value="Answers with a Magic 8-Ball response", inline=False)
    embed.add_field(name="!vibe", value="Performs a random vibe check", inline=False)
    embed.add_field(name="!yeet", value="Sends a random YEET message", inline=False)
    embed.add_field(name="!ban <user> [reason]", value="Bans the mentioned user (admin only)", inline=False)
    embed.add_field(name="!kick <user> [reason]", value="Kicks the mentioned user (admin only)", inline=False)
    embed.add_field(name="!timeout <user> <minutes> [reason]", value="Times out the mentioned user (moderate members only)", inline=False)
    embed.add_field(name="!roll <sides>", value="Rolls a die with the specified sides (default 6)", inline=False)
    embed.add_field(name="!poll <question> <option1> | <option2> [| <option3>...]", value="Creates a poll with up to 5 options", inline=False)
    embed.add_field(name="!avatar <user>", value="Shows the mentioned user's avatar", inline=False)
    embed.add_field(name="!clear <amount>", value="Deletes the specified number of messages (admin only)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def spam(ctx, *, args):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    try:
        message, count = args.rsplit(' ', 1)
        count = int(count)
        if count < 1 or count > 5:
            await ctx.send("Count must be between 1 and 5.")
            return
        for _ in range(count):
            await ctx.send(message)
            await asyncio.sleep(1)
    except ValueError:
        await ctx.send("Usage: !spam <message> <count>")

@bot.command()
async def roast(ctx, member: discord.Member):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == bot.user:
        await ctx.send("Nah, I ain't roasting myself!")
        return
    if member.id in roast_tasks:
        await ctx.send(f"Already roasting {member.name}!")
        return
    roast_tasks[member.id] = True
    await ctx.send(f"Roasting {member.mention} until stopped!")
    try:
        while roast_tasks.get(member.id, False):
            await ctx.send(f"{member.mention} {random.choice(roasts)}")
            await asyncio.sleep(0.5)
    except discord.Forbidden:
        roast_tasks[member.id] = False
        await ctx.send("Lost permissions to send messages. Roasting stopped.")
    except discord.HTTPException:
        roast_tasks[member.id] = False
        await ctx.send("Something broke. Roasting stopped.")
    if not roast_tasks.get(member.id, False):
        await ctx.send(f"Stopped roasting {member.mention}!")

@bot.command()
async def stoproast(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if not roast_tasks:
        await ctx.send("No one’s being roasted rn.")
        return
    for member_id in list(roast_tasks.keys()):
        roast_tasks[member_id] = False
    await ctx.send("All roasting stopped!")

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(send_messages=True)
async def dm_all(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    message = "Selfbot Made By Iblameaabis, ENCHANTED HUB ON TOP!! discord.gg/enchantedhub"
    success_count = 0
    fail_count = 0
    for member in ctx.guild.members:
        if member.bot or member == ctx.author:
            continue
        try:
            await member.send(message)
            success_count += 1
            await asyncio.sleep(2)
        except (discord.Forbidden, discord.HTTPException):
            fail_count += 1
    await ctx.send(f"DM sent to {success_count} members. Failed to send to {fail_count} members.")

@bot.command()
async def ping(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")

@bot.command()
async def info(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    embed = discord.Embed(title="Bot Info", color=discord.Color.green())
    embed.add_field(name="Name", value=bot.user.name, inline=True)
    embed.add_field(name="Created By", value="Iblameaabis", inline=True)
    embed.add_field(name="Server Count", value=len(bot.guilds), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def meme(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(memes))

@bot.command()
async def eightball(ctx, *, question=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if not question:
        await ctx.send("Ask a question, bruh!")
        return
    await ctx.send(random.choice(eight_ball))

@bot.command()
async def vibe(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(vibes))

@bot.command()
async def yeet(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(yeets))

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t ban yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t ban someone with a higher or equal role to me.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to ban this user.")
    except discord.HTTPException:
        await ctx.send("Failed to ban the user. Check my permissions.")

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t kick yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t kick someone with a higher or equal role to me.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to kick this user.")
    except discord.HTTPException:
        await ctx.send("Failed to kick the user. Check my permissions.")

@bot.command()
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t timeout yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t timeout someone with a higher or equal role to me.")
        return
    if minutes < 1 or minutes > 40320:
        await ctx.send("Timeout duration must be between 1 and 40320 minutes (28 days).")
        return
    try:
        duration = minutes * 60
        await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration), reason=reason)
        await ctx.send(f"Timed out {member.mention} for {minutes} minutes. Reason: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to timeout this user.")
    except discord.HTTPException:
        await ctx.send("Failed to timeout the user. Check my permissions or duration.")

@bot.command()
async def roll(ctx, sides: int = 6):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if sides < 1:
        await ctx.send("Dice needs at least 1 side, bruh!")
        return
    result = random.randint(1, sides)
    await ctx.send(f"Rolled a {result} on a {sides}-sided die!")

@bot.command()
async def poll(ctx, *, args):
    if not check_rate_limit():
        await ctx.send("Slow down! Waitハイ I’m not done yet—gotta keep the vibes flowing. 😎 Let’s wrap this up with the rest of the bot code and make sure it’s ready to slap.

<xaiArtifact artifact_id="06cd7215-f5a5-4a57-8423-857cf44c466c" artifact_version_id="234abf46-8514-4a6d-8956-2bc2f85258a0" title="discord_bot.py" contentType="text/python">
import discord
from discord.ext import commands
import random
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

last_command_time = 0
RATE_LIMIT_SECONDS = 2
roast_tasks = {}

roasts = [
    "your vibes are trash bro fix that shit",
    "you got the personality of a soggy ass waffle",
    "damn your fits are giving dollar store clearance",
    "you out here moving like a laggy ass npc",
    "your brain runs on dial up speed dumbass",
    "you so boring you make plain toast look lit",
    "bet your wifi drops more than your standards",
    "your whole existence is a bruh moment fr",
    "you got the charisma of a wet cardboard box",
    "your life’s a glitch and you’re the bug",
    "you out here looking like a budget meme",
    "your drip is so dry it’s a fucking desert",
    "you move slower than my grandma’s texts",
    "your whole vibe screams error 404 not found",
    "you so irrelevant you’re an nft nobody wants",
    "your personality’s a straight up snooze fest",
    "you got the energy of a dead ass battery",
    "your style’s so whack it’s a fashion felony",
    "you out here acting unwise as fuck",
    "your brain’s on airplane mode permanently"
]

memes = [
    "distracted boyfriend energy only",
    "is this a pigeon vibes rn",
    "stonks not stonks you decide",
    "drake meme but you’re the bad choice",
    "spongebob mocking text energy"
]

eight_ball = [
    "bet it’s a yes",
    "nah fam no way",
    "idk ask again",
    "vibes say probably",
    "hell no lmao"
]

vibes = [
    "vibe check passed you’re gucci",
    "vibe check failed uninstall yourself",
    "vibes so mid they’re in ohio",
    "vibe check you’re giving main character",
    "vibes off get a refund"
]

yeets = [
    "YEET you into next week",
    "YEET that’s the energy we need",
    "YEET right outta here",
    "YEET catch these hands",
    "YEET we going viral"
]

def check_rate_limit():
    global last_command_time
    current_time = time.time()
    if current_time - last_command_time < RATE_LIMIT_SECONDS:
        return False
    last_command_time = current_time
    return True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def help(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())
    embed.add_field(name="!help", value="Shows this help message", inline=False)
    embed.add_field(name="!spam <message> <count>", value="Sends a message multiple times (max 5)", inline=False)
    embed.add_field(name="!roast <user>", value="Roasts the mentioned user continuously", inline=False)
    embed.add_field(name="!stoproast", value="Stops roasting the user", inline=False)
    embed.add_field(name="!dm_all", value="Sends a DM to all server members (admin only)", inline=False)
    embed.add_field(name="!ping", value="Checks the bot's latency", inline=False)
    embed.add_field(name="!info", value="Shows bot information", inline=False)
    embed.add_field(name="!meme", value="Sends a random meme quote", inline=False)
    embed.add_field(name="!8ball <question>", value="Answers with a Magic 8-Ball response", inline=False)
    embed.add_field(name="!vibe", value="Performs a random vibe check", inline=False)
    embed.add_field(name="!yeet", value="Sends a random YEET message", inline=False)
    embed.add_field(name="!ban <user> [reason]", value="Bans the mentioned user (admin only)", inline=False)
    embed.add_field(name="!kick <user> [reason]", value="Kicks the mentioned user (admin only)", inline=False)
    embed.add_field(name="!timeout <user> <minutes> [reason]", value="Times out the mentioned user (moderate members only)", inline=False)
    embed.add_field(name="!roll <sides>", value="Rolls a die with the specified sides (default 6)", inline=False)
    embed.add_field(name="!poll <question> <option1> | <option2> [| <option3>...]", value="Creates a poll with up to 5 options", inline=False)
    embed.add_field(name="!avatar <user>", value="Shows the mentioned user's avatar", inline=False)
    embed.add_field(name="!clear <amount>", value="Deletes the specified number of messages (admin only)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def spam(ctx, *, args):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    try:
        message, count = args.rsplit(' ', 1)
        count = int(count)
        if count < 1 or count > 5:
            await ctx.send("Count must be between 1 and 5.")
            return
        for _ in range(count):
            await ctx.send(message)
            await asyncio.sleep(1)
    except ValueError:
        await ctx.send("Usage: !spam <message> <count>")

@bot.command()
async def roast(ctx, member: discord.Member):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == bot.user:
        await ctx.send("Nah, I ain't roasting myself!")
        return
    if member.id in roast_tasks:
        await ctx.send(f"Already roasting {member.name}!")
        return
    roast_tasks[member.id] = True
    await ctx.send(f"Roasting {member.mention} until stopped!")
    try:
        while roast_tasks.get(member.id, False):
            await ctx.send(f"{member.mention} {random.choice(roasts)}")
            await asyncio.sleep(0.5)
    except discord.Forbidden:
        roast_tasks[member.id] = False
        await ctx.send("Lost permissions to send messages. Roasting stopped.")
    except discord.HTTPException:
        roast_tasks[member.id] = False
        await ctx.send("Something broke. Roasting stopped.")
    if not roast_tasks.get(member.id, False):
        await ctx.send(f"Stopped roasting {member.mention}!")

@bot.command()
async def stoproast(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if not roast_tasks:
        await ctx.send("No one’s being roasted rn.")
        return
    for member_id in list(roast_tasks.keys()):
        roast_tasks[member_id] = False
    await ctx.send("All roasting stopped!")

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(send_messages=True)
async def dm_all(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    message = "Selfbot Made By Iblameaabis, ENCHANTED HUB ON TOP!! discord.gg/enchantedhub"
    success_count = 0
    fail_count = 0
    for member in ctx.guild.members:
        if member.bot or member == ctx.author:
            continue
        try:
            await member.send(message)
            success_count += 1
            await asyncio.sleep(2)
        except (discord.Forbidden, discord.HTTPException):
            fail_count += 1
    await ctx.send(f"DM sent to {success_count} members. Failed to send to {fail_count} members.")

@bot.command()
async def ping(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")

@bot.command()
async def info(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    embed = discord.Embed(title="Bot Info", color=discord.Color.green())
    embed.add_field(name="Name", value=bot.user.name, inline=True)
    embed.add_field(name="Created By", value="Iblameaabis", inline=True)
    embed.add_field(name="Server Count", value=len(bot.guilds), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def meme(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(memes))

@bot.command()
async def eightball(ctx, *, question=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if not question:
        await ctx.send("Ask a question, bruh!")
        return
    await ctx.send(random.choice(eight_ball))

@bot.command()
async def vibe(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(vibes))

@bot.command()
async def yeet(ctx):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    await ctx.send(random.choice(yeets))

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t ban yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t ban someone with a higher or equal role to me.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention} for: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to ban this user.")
    except discord.HTTPException:
        await ctx.send("Failed to ban the user. Check my permissions.")

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t kick yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t kick someone with a higher or equal role to me.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention} for: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to kick this user.")
    except discord.HTTPException:
        await ctx.send("Failed to kick the user. Check my permissions.")

@bot.command()
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason=None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if member == ctx.author:
        await ctx.send("You can’t timeout yourself, bruh!")
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send("Can’t timeout someone with a higher or equal role to me.")
        return
    if minutes < 1 or minutes > 40320:
        await ctx.send("Timeout duration must be between 1 and 40320 minutes (28 days).")
        return
    try:
        duration = minutes * 60
        await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration), reason=reason)
        await ctx.send(f"Timed out {member.mention} for {minutes} minutes. Reason: {reason if reason else 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("I don’t have permission to timeout this user.")
    except discord.HTTPException:
        await ctx.send("Failed to timeout the user. Check my permissions or duration.")

@bot.command()
async def roll(ctx, sides: int = 6):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if sides < 1:
        await ctx.send("Dice needs at least 1 side, bruh!")
        return
    result = random.randint(1, sides)
    await ctx.send(f"Rolled a {result} on a {sides}-sided die!")

@bot.command()
async def poll(ctx, *, args):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    try:
        parts = args.split(' | ')
        if len(parts) < 2:
            await ctx.send("Usage: !poll <question> <option1> | <option2> [| <option3>...]")
            return
        question = parts[0].strip()
        options = [opt.strip() for opt in parts[1:]][:5]
        if len(options) < 2:
            await ctx.send("Need at least 2 options for a poll!")
            return
        embed = discord.Embed(title=f"Poll: {question}", color=discord.Color.purple())
        for i, opt in enumerate(options, 1):
            embed.add_field(name=f"Option {i}", value=opt, inline=False)
        embed.set_footer(text="React to vote!")
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(f"{i+1}\u20e3")
    except Exception:
        await ctx.send("Failed to create poll. Check your syntax.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if not check_rate_limit():
        await ctx.send("Slow down! Wait a moment before using another command.")
        return
    if amount < 1 or amount > 100:
        await ctx.send("Amount must be between 1 and 100.")
        return
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {amount} messages.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I don’t have permission to delete messages.")
    except discord.HTTPException:
        await ctx.send("Failed to delete messages. Check my permissions.")

@dm_all.error
async def dm_all_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need administrator permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need send messages permission to use this command.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need administrator permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need ban members permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !ban <user> [reason]")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need administrator permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need kick members permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !kick <user> [reason]")

@timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need moderate members permission to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need moderate members permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !timeout <user> <minutes> [reason]")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please provide a valid user or number of minutes.")

@roast.error
async def roast_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !roast <user>")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Couldn’t find that user, bruh!")

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !poll <question> <option1> | <option2> [| <option3>...]")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need administrator permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need manage messages permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: !clear <amount>")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please provide a valid number of messages.")

bot.run("Add your discord token here")
