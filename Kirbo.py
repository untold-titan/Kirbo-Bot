# bot.py

import os
import ast
from discord.ext.commands.converter import MemberConverter
import requests
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color
from datetime import datetime, timedelta

import Helper
import sys
sys.path.insert(0,"Commands")
from Fun import FunCog
from Factions import FactionCog
from MTG import MTGCog

VERSION = 'V0.1.8'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users/"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions/"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',',intents=intents,activity=discord.Activity(type=discord.ActivityType.playing, name='with itself'))
bot.titan=None

@bot.event
async def on_ready():
    bot.titan = bot.get_user(847989667088564244)
    bot.adminChat = bot.get_channel(764867760957947934)
    bot.add_cog(FunCog(bot))
    bot.add_cog(FactionCog(bot))
    bot.add_cog(MTGCog(bot))
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
            response = requests.put(USER_URL +str(user["id"]),json=jsonData)
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


# Economy Commands --------------------------------------------------------------

roleIDS=[
    766132157260496926,
    888905712275701791,
    912464479466442832,
    912469849421271041,
    912457301561069638,
    925455734307717141,
    911664993005600768,
    905119389244878909,
    890006091507830864,
    894726346184458270,
    890006064626561034,
    888468823144026113,
    888816896013643858,
    888468985392275467,
    888939559595958364,
    888939512514891788,
    888939461562486785,
    941763926327177226,
    892479878585286696
]

@bot.command(aliases=["s","shop"])
async def store(ctx):
    embed=discord.Embed(title="Army Gang Token Store",description="Use `,buy <item-number>` to purchase an item!",color=PINK)
    embed.add_field(name="1. Custom Role",value="15000 Tokens")
    i = 2
    for roleID in roleIDS:
        role = bot.get_guild(752023138795126856).get_role(roleID)
        embed.add_field(name=f"{i}. {role.name}",value="Price: FREE!",inline=False)
        i += 1
    embed.set_footer(text="If you have any ideas for things to put in the store, please DM Titan! :)")
    await ctx.send(embed=embed)

@bot.command(aliases=["d"])
async def daily(ctx):
    await ctx.send("Hold on a sec, this might take some time!")
    currentdate = datetime.now()
    userId = ctx.author.id
    url = USER_URL + str(userId)
    response = requests.get(url)
    jsonResponse = ast.literal_eval(str(response.json()))
    if response.status_code == 404:
        jsonData = {"Id": f"{userId}", "token": 500, "date": f"{currentdate.date()}T{currentdate.time().replace(microsecond=0)}", "customRole": 0}
        response = requests.post(USER_URL,json=jsonData)
        if response.status_code == 201:
            embed = discord.Embed(title="Daily Token Reward", description="You gained 500 AG Tokens!",color=PINK)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"There was an issue contacting the CataclysmAPI (ERROR CODE = {response.status_code})")
    elif response.status_code == 200:
        actualDate = datetime.strptime(jsonResponse["date"], '%Y-%m-%dT%H:%M:%S')
        if (currentdate - actualDate).days >= 1:
            total = int(jsonResponse["token"]) + 500
            jsonData = {"Id": f"{userId}","token": total, "date": f"{currentdate.date()}T{currentdate.time().replace(microsecond=0)}"}
            response = requests.put(url,json=jsonData)
            if response.status_code == 204:
                embed = discord.Embed(title="Daily Token Reward", description="You gained 500 AG Tokens!",color=PINK)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"There was an issue contacting the CataclysmAPI (ERROR CODE = {response.status_code})")
        else:
            dateUntil = (actualDate + timedelta(days=1)) - currentdate
            await ctx.send(f"You already claimed today's reward! Please try again in `{dateUntil}`")
    else:
        await ctx.send(f"There was an issue contacting the CataclysmAPI (ERROR CODE = {response.status_code})")

@bot.command(aliases=["balance","b"])
async def bal(ctx):
    jsonResponse = Helper.getUserData(ctx.author.id)
    if jsonResponse == None:
        json = {"Id":f"{ctx.author.id}"}
        response= requests.post(USER_URL,json)
        tokenAmt = 0
    else:
        tokenAmt = jsonResponse["token"]
    embed = discord.Embed(title=f"{ctx.author}'s Token Balance", description=f"{tokenAmt} AG tokens",color=PINK)
    await ctx.send(embed=embed)

@bot.command(name="buy")
async def buy(ctx,item: int):
    url = USER_URL + str(ctx.author.id)
    data = Helper.getUserData(ctx.author.id)
    if item == 1:
        if (int(data["token"]) - 15000) >= 0 and data["customRole"] != 1:
            tokens = int(data["token"]) - 15000
            jsonData = {"Id": f"{ctx.author.id}", "token":f'{tokens}', "date":f'{data["date"]}',"customRole":1}
            response= requests.put(url,json=jsonData)
            if response.status_code == 204:
                await ctx.send("You purchased a Custom Role!\nUse `,customrole <name> <color-hex-code>` to claim it!")
            else:
                await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
        else:
            if data["customRole"] == 1:
                await ctx.send("You already have a custom role!")
                return
            await ctx.send("You don't have enough tokens!")
    elif item > 1:
        role = bot.get_guild(752023138795126856).get_role(roleIDS[item - 2])
        await ctx.author.add_roles(role)
        await ctx.send(f"You bought: {role.name}")

@bot.command(name="give")
async def give(ctx,member: MemberConverter, amount: int):
    giver = Helper.getUserData(ctx.author.id)
    taker = Helper.getUserData(member.id)
    
    if giver != None and taker != None and giver["token"] >= amount:
        total = int(giver["token"]) - amount
        jsonGive = {"id":giver["id"],"token":int(total),"date":f"{giver['date']}"}
        response = requests.put(USER_URL+"/"+str(ctx.author.id),json=jsonGive)
        if response.status_code == 204:
            total = int(taker["token"]) + amount
            json = {"id":taker["id"],"token":int(total),"date":f"{taker['date']}"}
            response = requests.put(USER_URL+"/"+str(member.id),json=json)
            if response.status_code == 204:
                await ctx.send(f"Gave {amount} to {member}")
            else:
                await ctx.send("Something went wrong")
        else:
            await ctx.send("Somehting went wrong")
    elif taker == None:
        await ctx.send(member +"has to earn some tokens before they can recive!")
    elif giver == None:
        await ctx.send(ctx.author +"has to earn some tokens before they can send!")
    elif giver["token"] < amount:
        await ctx.send("You don't have enough tokens!")
    else:
        await ctx.send("Something went wrong. Try again later!")

@bot.command(name="customrole")
async def customrole(ctx,roleName:str,r:int,g:int,b:int):
    data = Helper.getUserData(ctx.author.id)
    if data["customRole"] == 1:
        guild = ctx.guild
        await guild.create_role(name=roleName,color=Color.from_rgb(r,g,b))
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        gamerRole = discord.utils.get(ctx.guild.roles, name="S Tier Gamer")
        await role.edit(position=gamerRole.position)
        user = ctx.message.author
        await user.add_roles(role)
        await ctx.send("Congrats! You now have your very own role!")
    else:
        await ctx.send("You haven't purchased a custom role!")


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

#Events ---------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Thats an admin only command!')
    await ctx.send(f"Something went wrong!\n{error}")
    await bot.titan.send(f"{error}")

@bot.event 
async def on_member_remove(member):
    await bot.adminChat.send(f"{member} Left")

@bot.event
async def on_member_join(member):
    await bot.adminChat.send(f"{member} Joined")
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')



bot.run(TOKEN)
