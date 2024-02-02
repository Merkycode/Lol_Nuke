import discord
import logging
from discord.ext import commands

# Setup logging
logging.basicConfig(level=logging.INFO)

# Use your bot's token here
TOKEN = 'token'

# Replace with your Discord user ID
MY_USER_ID = "User ID Number"  # Make sure this is an integer, not a string

# Enable intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.presences = True  # May need to be enabled in the Discord Developer Portal

bot = commands.Bot(intents=intents)

# Flag to keep track of the command's state
disconnect_enabled = False


@bot.event
async def on_ready():
    print("This is a message")

@bot.slash_command(name="nuke", description="Secret command to toggle LoL nuke")
async def toggle_disconnect(ctx):
    global disconnect_enabled
    if ctx.author.id == int(MY_USER_ID):  # Ensure IDs are compared correctly
        disconnect_enabled = not disconnect_enabled
        # Send an immediate response to acknowledge the command
        await ctx.respond(f'LoL_Nuke toggling: {disconnect_enabled}. Checking voice channels now...')
        logging.info(f"LoL_Nuke toggled to: {disconnect_enabled} by {ctx.author}")

        if disconnect_enabled:
            # Perform the check and disconnect asynchronously
            bot.loop.create_task(check_and_disconnect(ctx))
    else:
        await ctx.respond('You do not have permission to use this command.')
        logging.warning(f"Unauthorized toggle attempt by {ctx.author}")



async def check_and_disconnect(ctx):
    print("this command was triggered")
    try:
        for guild in bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    for activity in member.activities:
                        print(f"{member} in {vc} - Activity: {activity.name}, Type: {type(activity)}")
                        if "League of Legends" in activity.name:
                            print("Made it before play disconnect")
                            await member.move_to(None, reason="Disconnected for playing League of Legends")
                            logging.info(f'{member} was disconnected for playing League of Legends.')
    except Exception as e:
        logging.error(f"Error in check_and_disconnect: {e}")
        # Handle or log the error appropriately
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.event
async def on_voice_state_update(member, before, after):
    global disconnect_enabled
    if disconnect_enabled and after.channel is not None:
        try:
            for guild in bot.guilds:
                for vc in guild.voice_channels:
                    for member in vc.members:
                        for activity in member.activities:
                            print(f"{member} in {vc} - Activity: {activity.name}, Type: {type(activity)}")
                            if "League of Legends" in activity.name:
                                print("Made it before play disconnect")
                                await member.move_to(None, reason="Disconnected for playing League of Legends")
                                logging.info(f'{member} was disconnected for playing League of Legends.')
        except Exception as e:
            logging.error(f"Error in check_and_disconnect: {e}")
            # Handle or log the error appropriately

bot.run(TOKEN)
