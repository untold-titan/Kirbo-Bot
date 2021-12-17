# bot.py
VERSION = 'V0.0.1 DEV'
import os

import discord
from discord import client
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',',intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Army Gang!'))
    print(f'{bot.user.name} has connected to Discord!')

#Commands ------------------------------------------------------------------
@bot.command(name='poyo', help='Signature Korby noise')
@commands.has_role('admin')
async def poyo(ctx):
    await ctx.send('Poyo!')

@bot.command(name='store', help='Opens the Army Gang store')
@commands.has_role('admin')
async def store(ctx):
    await ctx.send('Army Gang Store\nCustom Role = 15000 tokens')

@bot.command(name='about', help='Infomation about the bot, and its developer')
@commands.has_role('admin')
async def about(ctx):
    myEmbed=discord.Embed(title=f"Kirbo Bot {VERSION}",url="https://github.com/cataclysm-interactive/Kirbo-Bot",description="This bot was developed by Cataclysm-Interactive for the Army Gang", color=PINK)
    myEmbed.set_author(name="christmas titan#1704", icon_url="https://icy-mushroom-088e1a210.azurestaticapps.net/pfp.png")
    myEmbed.add_field(name="Acknowledgements:", value="Titan - Lead Developer")
    myEmbed.set_footer(text="This bot's code is on Github! Tap the embed to go there!")
    await ctx.send(embed=myEmbed)

@bot.command(name="shutdown")
@commands.has_role("admin")
async def shutdown(ctx):
    quit()


#Events ---------------------------------------------------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Since this bot is still in development, it is restriced to admins only! Sorry!')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')

bot.run(TOKEN)