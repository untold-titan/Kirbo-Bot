# bot.py

VERSION = 'V0.1.5 Factions Fixes'

from ctypes import util
import json
import os
import ast
import re
from warnings import resetwarnings
from discord import colour, embeds, member, user
from discord.ext.commands.converter import MemberConverter
import requests
import discord
import random
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color
from datetime import datetime, timedelta
from datetime import date
from discord.utils import get
from requests import api
from requests.models import Response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)


USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=',',intents=intents,activity=discord.Activity(type=discord.ActivityType.listening, name='Army Gang!'))
bot.titan=None

@bot.event
async def on_ready():
    bot.titan = bot.get_user(847989667088564244)
    bot.adminChat = bot.get_channel(764867760957947934)
    print(f'{bot.user.name} has connected to Discord!')

# Helper Functions -----------------------------------------------------------------
def getAllUsers():
    response = requests.get(USER_URL)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def getUserData(id):
    url = USER_URL + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def getAllFactions():
    response = requests.get(FACTION_URL)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def getUserFaction(id):
    response = getAllFactions()
    for x in response:
        factionData = ast.literal_eval(str(x))
        if ',' in factionData["factionMembers"]:
            members = str(factionData["factionMembers"]).split(",")
            for y in members:
                if y == str(id):
                    return factionData
        else:
            if factionData["factionMembers"] == str(id):
                return factionData

def updateFaction(faction):
    json = {
        "id":faction["id"],
        "factionName":faction["factionName"],
        "factionIncome":faction["factionIncome"],
        "factionMembers":faction["factionMembers"],
        "factionLandClaim":faction["factionLandClaim"],
        "factionLogo":faction["factionLogo"],
        "attack":faction["attack"],
        "defense":faction["defense"],
        "utility":faction["utility"],
        "balance":faction["balance"]
        }
    print(json)
    response = requests.put(FACTION_URL+"/"+str(faction["id"]),json=json)
    return response

# User Income Update Function ----------------------------------------------
from apscheduler.schedulers.background import BackgroundScheduler

# Start the scheduler
sched = BackgroundScheduler()

def job_function():
    users = getAllUsers()
    for user in users:
        faction = getUserFaction(user["id"])
        if faction != None:
            amount = int(faction["factionIncome"])
            tokens = int(user["token"]) + amount
            jsonData = {"id": user["id"], "token": tokens, "date": f"{user['date']}"}
            print(jsonData)
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
async def help(ctx, comnd: str=None):
    embed=discord.Embed(title="Kirbo Help",description="This bot's prefix is ','",color=PINK)
    embed.add_field(name="Fun Commands", value="about, poyo, roll, slap, shoot",inline=False)
    embed.add_field(name="Economy Commands",value="bal, daily, store, buy, give",inline=False)
    embed.add_field(name="Faction Commands",value="faction, createfaction, leavefaction, invite, deposit",inline=False)
    embed.add_field(name="Debugging Commands",value="testapi, shutdown",inline=False)

    await ctx.send(embed=embed)

# Fun Commands ------------------------------------------------------------------
slaps=[
    "https://media1.giphy.com/media/u8maN0dMhVWPS/giphy.gif?cid=ecf05e47qxkggg1r4jinkln0tb1u3dpifv9oi5qlh6pwha5g&rid=giphy.gif&ct=g",
    "https://media2.giphy.com/media/xUO4t2gkWBxDi/giphy.gif?cid=ecf05e472gsaenvi78og92yzidg1n3vwsqnrqc46wvm0mzn1&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/rCftUAVPLExZC/giphy.gif?cid=ecf05e47l30hhg2uu0gxsk5c10a1szljgzutl9zqddp4jz12&rid=giphy.gif&ct=g",
    "https://media3.giphy.com/media/4IDCnoWDFLTLa/giphy.gif?cid=ecf05e47v9srymnrqq83jpdet5046u0r3lpzblkkcj0zqwul&rid=giphy.gif&ct=g"
]

shoots=[
    "https://media1.giphy.com/media/PnhOSPReBR4F5NT5so/giphy.gif?cid=ecf05e47h3dm68qa24kn353rt774w4ef9g2qe7z8lkvu75cz&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/GEGnqhJcKyYoM/giphy.gif?cid=ecf05e47gdrly5qpksnw0bvxj5lsks749cb1tzmyi3s5n86t&rid=giphy.gif&ct=g",
    "https://media4.giphy.com/media/xTiTnnm7kR6MczdYEo/giphy.gif?cid=ecf05e47gdrly5qpksnw0bvxj5lsks749cb1tzmyi3s5n86t&rid=giphy.gif&ct=g"
]

