import random
import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter

VERSION = 'V0.1.8'
PINK = Color.from_rgb(255,185,209)

slaps=[
    "https://media2.giphy.com/media/xUO4t2gkWBxDi/giphy.gif?cid=ecf05e472gsaenvi78og92yzidg1n3vwsqnrqc46wvm0mzn1&rid=giphy.gif&ct=g",
    "https://media1.giphy.com/media/u8maN0dMhVWPS/giphy.gif?cid=ecf05e47qxkggg1r4jinkln0tb1u3dpifv9oi5qlh6pwha5g&rid=giphy.gif&ct=g",
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
    "https://cdn.discordapp.com/attachments/923389847232733295/925094364122873857/demon-slayer-tanjiro-vs-rui.gif",
    "https://cdn.discordapp.com/attachments/923389847232733295/940319257235976292/demon-slayer.gif",
    "https://cdn.discordapp.com/attachments/923389847232733295/940319559859179621/astartes-warhammer.gif"
]
class FunCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='poyo')
    async def poyo(self,ctx):
        await ctx.send('Poyo!')

    @commands.command(name="roll")
    async def roll(self,ctx,number_of_dice: int,number_of_sides:int): 
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(name='about')
    async def about(self,ctx):
        myEmbed=discord.Embed(title=f"Kirbo Bot {VERSION}",url="https://github.com/cataclysm-interactive/Kirbo-Bot",description="This bot was developed by Untold_Titan for the Army Gang", color=PINK)
        myEmbed.set_author(name="Untold_Titan#4644", icon_url="https://icy-mushroom-088e1a210.azurestaticapps.net/pfp.png")
        myEmbed.add_field(name="Changes:", value="Added Magic the Gathering Commands, Also fixed several bugs, and added the Gamer Tiers.")
        myEmbed.add_field(name="Acknowledgements:", value="Titan - Lead Developer\nLord Death_Trooper - Helping with testing and Ideas.")
        myEmbed.set_footer(text="This bot's code is on Github! Tap the embed to go there!")
        await ctx.send(embed=myEmbed)

    @commands.command(name="slap")
    async def slap(self,ctx, member: MemberConverter):
        embed=discord.Embed(title=f"{ctx.author.name} slapped {member.name}",color=PINK)
        imageNum = random.choice(range(0,len(slaps)))
        url = slaps[imageNum]
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="shoot")
    async def shoot(self,ctx, member: MemberConverter):
        embed=discord.Embed(title=f"{ctx.author.name} shot {member.name}",color=PINK)
        imageNum = random.choice(range(0,len(shoots)))
        url = shoots[imageNum]
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="finish")
    async def finish(self,ctx, member: MemberConverter):
        embed=discord.Embed(title=f"{ctx.author.name} finished {member.name}",color=PINK)
        imageNum = random.choice(range(0,len(finishers)))
        url = finishers[imageNum]
        embed.set_image(url=url)
        await ctx.send(embed=embed)