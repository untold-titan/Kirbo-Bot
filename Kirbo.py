# bot.py

# TODO: Replace ALL HTTPS requests with Firebase.

import os
import ast
from discord.ext.commands.converter import MemberConverter
import requests
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color
from Datatypes import User
import traceback
import datetime

from Helper import db, getUserData
import Helper
import sys
sys.path.insert(0,"Commands")
from Fun import FunCog
from Factions import FactionCog
from MTG import MTGCog
from Economy import EconomyCog


VERSION = 'V0.1.9'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users/"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions/"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',',intents=intents,activity=discord.Activity(type=discord.ActivityType.playing, name='LEGO Star Wars'))
bot.titan=None

@bot.event
async def on_ready():
    bot.titan = bot.get_user(847989667088564244)
    bot.adminChat = bot.get_channel(764867760957947934)
    bot.add_cog(FunCog(bot))
    # bot.add_cog(FactionCog(bot))
    bot.add_cog(MTGCog(bot))
    bot.add_cog(EconomyCog(bot))
    print(f'{bot.user.name} has connected to Discord!')

# User Income Update Function ----------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler

# Start the scheduler
sched = BackgroundScheduler()

# Adds Faction Income, Currently Broken cause Factions had a rework. 
# def job_function():
#     users = Helper.getAllUsers()
#     for user in users:
#         faction = Helper.getUserFaction(user["id"])
#         if faction != None:
#             amount = int(faction["factionIncome"])
#             tokens = int(user["token"]) + amount
#             jsonData = {"id": user["id"], "token": tokens, "date": f"{user['date']}"}
#             response = requests.put(USER_URL +str(user["id"]),json=jsonData)
#             if(response.status_code != 204):
#                 print(f"Something went wrong with adding Tokens to user's balance. Heres the error code: {response.status_code}")
         

# Schedules job_function to be run once each day
# hours = 24
# sched.add_job(job_function, 'interval', hours=hours)
# sched.start()

# About Bot Command --------------------------------------------------------------
@commands.command(name='about')
async def about(self,ctx):
    myEmbed=discord.Embed(title=f"Kirbo Bot {VERSION}",url="https://github.com/cataclysm-interactive/Kirbo-Bot",description="This bot was developed by Untold_Titan for the Army Gang", color=PINK)
    myEmbed.set_author(name="Untold_Titan#4644", icon_url="https://icy-mushroom-088e1a210.azurestaticapps.net/pfp.png")
    myEmbed.add_field(name="Changes:", value="All the backend of this bot, and Army Gang's website was redone, everything should be faster now!")
    myEmbed.add_field(name="Acknowledgements:", value="Titan - Lead Developer\nLord Death_Trooper - Helping with testing and Ideas.")
    myEmbed.set_footer(text="This bot's code is on Github! Tap the embed to go there!")
    await ctx.send(embed=myEmbed)


# Help Command --------------------------------------------------------------
bot.remove_command('help')
@bot.command("help")
async def help(ctx):
    embed=discord.Embed(title="Kirbo Help",description="This bot's prefix is ','\nSome of the commands have aliases.",color=PINK)
    embed.add_field(name="Fun Commands", value="about, poyo, roll, slap, shoot, finish",inline=False)
    embed.add_field(name="Economy Commands",value="balance, daily, store, buy, give",inline=False)
    embed.add_field(name="Faction Commands",value="All Factions commands are currently disabled!",inline=False)
    embed.add_field(name="MTG Commands",value="won, stats",inline=False)
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
    user = Helper.getUserData(u"temp-user")
    if user == None:
        user = User("temp-user","TemplateUser#6466")
        print(Helper.updateUser(user))
        return
    user.tokens = 50
    Helper.updateUser(user)
    await bot.titan.send("Check Firebase, Supposedly updated it. ")
    
    titan = User(ctx.author.id,ctx.author.name)
    Helper.updateUser(titan)
    titan2 = getUserData(str(ctx.author.id))
    titan2.tokens = 100
    Helper.updateUser(titan2)

    # docs = db.collection(u'users').stream()
    # user = Helper.getUserData("template-user")
    # await bot.titan.send(user.to_string())
    # # Will need to add other collections to this once they're created
    # for doc in docs:
    #     await ctx.send(f"{doc.id} => {doc.to_dict()}")
    

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

# @bot.event
# async def on_command_error(event, *args, **kwargs):
#     embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
#     embed.add_field(name='Event', value=event)
#     embed.description = '```py\n%s\n```' % traceback.format_exc()
#     embed.timestamp = datetime.datetime.utcnow()
#     await bot.titan.send(embed=embed)

@bot.event 
async def on_member_remove(member):
    await bot.adminChat.send(f"{member} Left")

@bot.event
async def on_member_join(member):
    await bot.adminChat.send(f"{member} Joined")
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')



bot.run(TOKEN)