finishers=[
    "https://cdn.discordapp.com/attachments/923389847232733295/925093106813108244/fatality-mortal.gif",
    "https://cdn.discordapp.com/attachments/923389847232733295/925093596149997628/mort-mortal-kombat.gif",
    "https://cdn.discordapp.com/attachments/923389847232733295/925093170398785566/tumblr_mj6l4nBwEb1s2b58zo1_500.gif",
    "https://cdn.discordapp.com/attachments/923389847232733295/925094364122873857/demon-slayer-tanjiro-vs-rui.gif"
]

@bot.command(name='poyo')
async def poyo(ctx):
    await ctx.send('Poyo!')

@bot.command(name="roll")
async def roll(ctx,number_of_dice: int,number_of_sides:int): 
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='about')
async def about(ctx):
    myEmbed=discord.Embed(title=f"Kirbo Bot {VERSION}",url="https://github.com/cataclysm-interactive/Kirbo-Bot",description="This bot was developed by Cataclysm-Interactive for the Army Gang", color=PINK)
    myEmbed.set_author(name="Untold_Titan#4644", icon_url="https://icy-mushroom-088e1a210.azurestaticapps.net/pfp.png")
    myEmbed.add_field(name="Changes:", value="Smashed a lot of bugs. Also added faction income, and upgrading stats.")
    myEmbed.add_field(name="Acknowledgements:", value="Titan - Lead Developer Lord Death_Trooper - Helping with testing and Ideas.")
    myEmbed.set_footer(text="This bot's code is on Github! Tap the embed to go there!")
    await ctx.send(embed=myEmbed)

@bot.command(name="slap")
async def slap(ctx, member: MemberConverter):
    embed=discord.Embed(title=f"{ctx.author.name} slapped {member.name}",color=PINK)
    imageNum = random.choice(range(0,len(slaps)))
    url = slaps[imageNum]
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command(name="shoot")
async def shoot(ctx, member: MemberConverter):
    embed=discord.Embed(title=f"{ctx.author.name} shot {member.name}",color=PINK)
    imageNum = random.choice(range(0,len(shoots)))
    url = shoots[imageNum]
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command(name="finish")
async def finish(ctx, member: MemberConverter):
    embed=discord.Embed(title=f"{ctx.author.name} finished {member.name}",color=PINK)
    imageNum = random.choice(range(0,len(finishers)))
    url = finishers[imageNum]
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    

# Economy Commands --------------------------------------------------------------

@bot.command(name='store')
async def store(ctx):
    embed=discord.Embed(title="Army Gang Token Store",description="Use `,buy <item-number>` to purchase an item!\n\n1. Custom Role = 15000 tokens \n ",color=PINK)
    embed.set_footer(text="If you have any ideas for things to put in the store, please DM Titan! :)")
    await ctx.send(embed=embed)

@bot.command(name="daily")
async def daily(ctx):
    await ctx.send("Hold on a sec, this might take some time!")
    currentdate = datetime.now()
    userId = ctx.author.id
    url = USER_URL + "/" + str(userId)
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

@bot.command(name="bal")
async def bal(ctx):
    jsonResponse = getUserData(ctx.author.id)
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
    url = USER_URL + "/" + str(ctx.author.id)
    data = getUserData(ctx.author.id)
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

@bot.command(name="give")
async def give(ctx,member: MemberConverter, amount: int):
    giver = getUserData(ctx.author.id)
    taker = getUserData(member.id)

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
    data = getUserData(ctx.author.id)
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


#  Faction Commands ----------------------------------------------------------------

factionTasks= [
    "Cleaning the floors...",
    "Catching Pokemon...",
    "Secretly Building a Nuclear Weapon...",
    "Cooking Tacos...",
    "Serving up some fresh Pizza...",
    "Selling 17 metric tons of weed...",
    "Slowly decending into madness...",
    "Plotting a coupé...",
    "Hiding bodies...",
    "Nothing...",
    "Sleeping..."
]

