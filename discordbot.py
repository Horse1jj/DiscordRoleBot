import discord
from discord.ext import commands

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
    if message.author.bot:  # Ignore messages from bots to avoid potential loops
        return

    desired_channel_id = YOUR_CHANNEL_ID  # Replace with actual channel ID
    if message.channel.id != desired_channel_id:
        return

    text = message.content.strip().lower()

    guild = bot.get_guild(YOUR_SERVER_ID)  # Replace with actual server ID
    if guild is None:
        print("Bot is not in the specified server.")
        return

    role_to_give = guild.get_role(YOUR_ROLE_ID)  # Replace with actual role ID
    if role_to_give is None:
        print("Role not found.")
        return

    member = discord.utils.get(guild.members, name=text)
    if member:
        try:
            await member.add_roles(role_to_give)
            print(f'Gave role to {member.name} for being mentioned.')
            await message.add_reaction('✅')
        except discord.Forbidden:
            print(f"Failed to give role to {member.name}. Missing Permissions.")
            await message.add_reaction('❌')
        except discord.HTTPException:
            print(f"Failed to give role to {member.name}. HTTP Exception.")
            await message.add_reaction('❌')

    await bot.process_commands(message)  # Ensure commands still work

# Replace placeholders with actual IDs
YOUR_SERVER_ID = 112998032189
YOUR_ROLE_ID = 11299945306
YOUR_CHANNEL_ID = 11300305620

# Run the bot
bot.run('YOUR_BOT_TOKEN')  # Replace with your bot token
