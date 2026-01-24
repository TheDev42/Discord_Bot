import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import random

load_dotenv()

# these load the variables stored in the .env file
token = os.getenv('DISCORD_TOKEN')
Welcome_channel_id = int(os.getenv('WELCOME_CHANNEL_ID'))
join_message_id = int(os.getenv('JOIN_MESSAGE_ID'))

# this is for logs
handler = logging.FileHandler(filename='bot_log.txt', encoding='utf-8', mode='w')

# bot permission requests
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents) # The discord bots prefix


@bot.event # tells console the bot is ready
async def on_ready():
    print(f"bot is ready, {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"Watching Over The CivCraft Server", type=discord.ActivityType.watching))



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(Welcome_channel_id)
    if channel:
        try:
            message_to_reply = await channel.fetch_message(join_message_id)
            await asyncio.sleep(15)
            sent_message = await channel.send(f"Welcome To The CivCraft Server {member.mention}!", reference=message_to_reply, mention_author=False)
            await asyncio.sleep(120)
            await sent_message.delete()
        except discord.NotFound:
            await asyncio.sleep(15)
            sent_message = await channel.send(f"Welcome To The CivCraft Server {member.mention}!")
            await asyncio.sleep(120)
            await sent_message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is on the specified channel and message
    if payload.channel_id == 1457516340431814880 and payload.message_id == 1458211664121041121:
        # Check if the emoji is island
        if str(payload.emoji) == '🏝':
            # Get the guild and member
            guild = bot.get_guild(payload.guild_id)
            if guild:
                member = guild.get_member(payload.user_id)
                if member:
                    # Get the role
                    role = guild.get_role(1123862354392776714)
                    if role:
                        try:
                            # Add the role to the member
                            await member.add_roles(role)
                            print(f"Added role {role.name} to {member.name}")
                        except discord.Forbidden:
                            print("Bot does not have permission to add roles.")
                        except Exception as e:
                            print(f"Error adding role: {e}")
                    else:
                        print("Role not found.")
                else:
                    print("Member not found.")
            else:
                print("Guild not found.")

@bot.event
async def on_raw_reaction_remove(payload):
    # Check if the reaction is on the specified channel and message
        # Check if the emoji is island
        if str(payload.emoji) == '🏝':
            # Get the guild and member
            guild = bot.get_guild(payload.guild_id)
            if guild:
                member = guild.get_member(payload.user_id)
                if member:
                    # Get the role
                    role = guild.get_role(1123862354392776714)
                    if role:
                        try:
                            # Remove the role from the member
                            await member.remove_roles(role)
                            print(f"Removed role {role.name} from {member.name}")
                        except discord.Forbidden:
                            print("Bot does not have permission to remove roles.")
                        except Exception as e:
                            print(f"Error removing role: {e}")
                    else:
                        print("Role not found.")
                else:
                    print("Member not found.")
            else:
                print("Guild not found.")



@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

@bot.command()
async def stupid(ctx):
    await ctx.send(f"Stupid Message Spotted! Read <#1123759555663384617> First! ")

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Server Roadmap", description="Ideas for the server.", color=0x00ff00)
    embed.add_field(name="CivCraft 5.5", value="For middle of february.", inline=False)
    embed.add_field(name="SMP Server", value="For end of march.", inline=False)
    embed.add_field(name="Network Server", value="At some point.", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def dice(ctx: commands.Context):
    await ctx.send("What value do you want to bet on?")
    message = await bot.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)
    value_input = message.content
    with open("test.txt", 'a') as txt:
        print(value_input, file = txt)


@bot.command()
async def dice1(ctx, value): # value variable will store user's input
    await ctx.send(f"You just bet {value} coins") # sends user's input
    value = value

@bot.command()
async def register(ctx):
    dm_channel = await ctx.author.create_dm()
    await dm_channel.send("What is your Minecraft username?")
    try:
        msg1 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel, timeout=60.0)
        username = msg1.content
        run = True
        while run == True:
            try:
                await dm_channel.send("How old are you?")
                msg2 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == dm_channel, timeout=60.0)
                age = int(msg2.content)
                run = False
            except ValueError as e:
                await dm_channel.send("that is not a number!")
        discord_id = ctx.author.id
        file_num = random.randint(1, 4)
        filename = f"file{file_num}.txt"
        with open(filename, 'a') as f:
            f.write(f"<@{discord_id}>, {username}, {age}\n")
        await dm_channel.send("Registration complete!")
    except asyncio.TimeoutError:
        await dm_channel.send("You took too long to respond.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
