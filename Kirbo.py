# bot.py

import os
import ast
from discord.ext.commands.converter import MemberConverter
import requests
import discord
import random
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color
from datetime import datetime, timedelta
from discord.utils import get
import Helper
import sys
sys.path.insert(0,"Commands")
from Fun import FunCog

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
async def help(ctx, comnd: str=None):
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
    url = USER_URL + "/" + str(ctx.author.id)
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


# Faction Commands ----------------------------------------------------------------

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
    "Sleeping...",
    "Killing 100 Bidoofs, because why tf not..."
]

@bot.command(aliases=["dep"])
async def deposit(ctx,amount:int):
    user = Helper.getUserData(ctx.author.id)
    faction = Helper.getUserFaction(ctx.author.id)
    if faction == None:
        await ctx.send("You aren't in a faction!")
        return
    if int(user["token"]) < amount:
        await ctx.send("You don't have enough tokens! Pick a smaller amount.")
        return
    faction["balance"] = int(faction["balance"]) + amount
    jsonData = {"Id": f"{ctx.author.id}", "token": int(user["token"]) - amount, "date": f"{user['date']}"}
    response = requests.put(USER_URL+"/"+str(ctx.author.id),json=jsonData)
    response = Helper.updateFaction(faction=faction)
    if response.status_code == 204:
        await ctx.send(f"Added {amount} to the faction vault!")
    else:
        await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")

@bot.command(aliases=["f"])
async def faction(ctx):  
    faction = Helper.getUserFaction(ctx.author.id)
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
        map = Helper.getAllMapTiles()
        tilesOwned = []
        for x in map:
            if x["plotOwner"] == faction["factionName"]:
                tilesOwned.append(x["plotNum"])
        embed.add_field(name="Faction Plots:",value=f"{tilesOwned}")

        await ctx.send(embed=embed)

@bot.command(name="createfaction")
async def createfaction(ctx,plot:int,*name:str):
    await ctx.send("Please hold for a bit. This may take a while.")
    faction = Helper.getUserFaction(ctx.author.id)

    factionName = ""
    for x in name:
        factionName = factionName +" "+ x
    if faction == None:
        #Checking if the Plot is already claimed. 
        tile = Helper.getMapTile(plot)
        if tile["plotOwner"] != "Unclaimed!":
            await ctx.send("This plot is already claimed!")
            return
        # Checking for image, If there is one, upload it as an emoji
        if len(ctx.message.attachments) == 0:
            await ctx.send("You need to upload a photo to create a faction!")
            return
        else:
            img_data = requests.get(ctx.message.attachments[0].url).content
            emojiName = factionName.replace(" ","")
            emojiName = emojiName.replace("'","")
            emojiName = emojiName.replace(",","")
            await ctx.guild.create_custom_emoji(name=str(emojiName),image=img_data)
        succedded = Helper.claimMapTile(plot,factionName)
        if succedded != True:
            await ctx.send("Failed to claim plot. Please try again later!")
            return
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
    faction = Helper.getUserFaction(ctx.author.id)
    if member != None and faction != None:
        invited = Helper.getUserFaction(member.id)
        if invited == None:
            await ctx.send(f"{member} type `y` to accept the invitiation!")
            def check(m: discord.Message):
                return m.author.id == member.id and m.channel.id == ctx.channel.id and m.content == "y" or "Y" 
            try:
                msg = await bot.wait_for(event = 'message', check = check, timeout = 60.0)
            except asyncio.TimeoutError:
                await ctx.send(f"Automatically declined invite.")
                return
            else:
                faction["factionMembers"] = faction['factionMembers'] + ',' + str(member.id)
                response = Helper.updateFaction(faction=faction)
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
    faction = Helper.getUserFaction(ctx.author.id)
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
        response = Helper.updateFaction(faction=faction)
        
    if response.status_code == 204:
        await ctx.send("You left your faction!")
    else:
        await ctx.send(f"There was an issue contacting the Cataclysm API. Error code: {response.status_code}")
# this function was a PAIN IN THE ASS
@bot.command(name="map")
async def map(ctx):
    # Creating the base land map.
    map = []
    landEmoji = get(ctx.guild.emojis, name="unclaimed")
    for x in range(100):
        map.append(f"{landEmoji}")

    factions = Helper.getAllFactions()
    mapTiles = Helper.getAllMapTiles()
    for i in mapTiles:
        if i['plotOwner'] != "Unclaimed!":
            map[int(i["plotNum"]) - 1] = i["plotOwner"]
     
    #Formatting the map for Discord
    for x in range(9):
        map.insert((((x*10)+10)+x),"\n")
    string = ""
    for x in map:
        string += x
    embed = discord.Embed(title="Factions Map",description=string, colour=PINK)
    await ctx.send(embed=embed)

