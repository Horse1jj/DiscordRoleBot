import discord
import json
from discord.ext import commands

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

TOKEN = config["bot_token"]
GUILD_ID = config["server_id"]
ROLE_ID = config["role_id"]
CHANNEL_ID = config["channel_id"]

# Setup bot with intents
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="recent donations"))

@bot.event
async def on_message(message):
    if message.author.bot:  # Ignore bot messages to prevent loops
        return

    if message.channel.id != CHANNEL_ID:
        return

    text = message.content.strip().lower()

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("Bot is not in the specified server.")
        return

    role_to_give = guild.get_role(ROLE_ID)
    if role_to_give is None:
        print("Role not found.")
        return

    # Find a member with a username that matches the message content
    member = discord.utils.find(lambda m: m.name.lower() == text, guild.members)
    if member:
        try:
            await member.add_roles(role_to_give)
            print(f"Gave {member.name} the donator role.")
            await message.add_reaction('✅')
        except discord.Forbidden:
            print(f"Failed to give {member.name} the role. Missing Permissions.")
            await message.add_reaction('❌')
        except discord.HTTPException:
            print(f"Failed to give {member.name} the role due to an HTTP error.")
            await message.add_reaction('❌')
    else:
        print(f"No matching user found for '{text}'.")

    await bot.process_commands(message)  # Ensure other commands still work

# Run the bot
bot.run(TOKEN)
