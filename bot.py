# bot.py
VERSION = 'V0.0.1 STABLE'
import json
import os
import ast
from discord import colour, embeds, member
from discord.ext.commands.converter import MemberConverter
import requests
import discord
import random
from discord import client
from dotenv import load_dotenv
from discord.ext import commands
from discord import Color
from requests.models import Response
from datetime import datetime
from datetime import date
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PINK = Color.from_rgb(255,185,209)


API_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"
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
def getUserData(id):
    url = API_URL + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse



#Help Command --------------------------------------------------------------
bot.remove_command('help')
@bot.command("help")
async def help(ctx, comnd: str=None):
    embed=discord.Embed(title="Kirbo Help",description="This bot's prefix is ','",color=PINK)
    embed.add_field(name="Fun Commands", value="about, poyo, roll, slap, shoot",inline=False)
    embed.add_field(name="Economy Commands",value="bal, daily, store, buy",inline=False)
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
    myEmbed.set_author(name="christmas titan#1704", icon_url="https://icy-mushroom-088e1a210.azurestaticapps.net/pfp.png")
    myEmbed.add_field(name="Acknowledgements:", value="Titan - Lead Developer")
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
    

# Economy Commands --------------------------------------------------------------

@bot.command(name='store')
async def store(ctx):
    embed=discord.Embed(title="Army Gang Token Store",description="Use `,buy <item-number>` to purchase an item!\n\n1. Custom Role = 15000 tokens \n ",color=PINK)
    embed.set_footer(text="If you have any ideas for things to put in the store, please DM Titan! :)")
    await ctx.send(embed=embed)

@bot.command(name="daily")
async def daily(ctx):
    currentdate = date.today()
    userId = ctx.author.id
    url = API_URL + "/" + str(userId)
    response = requests.get(url)
    jsonResponse = ast.literal_eval(str(response.json()))
    if response.status_code == 404:
        jsonData = {"Id": f"{userId}", "token": 500, "date": f"{currentdate}"}
        response = requests.post(API_URL,json=jsonData)
        if response.status_code == 201:
            embed = discord.Embed(title="Daily Token Reward", description="You gained 500 AG Tokens!",color=PINK)
            await ctx.send(embed=embed)
        else:
            await ctx.send("There was an issue contacting the CataclysmAPI (ERROR CODE = 1)")
            await bot.titan.send(f"Couldn't contact the API, Status code returned with: {response.status_code}")
    elif response.status_code == 200:
        actualDate = datetime.strptime(jsonResponse["date"], '%Y-%m-%dT%H:%M:%S')
        if (currentdate - actualDate.date()).days >= 1:
            total = int(jsonResponse["token"]) + 500
            jsonData = {"Id": f"{userId}","token": f"{total}", "date": f"{currentdate}"}
            response = requests.put(url,json=jsonData)
            if response.status_code == 204:
                embed = discord.Embed(title="Daily Token Reward", description="You gained 500 AG Tokens!",color=PINK)
                await ctx.send(embed=embed)
            else:
                await ctx.send("There was an issue contacting the CataclysmAPI (ERROR CODE = 2)")
                await bot.titan.send(f"Couldn't contact the API, Status code returned with: {response.status_code}")
        else:
            await ctx.send("You already claimed today's reward! Please try again tommorow")
    else:
        await ctx.send("There was an issue contacting the CataclysmAPI ERROR CODE = 3")
        await bot.titan.send(f"I was unable to contact the CataclysmAPI. \n Status code is: {response.status_code}.")

@bot.command(name="bal")
async def bal(ctx):
    jsonResponse = getUserData(ctx.author.id)
    if jsonResponse == None:
        json = {"Id":f"{ctx.author.id}"}
        response= requests.post(API_URL,json)
        tokenAmt = 0
    else:
        tokenAmt = jsonResponse["token"]
    embed = discord.Embed(title=f"{ctx.author}'s Token Balance", description=f"{tokenAmt} AG tokens",color=PINK)
    await ctx.send(embed=embed)

@bot.command(name="buy")
async def buy(ctx,item: int):
    url = API_URL + "/" + str(ctx.author.id)
    data = getUserData(ctx.author.id)
    if item == 1:
        if (int(data["token"]) - 15000) >= 0 and data["customRole"] != 1:
            tokens = int(data["token"]) - 15000
            jsonData = {"Id": f"{ctx.author.id}", "token":f"{tokens}","customRole":1}
            response= requests.put(url,json=jsonData)
            if response.status_code == 204:
                await ctx.send("You purchased a Custom Role!\nUse `,customrole <name> <color-hex-code>` to claim it!")
            else:
                await ctx.send("There was an issue contacting the CataclysmAPI ERROR CODE = 4")
                await bot.titan.send(f"I was unable to contact the CataclysmAPI. \n Status code is: {response.status_code}. \n JSON is: {response.json()}")
        else:
            if data["customRole"] == 1:
                await ctx.send("You already have a custom role!")
                return
            await ctx.send("You don't have enough tokens!")

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
    response = requests.get(API_URL)
    await ctx.send(response.json())

@bot.command(name="shutdown")
@commands.has_role("admin")
async def shutdown(ctx):
    await ctx.send("Shutting down Kirbo bot!")
    quit()

@bot.command(name="testmsgs")
@commands.has_role("admin")
async def testmsgs(ctx):
    await bot.titan.send("Test")
    await bot.adminChat.send("Test")


#Events ---------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Thats an admin only command!')
    await ctx.send(error)
    #await bot.titan.send(f"{error}")

@bot.event 
async def on_member_remove(member):
    await bot.adminChat.send(f"{member} Left")

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the Army Gang, {member.name}. Please take a look at #rules-roles to get access to the rest of the server! If you need anything, feel free to ping Titan or Coolr.')



bot.run(TOKEN)