@bot.command(name="deposit")
async def deposit(ctx,amount:int):
    user = getUserData(ctx.author.id)
    faction = getUserFaction(ctx.author.id)
    if faction == None:
        await ctx.send("You aren't in a faction!")
        return
    if int(user["token"]) < amount:
        await ctx.send("You don't have enough tokens! Pick a smaller amount.")
        return
    faction["balance"] = int(faction["balance"]) + amount
    jsonData = {"Id": f"{ctx.author.id}", "token": int(user["token"]) - amount, "date": f"{user['date']}"}
    response = requests.put(USER_URL+"/"+str(ctx.author.id),json=jsonData)
    response = updateFaction(faction=faction)
    if response.status_code == 204:
        await ctx.send(f"Added {amount} to the faction vault!")
    else:
        await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")

@bot.command(name="faction")
async def faction(ctx):  
    faction = getUserFaction(ctx.author.id)
    if faction == None:
        await ctx.send("You aren't in a faction! Make one with `,createfaction <Plot-Number> <Faction-Name>` Be sure to attach a Faction Logo Image too!")
        return
    else:
        factionEmoji = get(ctx.guild.emojis,name=faction["factionLogo"])
        factionName = str(faction["factionName"])
        factionOwner = bot.get_user(faction["id"])
        embed = discord.Embed(title=f"{factionName} {factionEmoji}",description=f"Faction Owner: {factionOwner}",colour=PINK)
        members = ""
        if "," in faction["factionMembers"]:
            membersList = str(faction["factionMembers"]).split(",")
            for x in membersList:
                member = bot.get_user(int(x))
                members += str(member) + "\n"
        else:
            members = bot.get_user(int(faction["factionMembers"]))

        embed.add_field(name="Faction Members:",value=f"{members}",inline=False)
        status = random.choice(range(0,len(factionTasks)))
        embed.add_field(name="Faction Status:",value=f"{factionTasks[status]}",inline=False)
        embed.add_field(name="Faction Stats",value=f"Income: {faction['factionIncome']} Tokens\nAttack: {faction['attack']}\nDefense: {faction['defense']}\nUtility: {faction['utility']}\nVault: {faction['balance']} Tokens")
        embed.add_field(name="Faction Plots:",value=f"{faction['factionLandClaim']}")

        await ctx.send(embed=embed)

@bot.command(name="createfaction")
async def createfaction(ctx,plot:int,*name:str):
    await ctx.send("Please hold for a bit. This may take a while.")
    faction = getUserFaction(ctx.author.id)

    factionName = ""
    for x in name:
        factionName = factionName +" "+ x
    if faction == None:
        otherFactions = getAllFactions()
        if otherFactions != None:
            for x in otherFactions:
                faction = ast.literal_eval(str(x))
                plots = faction["factionLandClaim"].split(",")
                for y in plots:
                    if int(y) == plot:
                        await ctx.send("This location is already owned! Please pick a different location.")
                        return
        if len(ctx.message.attachments) == 0:
            await ctx.send("You need to upload a photo to create a faction!")
            return
        else:
            img_data = requests.get(ctx.message.attachments[0].url).content
            emojiName = factionName.replace(" ","")
            emojiName = emojiName.replace("'","")
            emojiName = emojiName.replace(",","")
            await ctx.guild.create_custom_emoji(name=str(emojiName),image=img_data)
        json = {"id":f"{ctx.author.id}","factionName":f"{factionName}","factionIncome":10,"factionMembers":f"{ctx.author.id}","factionLandClaim":str(plot),"factionLogo":f"{emojiName}","attack":10,"defense":10,"utility":10}
        response = requests.post(FACTION_URL,json=json)   
        
        if response.status_code == 201:
            await ctx.send("Your faction has been created! Use `,faction` to view it!")
        else:
            await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")
    else:
        await ctx.send("You're already in a Faction! Use `,faction` to view it!")

