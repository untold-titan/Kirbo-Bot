# bot.py

import os
import ast
from discord.ext.commands.converter import MemberConverter
import requests
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color


import Helper
import sys
sys.path.insert(0,"Commands")
from Fun import FunCog
from Factions import FactionCog
from Economy import EconomyCog

VERSION = 'V0.1.8'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',',intents=intents,activity=discord.Activity(type=discord.ActivityType.listening, name='Army Gang!'))
bot.titan=None

@bot.event
async def on_ready():
    bot.titan = bot.get_user(847989667088564244)
    bot.adminChat = bot.get_channel(764867760957947934)
    bot.add_cog(FunCog(bot))
    bot.add_cog(FactionCog(bot))
    bot.add_cog(EconomyCog(bot))
    print(f'{bot.user.name} has connected to Discord!')

# User Income Update Function ----------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler

# Start the scheduler
sched = BackgroundScheduler()

def job_function():
    users = Helper.getAllUsers()
    for user in users:
        faction = Helper.getUserFaction(user["id"])
        if faction != None:
            amount = int(faction["factionIncome"])
            tokens = int(user["token"]) + amount
            jsonData = {"id": user["id"], "token": tokens, "date": f"{user['date']}"}
            response = requests.put(USER_URL + "/" + str(user["id"]),json=jsonData)
            if(response.status_code != 204):
                print(f"Something went wrong with adding Tokens to user's balance. Heres the error code: {response.status_code}")
         

# Schedules job_function to be run once each hour
minutes = 1
hours = 1
sched.add_job(job_function, 'interval', hours=hours)
sched.start()

#Help Command --------------------------------------------------------------
bot.remove_command('help')
@bot.command("help")
async def help(ctx):
    embed=discord.Embed(title="Kirbo Help",description="This bot's prefix is ','\nSome of the commands have aliases.",color=PINK)
    embed.add_field(name="Fun Commands", value="about, poyo, roll, slap, shoot, finish",inline=False)
    embed.add_field(name="Economy Commands",value="balance, daily, store, buy, give",inline=False)
    embed.add_field(name="Faction Commands",value="All Factions commands are currently disabled!",inline=False)
    embed.add_field(name="Debugging Commands",value="testapi, shutdown",inline=False)
    #faction, createfaction, leavefaction, invite, deposit, factionstore
    await ctx.send(embed=embed)


# Moderation Commands ------------------------------------------------------------
@bot.command(name="mute")
@commands.has_role("admin")
async def mute(ctx,member:MemberConverter):
    role = bot.get_guild(752023138795126856).get_role(796410893071810591)
    await member.add_roles(role)
    await ctx.send("Muted")

@bot.command(name="unmute")
@commands.has_role("admin")
async def unmute(ctx,member:MemberConverter):
    role = bot.get_guild(752023138795126856).get_role(796410893071810591)
    await member.remove_roles(role)
    await ctx.send("Unmuted")

# Debugging Commands -------------------------------------------------------------

@bot.command(name="testapi")
@commands.has_role("admin")
async def testapi(ctx):
    responseuser = requests.get(USER_URL)
    responsestore = requests.get(FACTION_URL)
    await bot.titan.send(responseuser.json())
    await bot.titan.send(responsestore.json())

@bot.command(name="shutdown")
@commands.has_role("admin")
async def shutdown(ctx):
    if ctx.author != bot.titan:
        await ctx.send("You aren't Titan!")
        return
    else:
        await ctx.send("Shutting down Kirbo bot!")
        quit()

@bot.command(name="testmsgs")
@commands.has_role("admin")
async def testmsgs(ctx):
    await bot.titan.send("Test")
    await bot.adminChat.send("Test")

@bot.command("enablefactions")
@commands.has_role("admin")
async def enableFaction(ctx):
    bot.add_cog(FactionCog(bot))
    await ctx.send("Factions Module Enabled!")

@bot.command("disablefactions")
@commands.has_role("admin")
async def disableFaction(ctx):
    bot.remove_cog('FactionCog')
    await ctx.send("Factions Module Disabled!")

@bot.command("enableeconomy")
@commands.has_role("admin")
async def enableEconomy(ctx):
    bot.add_cog(EconomyCog(bot))
    await ctx.send("Economy Module Enabled!")

@bot.command("disableeconomy")
@commands.has_role("admin")
async def disableEconomy(ctx):
    bot.remove_cog('EconomyCog')
    await ctx.send("Economy Module Disabled!")

#Events ---------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Thats an admin only command!')
    await bot.titan.send(f"{error}")

@bot.event 
async def on_member_remove(member):
    await bot.adminChat.send(f"{member} Left")

@bot.event
async def on_member_join(member):
    await bot.adminChat.send(f"{member} Joined")
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')



bot.run(TOKEN)