@bot.command(aliases=["fs","fstore"])
async def factionstore(ctx,selection:int=None,amount:int=1):
    if selection == None:
        embed = discord.Embed(title="Factions Store", description="This store allows you to purchase upgrades for your faction!",colour=PINK)
        embed.add_field(name="Faction Upgrades:",value="1. Income, $500 per level, increases income by 10 per hour. \n2. Attack, $1000 per level, increases attack by 10 per level.\n3. Defense, $1000 per level, increases defense by 10 per level.\n4. Utility, $1000 per level, increases utility by 10 per level.")
        
        await ctx.send(embed=embed)
    if selection == 1:
        faction = Helper.getUserFaction(ctx.author.id)
        income = int(faction["factionIncome"])
        if int(faction["balance"]) >= 500 * amount:
            income += 10 * amount
            faction["factionIncome"] = income
            faction["balance"] = int(faction["balance"]) - 500 * amount
            Helper.updateFaction(faction=faction)
            await ctx.send(f"Income was upgraded! Your faction now makes {income} tokens per hour!")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 2:
        faction = Helper.getUserFaction(ctx.author.id)
        attack = int(faction["attack"])
        if int(faction["balance"]) >= 1000 *amount :
            attack += 10 * amount
            faction["attack"] = attack
            faction["balance"] = int(faction["balance"]) - 1000 * amount
            Helper.updateFaction(faction=faction)
            await ctx.send(f"Income was upgraded! Your faction now has an attack of {attack}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 3:
        faction = Helper.getUserFaction(ctx.author.id)
        defense = int(faction["defense"])
        if int(faction["balance"]) >= 1000*amount:
            defense += 10 * amount
            print(defense)
            faction["defense"] = defense
            faction["balance"] = int(faction["balance"]) - 1000 * amount
            Helper.updateFaction(faction=faction)
            await ctx.send(f"Defense was upgraded! Your faction now has a defense of {defense}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    elif selection == 4:
        faction = Helper.getUserFaction(ctx.author.id)
        utility = int(faction["utility"])
        if int(faction["balance"]) >= 1000*amount:
            utility += 10 * amount
            faction["utility"] = utility
            faction["balance"] = int(faction["balance"]) - 1000 * amount
            Helper.updateFaction(faction=faction)
            await ctx.send(f"Utility was upgraded! Your faction now has a utility of {utility}")
        else:
            await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")

@bot.command(name="attack")
async def attack(ctx,plot:int):
    # Generating the map, and figuring out the owner of the plot
    map = []
    for x in range(100):
        map.append(0)
    factions = Helper.getAllFactions()
    for faction in factions:
        
        faction = ast.literal_eval(str(x))
        locationString = faction["factionLandClaim"]
        locations = locationString.split(",")
        print("Looping through the factions")
        for y in locations:
            print(map[y])
            if(map[y] == int(faction["id"])):
                print("Found plot owner")
    
    # plotOwner = map[plot - 1]

    # if plotOwner == 0:
    #     faction = getUserFaction(ctx.author.id)
    #     defense = int(faction["defense"])
    #     if int(faction["balance"]) >= 1000*amount:
    #         defense += 10 * amount
    #         faction["defense"] = defense
    #         faction["balance"] = int(faction["balance"]) - 1000 * amount
    #         updateFaction(faction=faction)
    #         await ctx.send(f"Defense was upgraded! Your faction now has a defense of {defense}")
    #     else:
    #         await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")
    # elif selection == 4:
    #     faction = getUserFaction(ctx.author.id)
    #     utility = int(faction["utility"])
    #     if int(faction["balance"]) >= 1000*amount:
    #         utility += 10 * amount
    #         faction["utility"] = utility
    #         faction["balance"] = int(faction["balance"]) - 1000 * amount
    #         updateFaction(faction=faction)
    #         await ctx.send(f"Utility was upgraded! Your faction now has a utility of {utility}")
    #     else:
    #         await ctx.send("Your faction vault doesn't have enough tokens! Deposit some with `,deposit <amount>`")


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
