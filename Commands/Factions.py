import Helper
import requests
import discord
import random
import ast
import asyncio
from discord import Color
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.converter import MemberConverter

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

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

PINK = Color.from_rgb(255,185,209)

class FactionCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["dep"])
    async def deposit(self,ctx,amount:int):
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

    @commands.command(aliases=["f"])
    async def faction(self,ctx):  
        faction = Helper.getUserFaction(ctx.author.id)
        if faction == None:
            await ctx.send("You aren't in a faction! Make one with `,createfaction <Plot-Number> <Faction-Name>` Be sure to attach a Faction Logo Image too!")
            return
        else:
            factionEmoji = get(ctx.guild.emojis,name=faction["factionLogo"])
            factionName = str(faction["factionName"])
            factionOwner = self.bot.get_user(faction["id"])
            embed = discord.Embed(title=f"{factionName} {factionEmoji}",description=f"Faction Owner: {factionOwner}",colour=PINK)
            members = ""
            if "," in faction["factionMembers"]:
                membersList = str(faction["factionMembers"]).split(",")
                for x in membersList:
                    member = self.bot.get_user(int(x))
                    members += str(member) + "\n"
            else:
                members = self.bot.get_user(int(faction["factionMembers"]))
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

    @commands.command(name="createfaction")
    async def createfaction(self,ctx,plot:int,*name:str):
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

    @commands.command(name="invite")
    async def invite(self,ctx,member:MemberConverter):
        faction = Helper.getUserFaction(ctx.author.id)
        if member != None and faction != None:
            invited = Helper.getUserFaction(member.id)
            if invited == None:
                await ctx.send(f"{member} type `y` to accept the invitiation!")
                def check(m: discord.Message):
                    return m.author.id == member.id and m.channel.id == ctx.channel.id and m.content == "y" or "Y" 
                try:
                    msg = await self.bot.wait_for(event = 'message', check = check, timeout = 60.0)
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

    @commands.command(name="leavefaction")
    async def leavefaction(self,ctx):
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
            response = requests.delete(FACTION_URL + str(faction["id"]))
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
    @commands.command(name="map")
    async def map(self,ctx):
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

    @commands.command(aliases=["fs","fstore"])
    async def factionstore(self,ctx,selection:int=None,amount:int=1):
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

    @commands.command(name="attack")
    async def attack(self,ctx,plot:int):
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