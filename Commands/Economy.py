import Helper
import requests
import discord
import ast
from discord import Color
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter
from datetime import datetime, timedelta

PINK = Color.from_rgb(255,185,209)

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

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
    892479878585286696,
    987535775455395880
]

class EconomyCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Economy Commands --------------------------------------------------------------

    @commands.command(aliases=["s","shop"])
    async def store(self,ctx):
        embed=discord.Embed(title="Army Gang Token Store",description="Use `,buy <item-number>` to purchase an item!",color=PINK)
        embed.add_field(name="1. Custom Role",value="50,000 tokens")
        embed.add_field(name="2. S Tier Gamer",value="25,000 tokens")
        embed.add_field(name="3. A Tier Gamer",value="20,000 tokens")
        embed.add_field(name="4. B Tier Gamer",value="15,000 tokens")
        embed.add_field(name="5. C Tier Gamer",value="10,000 tokens")
        embed.add_field(name="6. D Tier Gamer",value="5,000 tokens")
        i = 7
        for roleID in roleIDS:
            role = self.bot.get_guild(752023138795126856).get_role(roleID)
            embed.add_field(name=f"{i}. {role.name}",value="Price: FREE!",inline=False)
            i += 1
        embed.set_footer(text="If you have any ideas for things to put in the store, please DM Titan! :)")
        await ctx.send(embed=embed)

    @commands.command(aliases=["d"])
    async def daily(self,ctx):
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

    @commands.command(aliases=["balance","b"])
    async def bal(self,ctx):
        jsonResponse = Helper.getUserData(ctx.author.id)
        if jsonResponse == None:
            json = {"Id":f"{ctx.author.id}"}
            response = requests.post(USER_URL,json)
            tokenAmt = 0
        else:
            tokenAmt = jsonResponse["token"]
        embed = discord.Embed(title=f"{ctx.author}'s Token Balance", description=f"{tokenAmt} AG tokens",color=PINK)
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy(self,ctx,item: int):
        url = USER_URL + "/" + str(ctx.author.id)
        data = Helper.getUserData(ctx.author.id)
        if item == 1:
            if (int(data["token"]) - 50000) >= 0 and data["customRole"] != 1:
                tokens = int(data["token"]) - 50000
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
        elif item == 2:
            hasPreviousRole = False
            for role in ctx.author.roles:
                if(role.id == 794982165385052182):
                    hasPreviousRole = True
            if (int(data["token"]) - 25000) >= 0 and hasPreviousRole == True:
                data["token"] = str(int(data["token"]) - 25000)
                response= requests.put(url,json=data)
                if response.status_code == 204:
                    role = self.bot.get_guild(752023138795126856).get_role(794982243419422760)
                    await ctx.author.add_roles(role)
                    await ctx.send("You purchased S Tier Gamer! You're breathtaking!")
                else:
                    await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
            elif hasPreviousRole == False:
                await ctx.send("You must purchase A Tier Gamer first!")
            else:
                await ctx.send("You don't have enough tokens!")
        elif item == 3:
            hasPreviousRole = False
            for role in ctx.author.roles:
                if(role.id == 794982115589619752):
                    hasPreviousRole = True
            if (int(data["token"]) - 20000) >= 0 and hasPreviousRole == True:
                data["token"] = str(int(data["token"]) - 20000)
                response= requests.put(url,json=data)
                if response.status_code == 204:
                    role = self.bot.get_guild(752023138795126856).get_role(794982115589619752)
                    await ctx.author.add_roles(role)
                    await ctx.send("You purchased A Tier Gamer! You're Amazing!!")
                else:
                    await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
            elif hasPreviousRole == False:
                await ctx.send("You must purchase B Tier Gamer first!")
            else:
                await ctx.send("You don't have enough tokens!")
        elif item == 4:
            hasPreviousRole = False
            for role in ctx.author.roles:
                if(role.id == 794982059822022657):
                    hasPreviousRole = True
            if (int(data["token"]) - 15000) >= 0 and hasPreviousRole == True:
                data["token"] = str(int(data["token"]) - 15000)
                response= requests.put(url,json=data)
                if response.status_code == 204:
                    role = self.bot.get_guild(752023138795126856).get_role(794982059822022657)
                    await ctx.author.add_roles(role)
                    await ctx.send("You purchased B Tier Gamer!")
                else:
                    await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
            elif hasPreviousRole == False:
                await ctx.send("You must purchase C Tier Gamer first!")
            else:
                await ctx.send("You don't have enough tokens!")
        elif item == 5:
            hasPreviousRole = False
            for role in ctx.author.roles:
                if(role.id == 794981977568706610):
                    hasPreviousRole = True
            if (int(data["token"]) - 10000) >= 0 and hasPreviousRole == True:
                data["token"] = str(int(data["token"]) - 10000)
                response= requests.put(url,json=data)
                if response.status_code == 204:
                    role = self.bot.get_guild(752023138795126856).get_role(794982115589619752)
                    await ctx.author.add_roles(role)
                    await ctx.send("You purchased C Tier Gamer!")
                else:
                    await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
            elif hasPreviousRole == False:
                await ctx.send("You must purchase D Tier Gamer first!")
            else:
                await ctx.send("You don't have enough tokens!")
        elif item == 6:
            if (int(data["token"]) - 5000) >= 0:
                data["token"] = str(int(data["token"]) - 5000)
                response= requests.put(url,json=data)
                if response.status_code == 204:
                    role = self.bot.get_guild(752023138795126856).get_role(794981977568706610)
                    await ctx.author.add_roles(role)
                    await ctx.send("You purchased D Tier Gamer!")
                else:
                    await ctx.send(f"There was an issue contacting the CataclysmAPI ERROR CODE = {response.status_code}")
            else:
                await ctx.send("You don't have enough tokens!")
        elif item > 6:
            role = self.bot.get_guild(752023138795126856).get_role(roleIDS[item - 7])
            await ctx.author.add_roles(role)
            await ctx.send(f"You bought: {role.name}")

    @commands.command(name="give")
    async def give(self,ctx,member: MemberConverter, amount: int):
        giver = Helper.getUserData(ctx.author.id)
        taker = Helper.getUserData(member.id)

        if giver != None and taker != None and giver["token"] >= amount and amount > 0:
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
                await ctx.send("Something went wrong")
        elif taker == None:
            await ctx.send(member +"has to earn some tokens before they can recive!")
        elif giver == None:
            await ctx.send(ctx.author +"has to earn some tokens before they can send!")
        elif giver["token"] < amount:
            await ctx.send("You don't have enough tokens!")
        elif amount <= 0:
            await ctx.send("Haha, this was fixed. Get outta here.")
        else:
            await ctx.send("Something went wrong. Try again later!")

    @commands.command(name="customrole")
    async def customrole(self,ctx,roleName:str,r:int,g:int,b:int):
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
