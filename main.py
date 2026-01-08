import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
Welcome_channel_id = int(os.getenv('WELCOME_CHANNEL_ID'))
join_message_id = int(os.getenv('JOIN_MESSAGE_ID'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)

async def on_ready():
    await Bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"Over The CivCraft Server", type=discord.ActivityType.watching))

@bot.event
async def on_ready():
    print(f"bot ready, {bot.user.name}")



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(Welcome_channel_id)
    if channel:
        try:
            message_to_reply = await channel.fetch_message(join_message_id)
            await asyncio.sleep(15)
            sent_message = await channel.send(f"Welcome To The CivCraft Server {member.mention}!", reference=message_to_reply, mention_author=False)
            await asyncio.sleep(10)
            await sent_message.delete()
        except discord.NotFound:
            await asyncio.sleep(15)
            sent_message = await channel.send(f"Welcome To The CivCraft Server {member.mention}!")
            await asyncio.sleep(10)
            await sent_message.delete()



@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

@bot.command()
async def stupid(ctx):
    await ctx.send(f"Stupid Message Spotted! Read <#1123759555663384617> First! ")



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