@bot.command(name="invite")
async def invite(ctx,member:MemberConverter):
    faction = getUserFaction(ctx.author.id)
    if member != None and faction != None:
        invited = getUserFaction(member.id)
        if invited == None:
            await ctx.send(f"{member} type `y` to accept the invitiation!")
            def check(m: discord.Message):
                return m.author.id == member.id and m.channel.id == ctx.channel.id and m.content =="y"
            try:
                msg = await bot.wait_for(event = 'message', check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                await ctx.send(f"Automatically declined invite.")
                return
            else:
                faction["factionMembers"] = faction['factionMembers'] + ',' + str(member.id)
                response = updateFaction(faction=faction)
                if response.status_code == 204:
                    await ctx.send(f"{member} You accepted the invite. Welcome to {faction['factionName']}!")
                else:
                    await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")
                return
        else:
            await ctx.send(f"{member} needs to leave their faction in order to be invited to this one!")
    else:
        await ctx.send("You need to include a member to invite")

@bot.command(name="leavefaction")
async def leavefaction(ctx):
    faction = getUserFaction(ctx.author.id)
    if faction == None:
        await ctx.send("You aren't in a faction!")
        return
    members = str(faction["factionMembers"]).split(',')
    members.remove(str(ctx.author.id))
    string = ""
    for x in members:
        string += x + ","
    if string == "":
        response = requests.delete(FACTION_URL + "/" + str(faction["id"]))
        emojis = ctx.guild.emojis
        for emoji in emojis:
            if emoji.name == faction["factionLogo"]:
                await emoji.delete()
    else:
        faction["factionMembers"] = string[:-1]
        response = updateFaction(faction=faction)
        
    if response.status_code == 204:
        await ctx.send("You left your faction!")
    else:
        await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")

@bot.command(name="map")
async def map(ctx):
    # Creating the base land map.
    map = []
    landEmoji = get(ctx.guild.emojis, name="unclaimed")
    for x in range(100):
        map.append(f"{landEmoji}")

    #Adding the factions
    factions = getAllFactions()
    for x in factions:
        faction = ast.literal_eval(str(x))
        locationString = faction["factionLandClaim"]
        locations = locationString.split(",")
        emoji = get(ctx.guild.emojis,name=faction["factionLogo"])
        for y in locations:
            map[int(y)-1] = f"{emoji}"
    
    #Formatting the map for Discord
    for x in range(9):
        map.insert((((x*10)+10)+x),"\n")
    string = ""
    for x in map:
        string += x
    embed = discord.Embed(title="Factions Map",description=string, colour=PINK)
    await ctx.send(embed=embed)
# this function was a PAIN IN THE ASS
@bot.command(name="factionstore")
async def factionstore(ctx,selection:int=None):
    if selection == None:
        embed = discord.Embed(title="Factions Store", description="This store allows you to purchase upgrades for your faction!",colour=PINK)
        embed.add_field(name="Faction Upgrades:",value="1. Income, $500 per level, increases income by 10 per hour. \n2. Attack, $1000 per level, increases attack by 10 per level.\n3. Defense, $1000 per level, increases defense by 10 per level.\n4. Utility, $1000 per level, increases utility by 10 per level.")
        
        await ctx.send(embed=embed)
    if selection == 1:
        faction = getUserFaction(ctx.author.id)
        income = int(faction["factionIncome"])
        if int(faction["balance"]) >= 500:
            income += 10
            faction["factionIncome"] = income
            faction["balance"] = int(faction["balance"]) - 500
            updateFaction(faction=faction)
            await ctx.send(f"Income was upgraded! Your faction now makes {income} tokens per hour!")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 2:
        faction = getUserFaction(ctx.author.id)
        attack = int(faction["attack"])
        if int(faction["balance"]) >= 1000:
            attack += 10
            faction["attack"] = attack
            faction["balance"] = int(faction["balance"]) - 1000
            updateFaction(faction=faction)
            await ctx.send(f"Income was upgraded! Your faction now has an attack of {attack}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 3:
        faction = getUserFaction(ctx.author.id)
        defense = int(faction["defense"])
        if int(faction["balance"]) >= 1000:
            defense += 10
            print(defense)
            faction["defense"] = defense
            faction["balance"] = int(faction["balance"]) - 1000
            updateFaction(faction=faction)
            await ctx.send(f"Defense was upgraded! Your faction now has a defense of {defense}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 4:
        faction = getUserFaction(ctx.author.id)
        utility = int(faction["utility"])
        if int(faction["balance"]) >= 1000:
            utility += 10
            faction["utility"] = utility
            faction["balance"] = int(faction["balance"]) - 1000
            updateFaction(faction=faction)
            await ctx.send(f"Utility was upgraded! Your faction now has a utility of {utility}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")


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

@bot.command("repeat")
async def repeat(ctx,data:str):
    await ctx.send(data)


#Events ---------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Thats an admin only command!')
    await ctx.send("Something went wrong!")
    await bot.titan.send(f"{error}")

@bot.event 
async def on_member_remove(member):
    await bot.adminChat.send(f"{member} Left")

@bot.event
async def on_member_join(member):
    await bot.adminChat.send(f"{member} Joined")
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')



bot.run(TOKEN)
